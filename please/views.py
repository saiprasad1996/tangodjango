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
    elif request.method == 'PUT':
        body = request.body.decode('utf-8')
        auth = request.META['HTTP_AUTH']
        response = json.dumps({"request_type":'PUT','body':body,'header_auth':auth})
        return HttpResponse(response)
    elif request.method == 'PATCH':
        body = request.body.decode('utf-8')
        response = json.dumps({"request_type":'PATCH','body':body})
        return HttpResponse(response)
    elif request.method == 'DELETE':
        body = request.body.decode('utf-8')
        response = json.dumps({"request_type":'DELETE','body':body})
        return HttpResponse(response)
    else:
        return HttpResponse(json.dumps({"request_type":request.method,'body':request.body.decode('utf-8')}))

