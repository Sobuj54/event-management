from django.urls import path
from event.views import event_list, event_create, event_update, event_delete

app_name = "event"

urlpatterns = [
    path("list/", event_list, name="list"),
    path('create/', event_create, name='create'),
    path('edit/<int:pk>/', event_update, name='update'),
    path('delete/<int:pk>/', event_delete, name='delete'),
]
