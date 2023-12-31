"""
URL configuration for teleHealthCare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include #include 추가한거임


urlpatterns = [
    path('admin/', admin.site.urls), #기본 설정
    path('',include('patients.urls')), #patients app의 urls.py를 include한 것임
    path('',include('doctors.urls')), #patients app의 urls.py를 include한 것임
    path('',include('treatments.urls')) #treatments app의 urls.py를 include한 것임
]
