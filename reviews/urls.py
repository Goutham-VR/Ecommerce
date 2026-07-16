from django.urls import path
from reviews import views

app_name = "reviews"

urlpatterns = [

    path('addreview/<slug:slug>/',views.addreview,name='addreview'),

]