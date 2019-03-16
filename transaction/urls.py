from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('paper_submit/', views.paper_submit, name='paper_submit'),
    path('paper_submit/action', views.paper_submit_action, name='paper_submit_action'),
]

