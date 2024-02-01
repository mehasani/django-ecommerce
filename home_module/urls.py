from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('latest-product',views.LatestProductsApiView.as_view()),
    path('about-us', views.AboutView.as_view(), name='about_page')

]