from django.http import HttpResponse

def index(request):
    return HttpResponse("Lazy Rest App of tangodjango!")
