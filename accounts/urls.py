from . import views
from django.urls import path


urlpatterns = [
    path('User', views.BookingListView.as_view(), name='home')
]