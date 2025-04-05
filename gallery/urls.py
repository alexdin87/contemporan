from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('painting/<int:pk>/', views.painting_popup, name='painting_popup'),
    path('contact/', views.contact_view, name='contact'),
]

