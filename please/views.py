from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
@csrf_exempt
def pleaseInfo(request):
    if(request.method == 'GET'):
        return HttpResponse("This please is a get request");
    elif(request.method == 'POST'):
        try:
            meta_info = (request.META)

            body = str(request.body.decode('utf-8'))
            content = "";
            #content = "{}".format(meta_info)

            response = HttpResponse("", content_type="text/plain; charset=utf-8")
            response['custom-header']="Yo header"
            response.write(content)
            response.write("xzy")

            auth = meta_info["HTTP_AUTH"]
            response.write(auth)
            # if meta_info["HTTP_AUTH"] == "epsumlabs":
            #     response.write("Yeah authenticated ");
            return response
        except KeyError :
            return HttpResponse("UnAuthorized access detected",status = 403)
