from accounts.models import MyUser

def pending_doctors(request):
    if request.session.get('role') == 'admin':
        pending_count = MyUser.objects.filter(role='doctor', is_approved=False).count()
        return {'pending_count': pending_count}
    return {}