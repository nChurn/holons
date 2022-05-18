from django.http import HttpRequest


def method_name(request: HttpRequest) -> str:
    """
    :TODO: Get rid of this vintage piece of shit
    use decorators or request.method everywhere

    Helper to extract a method field from HttpRequest given
    :param request:
    :return:
    """

    method = 'unknown'
    if request.method == 'GET':
        method = 'get'
    elif request.method == 'POST':
        method = 'post'
    elif request.method == 'DELETE':
        method = 'delete'
    elif request.method == 'PATCH':
        method = 'patch'
    elif request.method == 'PUT':
        method = 'put'
    return method
