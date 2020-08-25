from django.urls import path
from . import views
app_name = "common"

urlpatterns = [
    path("list", view.list_rooms)
]
