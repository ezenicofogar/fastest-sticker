from django.urls import path
from . import views

app_name = 'content'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('images/', views.FullsetView.as_view(), name='all'),
    path('batch/<int:pk>/', views.QueryGroupDetailView.as_view(), name='qgdetail'),
    path('batch/<int:pk>/add/', views.QueryGroupAddImageView.as_view(), name='qgaddimage'),
    path('batch/<int:pk>/printed/', views.QueryGroupPrintedView.as_view(), name='qgprinted'),
    path('batch/', views.QueryGroupListView.as_view(), name='qglist'),
    path('batch/new/', views.QueryGroupNewView.as_view(), name='qgnew'),
]

