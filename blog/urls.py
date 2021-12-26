from django.conf.urls import url
from . import views
from django.urls import path
app_name='blog'

urlpatterns = [
    path('',views.post_list,name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<post>/',views.post_detail,name='post_detail'),
    path('<post_id>/share/',views.post_share,name='post_share')
]
  