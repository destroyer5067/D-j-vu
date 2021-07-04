
from django.contrib import admin
from django.urls import path
from . import views

admin.site.site_header="Deja-Vu Admin Login"
admin.site.site_title="Deja-Vu Admin"
admin.site.index_title="Welcome to Admin Page"

urlpatterns = [
    path('', views.home , name='dejavu-home'),
    path('about/',views.about , name= 'dejavu-about'),
    path('take',views.index , name= 'index'),
    path('hpd',views.index2,name="index2"),
    path('hpd2',views.index3,name="index3"),
    
]