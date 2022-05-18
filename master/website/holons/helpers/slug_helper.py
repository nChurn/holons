import logging

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import Http404

from accounts.models import User
from rays.models import RayCanned
from accounts.profile_public import user_profile
from rays.routes_automation import show as show_ray_canned


def view_by_slug(request: HttpRequest, slug: str) -> HttpResponse:
    """Generate redirect based on what Model the slug is for
    :param slug: slug string
    :return: redirect
    """
    
    slug_type = get_slug_type(slug)
    if 'profile' == slug_type:
      return user_profile(request, handle=slug)
    if 'ray_canned' == slug_type:
      return show_ray_canned(request, slug=slug)
    raise Http404("No such page")


def get_slug_type(slug: str) -> str:
    """Get model type by it's slug
    :return: model type
    """

    slug_profile = User.objects.filter(handle=slug).first()
    if slug_profile:
      return 'profile'
    slug_ray_canned = RayCanned.objects.filter(slug=slug).first()
    if slug_ray_canned:
      return 'ray_canned'

