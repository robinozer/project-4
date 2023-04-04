from . import views
from django.urls import path


urlpatterns = [
    path('', views.BookingListView.as_view(), name='home')
]