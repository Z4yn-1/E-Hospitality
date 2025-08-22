from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import MyUser
from .models import *
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from django.urls import reverse
import stripe
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
# Create your views here.


def Index(request):
    if request.session.get('role') != 'patient':
        return redirect('login')
    
    patient = None
    if request.session.get('patient_id'):
        patient = MyUser.objects.get(id=request.session['patient_id'])
    return render(request,'patient/index.html',{'patient':patient})

def DoctorDetails(request):
    if request.session.get('role') != 'patient':
        return redirect('login')
    
    patient = None
    if request.session.get('patient_id'):
        patient = MyUser.objects.get(id=request.session['patient_id'])

        
    doctor = MyUser.objects.filter(role='doctor',is_approved=True)
    
    paginator = Paginator(doctor, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'patient':patient,'doctor':doctor,'page_obj':page_obj}
    return render(request,'patient/doctors.html',context)

def AppoinmentBook(request, doc_id):
    if request.session.get('role') != 'patient':
        return redirect('login')
    
    patient = None
    if request.session.get('patient_id'):
        patient = MyUser.objects.get(id=request.session['patient_id'])
        
    doctor = get_object_or_404(MyUser, id=doc_id, role='doctor', is_approved=True)
    
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')
        
        appointment = Appointment.objects.create(
            booked_by = patient,
            patient_name = patient_name,
            doctor = doctor,
            date = date,
            time = time,
            reason = reason
        )
        
        return redirect('checkout', app_id=appointment.id)
    
    context = {'doctor': doctor, 'patient': patient}
    return render(request, 'patient/appoinment.html', context)


def BookHistory(request):
    if request.session.get('role') != 'patient':
        return redirect('login')
    
    patient = None
    if request.session.get('patient_id'):
        patient = MyUser.objects.get(id=request.session['patient_id'])
        
        appoinments = Appointment.objects.filter(booked_by=patient).order_by('-date', '-time')
    return render(request,'patient/history.html',{'appoinments':appoinments,'patient':patient})


def Cancel_appoinment(request,app_id):
    if request.session.get('role') != 'patient':
        return redirect('login')
    
    patient = None
    if request.session.get('patient_id'):
        patient = MyUser.objects.get(id=request.session['patient_id'])
    
    appointment = Appointment.objects.get(id=app_id)
    if request.session.get('patient_id') != appointment.booked_by.id:
        return redirect('history')
    
    if request.method == 'POST':
        appointment.delete()
        return redirect('history')
    return render(request,'patient/cancel.html',{'appointment':appointment,'patient':patient})


def Update_Appointment(request,app_id):
    if request.session.get('role') != 'patient':
        return redirect('login')
    patient = None
    if request.session.get('patient_id'):
        patient = MyUser.objects.get(id=request.session['patient_id'])
    
    appointment = Appointment.objects.get(id=app_id)
    if request.session.get('patient_id') != appointment.booked_by.id:
        return redirect('history')
    
    
    if request.method == 'POST':
        appointment.patient_name = request.POST.get('patient_name')
        appointment.date = request.POST.get('date')
        appointment.time = request.POST.get('time')
        appointment.reason = request.POST.get('reason')
        appointment.save()
        return redirect('history')
    context = {'appointment':appointment,'doctor':appointment.doctor,'patient':patient}
    return render(request,'patient/update.html',context)


def LogoutPage(request):
    request.session.flush()
    return redirect('login')



def DepartmentView(request):
    if request.session.get('role') != 'patient':
        return redirect('login')
    
    departments = MyUser.objects.filter(role='doctor') \
                        .values('specialization') \
                        .annotate(count=Count('id'))
    
    patient = None
    if request.session.get('patient_id'):
        patient = MyUser.objects.get(id=request.session['patient_id'])
        
    pending_count = MyUser.objects.filter(role='doctor', is_approved=False).count()
    context = {'departments':departments,'pending_count':pending_count,'patient':patient}
    
    return render(request,'patient/departments.html',context)


def ContactPage(request):
    if request.session.get('role') != 'patient':
        return redirect('login')
    
    patient = None
    if request.session.get('patient_id'):
        patient = MyUser.objects.get(id=request.session['patient_id'])
    
    return render(request,'patient/contact.html',{'patient':patient})


stripe.api_key = settings.STRIPE_SECRET_KEY

def CheckoutView(request, app_id):
    if request.session.get('role') != 'patient':
        return redirect('login')
    
    patient = None
    if request.session.get('patient_id'):
        patient = MyUser.objects.get(id=request.session['patient_id'])

    appointment = get_object_or_404(Appointment, id=app_id)
    doctor = appointment.doctor  

    context = {
        'appointment': appointment,
        'doctor': doctor,
        'fees': doctor.fees,
        'patient': patient
    }
    return render(request, 'patient/checkout.html', context)


def create_checkout_session(request, app_id):
    """Create Stripe Checkout Session (card only)"""
    if request.session.get('role') != 'patient':
        return redirect('login')

    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid method.")

    appointment = get_object_or_404(Appointment, id=app_id)
    doctor = appointment.doctor

    if doctor.fees is None:
        return HttpResponseBadRequest("Doctor has no fee set.")

    # Convert doctor fees (e.g. 500.00) into paise (e.g. 50000)
    amount_in_paise = int((Decimal(doctor.fees).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) * 100))

    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],   # ✅ only card payments allowed
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "inr",
                "product_data": {
                    "name": f"Consultation with Dr. {doctor.name}",
                    "description": f"{doctor.specialization or 'Doctor'} – Appointment #{appointment.id}",
                },
                "unit_amount": amount_in_paise,
            },
            "quantity": 1,
        }],
        metadata={
            "appointment_id": str(appointment.id),
        },
        success_url=request.build_absolute_uri(reverse('stripe_success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('stripe_cancel')),
    )

    return redirect(session.url, code=303)


def stripe_success(request):
    """Mark appointment paid after successful payment"""
    session_id = request.GET.get("session_id")
    if not session_id:
        return redirect("patient_dashboard")

    session = stripe.checkout.Session.retrieve(session_id)
    appointment_id = session.get("metadata", {}).get("appointment_id")

    if session.payment_status == "paid" and appointment_id:
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.is_paid = True
        appointment.status = "Paid"
        appointment.save()

    return render(request, "patient/payment_success.html", {"appointment": appointment})


def stripe_cancel(request):
    return render(request, "patient/payment_cancel.html")

        

                    
    
    
        
    
        
    
        
        
    
    