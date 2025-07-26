from django.urls import path
from category.views import category_list, category_create, category_delete, category_update, CategoryListView

app_name = "category"

urlpatterns = [
    path("list/", CategoryListView.as_view(), name="list"),
    path('create/', category_create, name='create'),
    path('edit/<int:pk>/', category_update, name='update'),
    path('delete/<int:pk>/',category_delete, name='delete'),
]
