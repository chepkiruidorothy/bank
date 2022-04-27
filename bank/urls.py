"""bank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from branch import views
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),
    path('accounts/create/',views.create,name='create'),
    path('accounts/delete/<int:pk>',views.delete,name='delete'),
    path('accounts/withdraw/<int:pk>/',views.withdraw,name='withdraw'),
    path('accounts/statement/<int:pk>/',views.statement,name='statement'),
    path('accounts/loan_statement/<int:pk>/',views.loan_statement,name='loan_statement'),
    path('accounts/deposit/<int:pk>/',views.deposit,name='deposit'),
    path('loans/loan/<int:pk>/', views.request_loan, name='loan'),
    path('accounts/', include('allauth.urls')),
]
