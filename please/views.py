from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SlackAskUs,Log
# Create your views here.

def json_response(obj):
    '''

    :param obj: Dictionary
    :return:    HttpResponse
    '''
    response = HttpResponse(json.dumps(obj))
    response['Content-Type'] = 'application/json'
    response["Access-Control-Allow-Origin"] = "*"
    return response

@csrf_exempt
def pleaseInfo(request):
    if(request.method == 'GET'):
        return HttpResponse("This is a get request");
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

@csrf_exempt
def postquestion(request):
    if request.method == "GET":
        return HttpResponse("Your questions down here")
    elif request.method =="POST":
        try : 
            log = Log(logtext=str(request))
            log.save(force_insert=True)
            token=request.POST["token"]
            team_id=request.POST["team_id"]
            team_domain=request.POST["team_domain"]
            enterprise_id=request.POST["enterprise_id"]
            enterprise_name=request.POST["enterprise_name"]
            channel_id=request.POST["channel_id"]
            channel_name=request.POST["channel_name"]
            user_id=request.POST["user_id"]
            user_name=request.POST["user_name"]
            command=request.POST["command"]
            text=request.POST["text"]
            response_url=request.POST["response_url"]
            trigger_id=request.POST["trigger_id"]
            new_data = SlackAskUs(token=token,
                                    team_id=team_id,
                                    team_domain=team_domain,
                                    enterprise_id=enterprise_id,
                                    enterprise_name=enterprise_name,
                                    channel_id=channel_id,
                                    channel_name=channel_name,
                                    user_id=user_id,
                                    user_name=user_name,
                                    command=command,
                                    text=text,
                                    response_url=response_url,
                                    trigger_id=trigger_id)
            new_data.save()
            response = {
                "text": "Ok! Thats a great question.. We'll get back to you soon!",
                "attachments": [
                    {
                        "text":"Thinking.. Thinking..."
                    }
                ]
            }
            return json_response(json.dumps(response))
        except Exception:
            return json_response({
            "response_type": "ephemeral",
            "text": "Oops! I think there is some issue with this command. Please check back later"
            })