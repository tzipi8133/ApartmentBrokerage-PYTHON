from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.homePage, name="home"),
    path("login/", views.Login),
    path("register/", views.Register),
    path("add_apartment/", views.add_appartment, name="add_appartment"),  # שם הקישור עדכון
    path("seller_dashboard/", views.seller_dashboard, name="seller_dashboard"),
    path("apartments/", views.apartment_list, name="apartment_list"),
    path("request/<str:apartment_id>/", views.request_form, name="request_form"),
    path('update_status/', views.update_status, name='update_status'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
