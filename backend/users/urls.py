from django.urls import path
from users.views import LogsViewSet


urlpatterns = [
    path('logs/', LogsViewSet.as_view(), name='logs'),
    path('logs/<int:pk>/', LogsViewSet.as_view(), name='log')
]

