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

from . import views
from django.urls import path

urlpatterns = [
    path('',views.Index,name='doctorindex'),
    path('appointmentview',views.AppiontmentView,name='appointmentview'),
    path('dlogout/',views.LogoutPage,name='dlogout'),
    path('cancelapp/<int:app_id>/',views.Cancel_appoinment,name='cancelapp'),
    path('docview/',views.DoctorDetails,name='docview'),
    path('department/',views.DepartmentView,name='department'),
]
