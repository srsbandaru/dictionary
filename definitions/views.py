from django.shortcuts import render
from django.views import View

# Create your views here.
class IndexView(View):
    template_name = "definitions/index.html"

    def get(self, request):
        return render(request, self.template_name)
    
    