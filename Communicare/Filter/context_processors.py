def user_authenticated(request):
    if request.user.is_authenticated:
        me=request.user
    else:
        me=None
    return {'me':me}