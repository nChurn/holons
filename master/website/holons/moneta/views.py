import logging
import json
from purpose.models import Context
from moneta.models import FixedCost, VariableCost, CostTag
from moneta.serializers import FixedCostSerializer, CostTagSerializer, VariableCostSerializer

from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from email_api.helpers import request_helper
from email_api.helpers import auth_helper

import moneta.payment_systems_supported_countries as payment_systems_supported_countries
import moneta.payment_systems_accounts_models as payment_systems_accounts_models

not_valid_response = JsonResponse({
  'success': False,
  'message': 'Data is not valid'
}, status=400)

def moneta_index(request: HttpRequest) -> JsonResponse:
    """
    :return:
    """

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    data = {}

    return JsonResponse({
        'result': 'OK',
        'method': method,
        'data': data,
    })


PAYMENT_SYSTEMS = ['Stripe', 'Paysend']
def create_ps_account(ps, user, **kwargs):
    user_payment_account = getattr(payment_systems_accounts_models, ps + 'Account')(user=user, **kwargs)
    user_payment_account.save()

    return user_payment_account

@require_http_methods(['GET', 'PATCH'])
@login_required
def withdraw(request: HttpRequest) -> JsonResponse:
    user_payment_account = None
    payment_system = None
    for ps in PAYMENT_SYSTEMS:
        if request.user.country in getattr(payment_systems_supported_countries, ps):
            payment_system = ps

            user_payment_account = getattr(request.user, f'{ps.lower()}_account', None)

            if not user_payment_account:
                user_payment_account = create_ps_account(ps, request.user)
                
            break
    if request.method == 'PATCH':
        request_data = json.loads(request.body)
        for prop in request_data:
            if hasattr(user_payment_account, prop):
                setattr(user_payment_account, prop, request_data[prop])

            user_payment_account.save()

        return JsonResponse({'success': True})
    elif request.method == 'GET':
        account_info = { 'id': user_payment_account.id }
        for field in user_payment_account.__class__._meta.get_fields():
            if not field.name in ['id', 'user', 'user_id']:
                account_info[field.name] = getattr(user_payment_account, field.name)

        return JsonResponse({
            'success': True, 
            'account': {
                'payment_system': payment_system, 
                **account_info
                # addon information about account here
            }
        } if payment_system else {'success': False, 'message': 'There arent\'t any payment systems in your country'})

@require_http_methods(['GET'])
@login_required
def costs(request: HttpRequest) -> JsonResponse:
    

    return JsonResponse(safe=False)

class CostTagApi(APIView):
    @method_decorator(login_required)
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse(CostTagSerializer(
            CostTag.objects.filter(
                Q(owner_id=request.user.id) | 
                Q(context__in=Context.objects.filter(
                    Q(user_handle=request.user.id) | 
                    Q(entity__in=[e.id for e in request.user.entities.all()])
                ).all())
            ), 
            many=True
        ).data, safe=False)
    
    def post(self, request: HttpRequest) -> JsonResponse:
        request.data['owner_id'] = str(request.user.id)
        
        raw_tag = CostTagSerializer(data=request.data)
        if not raw_tag.is_valid(): 
            return not_valid_response

        tag = raw_tag.save()

        return JsonResponse({'success': True, 'id': tag.id})

class FixedCostApi(APIView):
    @method_decorator(login_required)
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse(FixedCostSerializer(
            FixedCost.objects.filter(
                Q(owner_id=request.user.id) | 
                Q(context__in=Context.objects.filter(
                    Q(user_handle=request.user.id) | 
                    Q(entity__in=[e.id for e in request.user.entities.all()])
                ).all())
            ),
            many=True
        ).data, safe=False)
    
    @method_decorator(login_required)
    def post(self, request: HttpRequest) -> JsonResponse:
        request.data['owner_id'] = str(request.user.id)

        raw_fixed_cost = FixedCostSerializer(data=request.data)
        if not raw_fixed_cost.is_valid():
            return not_valid_response

        fixed_cost = raw_fixed_cost.save()

        fixed_cost.tags.set(CostTag.objects.filter(id__in=request.data.get('tags', [])).all())

        return JsonResponse({'success': True, 'id': fixed_cost.id})
    
    @method_decorator(login_required)
    def patch(self, request: HttpRequest, id: int) -> JsonResponse:
        fixed_cost = get_object_or_404(FixedCost, pk=id)

        if request.data.get('finish', False):
            if fixed_cost.finished_at:
                return JsonResponse({'success': False, 'message': 'This fixed cost is finished'}, status=409)
            fixed_cost.finished_at = timezone.now()
            fixed_cost.save()
        else:
            for prop in ['owner', 'owner_id', 'started_at', 'context', 'context_id']:
                request.data.pop(prop, None)

            raw_fixed_cost = FixedCostSerializer(instance=fixed_cost, data=request.data, partial=True)
            if not raw_fixed_cost.is_valid():
                return not_valid_response
            
            if 'tags' in request.data:
                fixed_cost.tags.set(CostTag.objects.filter(id__in=request.data['tags']).all())

            raw_fixed_cost.save()

        return JsonResponse({'success': True})

    @method_decorator(login_required)
    def delete(self, request: HttpRequest, id: int) -> JsonResponse:
        get_object_or_404(FixedCost, pk=id).delete()

        return JsonResponse({'success': True})

class VariableCostApi(APIView):
    @method_decorator(login_required)
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse(VariableCostSerializer(
            VariableCost.objects.filter(
                Q(owner_id=request.user.id) | 
                Q(context__in=Context.objects.filter(
                    Q(user_handle=request.user.id) | 
                    Q(entity__in=[e.id for e in request.user.entities.all()])
                ).all())
            ),
            many=True
        ).data, safe=False)
    
    @method_decorator(login_required)
    def post(self, request: HttpRequest) -> JsonResponse:
        request.data['owner_id'] = str(request.user.id)

        raw_variable_cost = VariableCostSerializer(data=request.data)
        if not raw_variable_cost.is_valid():
            return not_valid_response

        variable_cost = raw_variable_cost.save()

        variable_cost.tags.set(CostTag.objects.filter(id__in=request.data.get('tags', [])).all())

        return JsonResponse({'success': True, 'id': variable_cost.id})
    
    @method_decorator(login_required)
    def patch(self, request: HttpRequest, id: int) -> JsonResponse:
        variable_cost = get_object_or_404(VariableCost, pk=id)

        for prop in ['owner', 'owner_id', 'context', 'context_id']:
            request.data.pop(prop, None)

        raw_variable_cost = VariableCostSerializer(instance=variable_cost, data=request.data, partial=True)
        if not raw_variable_cost.is_valid():
            return not_valid_response
        
        if 'tags' in request.data:
            variable_cost.tags.set(CostTag.objects.filter(id__in=request.data['tags']).all())

        raw_variable_cost.save()

        return JsonResponse({'success': True})

    @method_decorator(login_required)
    def delete(self, request: HttpRequest, id: int) -> JsonResponse:
        get_object_or_404(VariableCost, pk=id).delete()

        return JsonResponse({'success': True})