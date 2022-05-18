import logging
from django.http import HttpRequest


def get_user(request: HttpRequest) -> str:
    """
    Helper to extract a user field from HttpRequest given
    :param request:
    :return:
    :todo: this wrapper is really obsolete, refactor the code and get rid of it
    """

    user = 'unknown'
    return request.user
