from django.shortcuts import render,redirect
from accounts.models import MyUser
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator

# Create your views here.

def Index(request):
    if request.session.get('role') != 'admin':
        return redirect('login')
    
    admin = None
    if request.session.get('admin_id'):
        admin = MyUser.objects.get(id=request.session['admin_id'])
    return render(request,'ADMINT/index.html',{'admin':admin})

def DoctorList(request):
    if request.session.get('role') != 'admin':
        return redirect('login')

    admin = None
    if request.session.get('admin_id'):
        admin = MyUser.objects.get(id=request.session['admin_id'])
        
    doctors = MyUser.objects.filter(role='doctor',is_approved=False)
    return render(request,'ADMINT/doctors.html',{'doctors':doctors,'admin':admin})


def approve_doctor(request, doctor_id):
    if request.session.get('role') != 'admin':
        return redirect('login')

    doctor = MyUser.objects.get(id=doctor_id, role='doctor')
    doctor.is_approved = True
    doctor.save()
    messages.success(request, f'Doctor {doctor.name} has been approved.')
    return redirect('doctors')

def DoctorsAllView(request):
    if request.session.get('role') != 'admin':
        return redirect('login')

    admin = None
    if request.session.get('admin_id'):
        admin = MyUser.objects.get(id=request.session['admin_id'])
        
    doctors = MyUser.objects.filter(role='doctor')
        
    paginator = Paginator(doctors, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request,'ADMINT/doctorslist.html',{'doctors':doctors,'admin':admin,'page_obj':page_obj})

def Specialization(request):
    if request.session.get('role') != 'admin':
        return redirect('login')
    specializations = MyUser.objects.filter(role='doctor') \
                                    .values('specialization') \
                                    .annotate(count=Count('id'))
    
    admin = None
    if request.session.get('admin_id'):
        admin = MyUser.objects.get(id=request.session['admin_id'])
                                       
    pending_count = MyUser.objects.filter(role='doctor', is_approved=False).count()
    context = {'specializations':specializations,'pending_count':pending_count,'admin':admin}
    return render(request,'ADMINT/department.html',context) 
    
def UsersView(request):
    if request.session.get('role') != 'admin':
        return redirect('login')
    
    admin = None
    if request.session.get('admin_id'):
        admin = MyUser.objects.get(id=request.session['admin_id'])
        
    user = MyUser.objects.filter(role='patient')
        
    paginator = Paginator(user, 5) 
    page_number = request.GET.get('page')   
    page_obj = paginator.get_page(page_number)
        
    return render(request,'ADMINT/userdetails.html',{'user':user,'admin':admin,'page_obj':page_obj})

def LogoutPage(request):
    request.session.flush()
    return redirect('login')

def Availability(request,doc_id):
    if request.session.get('role') != 'admin':
        return redirect('login')
    
    doctor = MyUser.objects.get(id=doc_id, role='doctor')
    doctor.is_available = not doctor.is_available  
    doctor.save()

    messages.success(request, f"{doctor.name}'s availability updated.")
    return redirect('doctorslist')

def DocDelete(request,doc_id):
    if request.session.get('role') != 'admin':
        return redirect('login') 
    
    doctor = MyUser.objects.filter(id=doc_id,role='doctor',is_approved=False)
    if doctor.exists():
        doctor.delete()
    return redirect('doctorslist')

def UserDelete(request,user_id):
    if request.session.get('role') != 'admin':
        return redirect('login') 
    
    patient = MyUser.objects.filter(id=user_id,role='patient')
    if patient.exists():
        patient.delete()
    return redirect('users')
    


        
