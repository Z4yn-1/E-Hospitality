from accounts.models import MyUser
from patientapp.models import Appointment

def pending_count(request):
    count = 0
    if request.session.get('role') == 'doctor' and request.session.get('doctor_id'):
        doctor_id = request.session['doctor_id']
        count = Appointment.objects.filter(doctor_id=doctor_id,is_seen=False).count()
    return {'pending_count': count}