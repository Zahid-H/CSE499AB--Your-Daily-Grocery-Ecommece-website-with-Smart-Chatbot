
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.store,name='store'),
    path('store/<slug:category_slug>/', views.store,name='product_by_category'),
    path('store/<slug:category_slug>/<slug:subcategory_slug>/', views.store,name='product_by_subcategory'),
    path('store/<slug:category_slug>/<slug:subcategory_slug>/<str:product_id>/', views.product_detail, name='product_detail'),
    path('search/',views.search,name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

]