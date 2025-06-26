from django.urls import path
from .views import DepartmentListView, DepartmentCreateView

urlpatterns = [
    path('', DepartmentListView.as_view(), name='department-list'),
    path('create/', DepartmentCreateView.as_view(), name='department-create'),
] 