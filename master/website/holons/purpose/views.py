from datetime import datetime, timedelta
import logging
import itertools

from django.conf import settings
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator 
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView

from .models import CheckIn, Context, KeyResultType, Purpose, Objective, KeyResult
from .serializers import ContextSerializer, KeyResultSerializer, KeyResultTypeSerializer, ObjectiveSerializer, PurposeSerializer

RAY_SOURCES = settings.RAY_SOURCES
LOGIN_REDIRECT_URL  = '/auth'
LOGIN_URL  = '/auth'

not_valid_response = JsonResponse({
  'success': False,
  'message': 'Data is not valid'
}, status=400)
forbidden_response = JsonResponse({
  'success': False,
  'message': 'You have not access'
}, status=403)

@require_http_methods(['GET'])
@login_required
def contexts(request: HttpRequest) -> JsonResponse:
  # TODO replace creating new contexts logic to another place
  if not Context.objects.filter(user_personal=request.user).first():
    logging.info('Create a new personal context for user ' + str(request.user))
    Context(user_personal=request.user).save()

  if not Context.objects.filter(user_handle=request.user).first():
    logging.info('Create a new handle context for user ' + str(request.user))
    Context(user_handle=request.user).save()

  for entity in request.user.entities.all():
    if not Context.objects.filter(entity=entity).first():
      logging.info('Create a new handle context for entity ' + str(entity))
      Context(entity=entity).save()

  return JsonResponse(ContextSerializer(Context.objects.filter(
    Q(user_personal=request.user.id) | 
    Q(user_handle=request.user.id) | 
    Q(entity__in=[e.id for e in request.user.entities.all()]) |
    Q(id__in=[kr.context.id for kr in request.user.owned_krs.all()]) 
  ), many=True).data, safe=False)


def start_purpose(purpose : Purpose):
  if not purpose.objectives.first() or purpose.context.purposes.filter(start_at__isnull=False, finish_at__isnull=True).first():
    return JsonResponse({
      'success': False,
      'message': 'To start the season, you must create at least one objective. If you have unfinished season, you can\'t start new'
    }, status=409)
  
  purpose.start_at = timezone.now()
  purpose.save()

  first_sunday = (purpose.start_at + timezone.timedelta(7 - (purpose.start_at.weekday() + 1))).replace(hour=12, minute=0, second=0)

  for kr in itertools.chain(*[o.key_results.all() for o in purpose.objectives.all()]):
    current_date = first_sunday

    while current_date <= purpose.plan_end_date:
      check_in = CheckIn(date=current_date, key_result=kr)
      check_in.save()

      current_date += timedelta(7 * kr.interval) 

  return JsonResponse({'success': True}) 

class PurposeAPI(APIView):  
  @method_decorator(login_required)
  def get(self, request: HttpRequest):
    return JsonResponse(PurposeSerializer(Purpose.objects.filter(
      Q(owner_id=request.user.id) |
      Q(id__in=[kr.objective.purpose.id if kr.objective.purpose.status != 'draft' else 0 for kr in request.user.owned_krs.all()])
    ).all(), many=True).data, safe=False)

  @method_decorator(login_required)
  def post(self, request: HttpRequest):
    parsed_request = request.data
    context = Context.objects.filter(pk=parsed_request.get('context_id', None)).first()
    
    if not context:
      return not_valid_response

    if not request.user.id == context.owner.id:
      return forbidden_response

    current_draft = Purpose.objects.filter(owner_id=request.user.id, finish_at__isnull=True, start_at__isnull=True, context_id=context.id).first()

    if current_draft:
      return JsonResponse({
        'success': False,
        'message': 'You have draft for this context'
      }, status=409)
    
    parsed_request['owner_id'] = str(request.user.id)

    raw_purpose = PurposeSerializer(data=parsed_request)

    if not raw_purpose.is_valid():
      return not_valid_response

    purpose = raw_purpose.save()
    return JsonResponse({'success': True, 'id': purpose.id}, status=201) 
  
  @method_decorator(login_required)
  def patch(self, request: HttpRequest, id: int):
    purpose = get_object_or_404(Purpose, pk=id)

    if not request.user.id == purpose.owner.id:
      return forbidden_response
  
    if purpose.status == 'draft':
      if 'start_at' in request.data:
        return start_purpose(purpose)

      for field in ['context_id', 'owner_id']:
        if field in request.data:
          del request.data[field]
      
      # print(request.data)
      raw_purpose = PurposeSerializer(instance=purpose, data=request.data, partial=True)
      if not raw_purpose.is_valid():
        return not_valid_response  
      
      raw_purpose.save()
    elif purpose.status == 'start':
      if 'finish_at' in request.data:
        purpose.finish_at = timezone.now()
        purpose.save() 
      else:
        return JsonResponse({
          'success': False,
          'message': 'Purpose is started'
        }, status=423)
    else:
      return JsonResponse({
        'success': False,
        'message': 'Purpose is finished'
      }, status=423)

    return JsonResponse({'success': True}) 
  
  @method_decorator(login_required)
  def delete(self, request: HttpRequest, id: int):
    purpose = get_object_or_404(Purpose, pk=id)

    if not request.user.id == purpose.owner.id:
      return forbidden_response

    purpose.delete()
    
    return JsonResponse({'success': True}) 


