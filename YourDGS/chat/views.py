from django.shortcuts import render
from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.shortcuts import Http404
from.models import Stock


# Create your views here.
class ThreadView(View):
    template_name = 'chat/chat.html'
    def get(self, request, **kwargs):

        stock=Stock.objects.all().order_by('id')[50:]
        return render(request, self.template_name,{'stock':stock})