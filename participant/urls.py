from django.urls import path
from participant.views import participant_list, participant_create, participant_delete, participant_update

app_name = 'participant'

urlpatterns = [
    path('list/',participant_list, name='list'),
    path('create/', participant_create, name='create'),
    path('edit/<int:pk>/', participant_update, name='update'),
    path('delete/<int:pk>/', participant_delete, name='delete'),
]
