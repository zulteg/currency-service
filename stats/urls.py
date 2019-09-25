from django.urls import path

from .views import IndexView, FilterView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('filter/', FilterView.as_view(), name='filter'),
]
