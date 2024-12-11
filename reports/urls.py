from django.urls import path
from .views import home
urlpatterns = [
   path('report_1' , home , name='report_1')
]