from django.urls import path
from orders import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('test/<str:oid>/<str:pid>/', views.test, name='test'),

    #extra

    path('orderdone/', views.orderdone, name='orderdone'),
    path('ordernotdone/', views.ordernotdone, name='ordernotdone'),

]