from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import MyUser
from patientapp.models import Appointment
from django.core.paginator import Paginator
from django.db.models import Count

# Create your views here.

def Index(request):
    if request.session.get('role') != 'doctor':
        return redirect('login')
    
    doctor = None
    if request.session.get('doctor_id'):
        doctor = MyUser.objects.get(id=request.session['doctor_id'])
    return render(request,'doctor/index.html',{'doctor':doctor})

def AppiontmentView(request):
    if request.session.get('role') != 'doctor':
        return redirect('login')
    
    doctor = MyUser.objects.get(id=request.session['doctor_id'])
        
    appointments = Appointment.objects.filter(doctor=doctor).order_by("date", "time")
    appointments.filter(is_seen=False).update(is_seen=True)
    context = {'doctor':doctor,'appointments':appointments}
    return render(request,'doctor/appointmentview.html',context)

def LogoutPage(request):
    request.session.flush()
    return redirect('login')


def Cancel_appoinment(request, app_id):
    if request.session.get('role') != 'doctor':
        return redirect('login')
    
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('login')

    doctor = get_object_or_404(MyUser, id=doctor_id)
    appointment = get_object_or_404(Appointment, id=app_id)

    if appointment.doctor.id == doctor.id:
        appointment.delete()
    
    return redirect('appointmentview')


def DoctorDetails(request):
    if request.session.get('role') != 'doctor':
        return redirect('login')
    
    doctor = None
    if request.session.get('doctor_id'):
        doctor = MyUser.objects.get(id=request.session['doctor_id'])

        
    doctor = MyUser.objects.filter(role='doctor',is_approved=True)
    
    paginator = Paginator(doctor, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'doctor':doctor,'doctor':doctor,'page_obj':page_obj}
    return render(request,'doctor/doctorsview.html',context)


def DepartmentView(request):
    if request.session.get('role') != 'doctor':
        return redirect('login')
    
    departments = MyUser.objects.filter(role='doctor') \
                        .values('specialization') \
                        .annotate(count=Count('id'))
    
    doctor = None
    if request.session.get('doctor_id'):
        doctor = MyUser.objects.get(id=request.session['doctor_id'])
        
    pending_count = MyUser.objects.filter(role='doctor', is_approved=False).count()
    context = {'departments':departments,'pending_count':pending_count,'doctor':doctor}
    
    return render(request,'doctor/department.html',context)
    





