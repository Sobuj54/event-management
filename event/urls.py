from django.urls import path
from event.views import event_list, event_create, event_update, event_delete, EventListView, EventCreateView, EventUpdateView, EventDeleteView

app_name = "event"

urlpatterns = [
    path("list/", EventListView.as_view(), name="list"),
    path('create/', EventCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', EventUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', EventDeleteView.as_view(), name='delete'),
]
