from django.urls import path
from . import views

from product.views import product_img_lst
# from influencer_img.views import ImgView

urlpatterns = [
  # path('', views.index, name = 'index'),
  # path('', ImgView.as_view()),
  path('', views.product_img_lst, name = 'product_img_lst'),
]