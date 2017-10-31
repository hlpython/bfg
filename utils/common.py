from .tool_fun import *

def user_is_login(request):
    return get_session(request, 'username')
