"""
URL configuration for e_hospitality project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',views.Index,name='patientindex'),
    path('doclist/',views.DoctorDetails,name='doclist'),
    path('book/<int:doc_id>',views.AppoinmentBook,name='book'),
    path('history/',views.BookHistory,name='history'),
    path('cancel/<int:app_id>/',views.Cancel_appoinment,name='cancel'),
    path('update/<int:app_id>/',views.Update_Appointment,name='update'),
    path('plogout/',views.LogoutPage,name='plogout'),
    path('docdept/',views.DepartmentView,name='docdept'),
    path('contact/',views.ContactPage,name='contact'),
    path('checkout/<int:app_id>/',views.CheckoutView,name='checkout'),
    
    
    path('create-session/<int:app_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.stripe_success, name='stripe_success'),
    path('cancel/', views.stripe_cancel, name='stripe_cancel'),
]
