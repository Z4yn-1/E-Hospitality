from django.shortcuts import render,redirect
from .models import MyUser
from django.contrib import messages
from django.contrib.auth.hashers import check_password

# Create your views here.

def Register(request):
    if request.method == 'POST':
        name = request.POST.get('name','').strip()
        email = request.POST.get('email','').strip().lower()
        password = request.POST.get('password', '')
        cpassword = request.POST.get('cpassword', '')
        role = request.POST.get('role', '').strip().lower()
        specialization = request.POST.get('specialization') if role == "doctor" else None
        fees = request.POST.get('fees') if role == "doctor" else None
        
        if password != cpassword:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'account/register.html', {'formdata': request.POST})
        
        if role == "doctor" and not specialization:
            messages.error(request, 'Please select a specialization for doctor.')
            return render(request, 'account/register.html', {'formdata': request.POST})

        if role not in dict(MyUser.ROLE_CHOICES):
            messages.error(request, 'Please choose a valid role.')
            return render(request, 'account/register.html', {'formdata': request.POST})

        if MyUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'account/register.html', {'formdata': request.POST})
        
        MyUser.objects.create(
            name = name,
            email = email,
            password = password,
            role = role,
            specialization = specialization,
            is_approved=(False if role == "doctor" else True),
            fees = fees,
        )
        
        if role == "doctor":
            messages.success(request, 'Doctor account created. Waiting for admin approval.')
        else:
            messages.success(request, 'Account Created Successfully! please Login')

        return redirect('login')
    return render(request,'account/register.html')

def Login(request):
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        password = request.POST.get('password', '')

        try:
            user = MyUser.objects.get(name=name)
        except MyUser.DoesNotExist:
            messages.error(request, 'User not found')
            return render(request, 'account/login.html')
        
        if user.role == "doctor" and not user.is_approved:
            messages.error(request, "Your account is pending approval by admin.")
            return render(request, 'account/login.html')
        
        if user.password == password:
            request.session['user_id'] = user.id
            request.session['name'] = user.name
            request.session['role'] = user.role
            
            if user.role == 'admin':
                request.session['admin_id'] = user.id  
                
            if user.role == 'patient':
                request.session['patient_id'] = user.id
                
            if user.role == 'doctor':
                request.session['doctor_id'] = user.id

            messages.success(request, f'Welcome {user.name}!')

            if user.role == 'admin':
                return redirect('adminview/')
            elif user.role == 'doctor':
                return redirect('doctor/')
            elif user.role == 'patient':
                return redirect('patient/')
            else:
                return redirect('login')
        else:
            messages.error(request, 'Invalid password')
            return render(request, 'account/login.html')
    return render(request,'account/login.html')