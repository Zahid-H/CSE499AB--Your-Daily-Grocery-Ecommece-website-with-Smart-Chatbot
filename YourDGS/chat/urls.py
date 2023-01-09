from django.urls import path, include
from chat.views import ThreadView

urlpatterns = [
    path('', ThreadView.as_view(),name='chat'),
    path('<str:username>/', ThreadView.as_view(),name='chat')
]