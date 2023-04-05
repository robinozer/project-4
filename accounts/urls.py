from . import views
from django.urls import path


urlpatterns = [
    path('/', views.BookingListView.as_view(), name='home'),
    path('/create', views.BookingCreateView.as_view(), name='create_view'),
    path('/booking_edit/<id:id>', views.BookingUpdateView().as_view(), name='update_view'),
]