class ObjectiveAPI(APIView):
  @method_decorator(login_required)
  def get(self, request: HttpRequest, id=None):
    objective = get_object_or_404(Objective, pk=id) if id else None

    if not objective:
      return JsonResponse({'message': 'Id required'}, status=404)
    
    return JsonResponse(ObjectiveSerializer(objective).data, safe=False)

  @method_decorator(login_required)
  def post(self, request: HttpRequest):
    if not 'purpose_id' in request.data:
      return not_valid_response

    purpose = Purpose.objects.filter(pk=request.data['purpose_id'], start_at__isnull=True).first()


    if not purpose:
      return JsonResponse({
        'success': False,
        'message': 'No such purpose or purpose is started'
      }, status=423)

    if not request.user.id == purpose.owner.id:
      return forbidden_response

    raw_objective = ObjectiveSerializer(data=request.data)
    
    if not raw_objective.is_valid():
      return not_valid_response  
    
    objective = raw_objective.save()

    return JsonResponse({'success': True, 'id': objective.id}) 
  
  @method_decorator(login_required)
  def patch(self, request: HttpRequest, id: int):
    objective = get_object_or_404(Objective, pk=id)

    if not request.user.id == objective.owner.id:
      return forbidden_response

    if objective.purpose.status != 'draft':
      return JsonResponse({
        'success': False,
        'message': 'Purpose is started'
      }, status=423)

    if 'purpose_id' in request.data:
      del request.data['purpose_id']
    raw_objective = ObjectiveSerializer(instance=objective, data=request.data, partial=True)
    if not raw_objective.is_valid():
      return not_valid_response  
    
    raw_objective.save()

    return JsonResponse({'success': True}) 
  
  @method_decorator(login_required)
  def delete(self, request: HttpRequest, id: int):
    objective = get_object_or_404(Objective, pk=id)

    if not request.user.id == objective.owner.id:
      return forbidden_response

    if objective.purpose.status != 'draft':
      return JsonResponse({
        'success': False,
        'message': 'Purpose is started'
      }, status=423)

    objective.delete()
    
    return JsonResponse({'success': True}) 



@require_http_methods(['GET'])
@login_required
def key_results_types(request: HttpRequest) -> JsonResponse:
 return JsonResponse(KeyResultTypeSerializer(KeyResultType.objects.all(), many=True).data, safe=False)

class KeyResultAPI(APIView):
  def get(self, request: HttpRequest):
    return JsonResponse(KeyResultSerializer(KeyResult.objects.filter(
      Q(owner_id=request.user.id) |
      Q(objective_id__in=itertools.chain(*[[o.id for o in p.objectives.all()] for p in request.user.purposes.all()]))
    ).all(), many=True).data, safe=False)

  def post(self, request):
    if not 'objective_id' in request.data:
      return not_valid_response

    objective = get_object_or_404(Objective, pk=request.data['objective_id'])
    
    if not request.user.id == objective.owner.id:
      return forbidden_response

    if objective.purpose.status != 'draft':
      return JsonResponse({
        'success': False,
        'message': 'Purpose is started'
      }, status=423)

    if objective.purpose.context.type == 'personal':
      for prop in ['owner_id']:
        request.data.pop(prop, None)

    if 'current_value' in request.data:
      del request.data['current_value']

    raw_key_result = KeyResultSerializer(data=request.data)
    
    if not raw_key_result.is_valid():
      return not_valid_response  
    
    key_result = raw_key_result.save()
    if not key_result.owner:
      key_result.owner = key_result.creator
      key_result.save()

    return JsonResponse({'success': True, 'id': key_result.id}) 

  def patch(self, request: HttpRequest, id: int):
    key_result = get_object_or_404(KeyResult, pk=id)

    if not request.user.id == key_result.creator.id:
      return forbidden_response

    req_data = request.data
    if key_result.purpose.status != 'draft':
      req_data = {'current_value': request.data['current_value']} if 'current_value' in request.data else {}

    if key_result.purpose.context.type == 'personal':
      for prop in ['owner_id']:
        request.data.pop(prop, None)

    for prop in ['objective', 'objective_id']:
      if prop in req_data:
        del req_data[prop]
      
    raw_key_result = KeyResultSerializer(instance=key_result, data=req_data, partial=True)
    if not raw_key_result.is_valid():
      return not_valid_response  
    
    raw_key_result.save()
    
    """
      If user try to update type to yes/no, delete owner and interval
    """
    new_type = KeyResultType.objects.filter(pk=req_data.get('type_id', None)).first()
    if new_type and new_type.name.lower() == 'yes/no':
      key_result.owner = None
      key_result.interval = None
      
      key_result.save()

    return JsonResponse({'success': True}) 

  @method_decorator(login_required)
  def delete(self, request: HttpRequest, id: int):
    key_result = get_object_or_404(KeyResult, pk=id)

    if not request.user.id == key_result.creator.id:
      return forbidden_response

    if key_result.objective.purpose.status != 'draft':
      return JsonResponse({
        'success': False,
        'message': 'Purpose is started'
      }, status=423)

    key_result.delete()
    
    return JsonResponse({'success': True}) 