import logging
from django.conf import settings
from .models.ray_source import RaySource
from accounts.models import User
from helpers.data_helper import duplicate_object


RAYS_SOURCE = settings.RAYS_SOURCE


def set_default_rays(user):
    # if user has no rays (except ALL ray), copy them from talant
    if len(user.rays.all()) < 2:
      ray_source_user = User.objects.get(username__exact=RAYS_SOURCE)
      logging.info(f'get defaults from {ray_source_user}')
      logging.info(f'set defaults for {user}')
      for ray in ray_source_user.rays.exclude(title='ALL').all():
          ray_to_copy = duplicate_object(ray)
          user.rays.add(ray)
        
