from django.urls import path
from .views import ReservationsView

urlpatterns = [
    path('<int:post_id>/',  ReservationsView.as_view(),
         name='createReservation'),
    path('<int:post_id>/<int:reservation_id>',
         ReservationsView.as_view(), name='getReservation'),
    path('<int:post_id>/<int:reservation_id>',
         ReservationsView.as_view(), name='updateReservation'),
    path('<int:post_id>/<int:reservation_id>',
         ReservationsView.as_view(), name='deleteReservations'),
]
