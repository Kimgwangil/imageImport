from django.urls import path
from . import views

from influencer_img.views import influencer_img_lst
# from influencer_img.views import ImgView

urlpatterns = [
  # path('', views.index, name = 'index'),
  # path('', ImgView.as_view()),
  path('', views.influencer_img_lst, name = 'influencer_img_lst'),
]