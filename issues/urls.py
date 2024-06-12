from django.urls import path
from .views import BoardView, StatusUpdateView


urlpatterns = [
    path("", BoardView.as_view(), name="board"),
    path("edit/status/<int:pk>/", StatusUpdateView.as_view(), name="update_status")
]