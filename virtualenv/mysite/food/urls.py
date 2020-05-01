from django.urls import path
from . import views

urlpatterns = [
    path('food', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('update', views.background_view, name='background_view'),
    path('contact', views.contact, name='contact'),
    path('', views.home_page, name='home_page')
]