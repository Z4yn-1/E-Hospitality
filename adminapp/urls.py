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
    path('',views.Index,name='adminindex'),
    path('doctors/',views.DoctorList,name='doctors'),
    path('approved/<int:doctor_id>/',views.approve_doctor,name='approved'),
    path('doctorslist/',views.DoctorsAllView,name='doctorslist'),
    path('department/',views.Specialization,name='department'),
    path('users/',views.UsersView,name='users'),
    path('logout/',views.LogoutPage,name='logout'),
    path('availabe/<int:doc_id>/',views.Availability,name='available'),
    path('docdelete/<int:doc_id>/',views.DocDelete,name='docdelete'),
    path('userdelete/<int:user_id>/',views.UserDelete,name='userdelete')
]
