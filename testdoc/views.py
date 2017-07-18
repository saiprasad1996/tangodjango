from django.http import HttpResponse

# Create your views here.
def testdoc(request):
    return HttpResponse("Test Docs App of Tango django")
