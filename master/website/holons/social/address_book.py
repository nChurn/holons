import logging

from django.conf import settings

from django.http import HttpRequest
from django.http import JsonResponse


from accounts.models import User
from invitation.models import Token
from social.models import Graph


LOGIN_PARAMS = ('/auth', None)
RAY_SOURCES = settings.RAY_SOURCES

  
def update_social_graph(invitation_token: Token):
    """Add user's to the social models

    * Get parent user from Token
    * Get child user from Token
    * Attach parent user to the child.friends
    * Attach child user to the parents.social
    * Attach child user to the parents.friends
    * Attach parent user to the child.social

    :todo: this is unreadable... what can be done?
    """

    if not isinstance(invitation_token, Token):
      return

    parent_user = User.objects.filter(pk=invitation_token.issuer.first().id).first()
    child_user = User.objects.filter(pk=invitation_token.used_by.first().id).first()
    p_graph, created = Graph.objects.get_or_create(user_id=parent_user.id)
    c_graph, created = Graph.objects.get_or_create(user_id=child_user.id)
    c_graph.friends.add(p_graph)
    p_graph.user.add(child_user)
    parent_user.social.add(c_graph)
    p_graph.friends.add(c_graph)
    c_graph.user.add(parent_user)
    child_user.social.add(p_graph)
    

def get_address_book(user_id: int) -> dict:
    """Take user id, get their contacts, format contacts

    :todo: check and test for non-existant user behavior
    :returns: dict of user's contacts
    """

    user = User.objects.filter(pk=user_id).first()
    friends_list = []
    fixed_rays_users = User.objects.filter(handle__in=RAY_SOURCES)

    for item in user.social.all():
      for friend in item.friends.all():
        friend_data = friend.user.get()
        friends_list.append({
          'user_id': str(friend_data.id),
          'username': friend_data.username,
          'user_phone': friend_data.phone_number,
        })

    for fixed_user in fixed_rays_users:
        friends_list.append({
          'user_id': str(fixed_user.id),
          'username': fixed_user.username,
          'user_phone': '',
        })
    return friends_list
