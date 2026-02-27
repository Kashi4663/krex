def admin_status(request):
    return {
        'is_admin_user': request.user.is_authenticated and request.user.is_staff
    }