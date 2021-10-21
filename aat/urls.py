from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registerPage,name="register"),
    path('login/', views.loginPage,name="login"),
    path('overview/', views.overview,name="overview"),
    path('logout/', views.logoutUser,name="logout"),
    path('', views.fileupload,name="fileupload"),
    path('metricSelection/', views.metricSelection,name="metricSelection"),
    path('graphs/', views.graphdisplay,name="graphs"),
    path('output/', views.outputPage,name="output"),
    path('about/', views.about,name="about"),
    path('optimization/', views.optimization,name="optimization"),
    path('gpstracking/', views.gpstracking,name="gpstracking"),
    path('trains/', views.trains,name="trains"),

   # path('', views.home,name="home"),
]
