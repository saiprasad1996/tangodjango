from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import json
from .models import SlackAskUs, Log, AuthenticatedSpaces, User
import datetime
import requests
from tangodjango import settings
from urllib.parse import urlencode


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
    if (request.method == 'GET'):
        return HttpResponse("This is a get request")
    elif (request.method == 'POST'):
        try:
            meta_info = (request.META)

            body = str(request.body.decode('utf-8'))
            content = ""
            # content = "{}".format(meta_info)

            response = HttpResponse("", content_type="text/plain; charset=utf-8")
            response['custom-header'] = "Yo header"
            response.write(content)
            response.write("xzy")

            auth = meta_info["HTTP_AUTH"]
            response.write(auth)
            # if meta_info["HTTP_AUTH"] == "epsumlabs":
            #     response.write("Yeah authenticated ");
            return response
        except KeyError:
            return HttpResponse("UnAuthorized access detected", status=403)
    elif request.method == 'PUT':
        body = request.body.decode('utf-8')
        auth = request.META['HTTP_AUTH']
        response = json.dumps({"request_type": 'PUT', 'body': body, 'header_auth': auth})
        return HttpResponse(response)
    elif request.method == 'PATCH':
        body = request.body.decode('utf-8')
        response = json.dumps({"request_type": 'PATCH', 'body': body})
        return HttpResponse(response)
    elif request.method == 'DELETE':
        body = request.body.decode('utf-8')
        response = json.dumps({"request_type": 'DELETE', 'body': body})
        return HttpResponse(response)
    else:
        return HttpResponse(json.dumps({"request_type": request.method, 'body': request.body.decode('utf-8')}))


@csrf_exempt
def postquestion(request):
    if request.method == "GET":
        return HttpResponse("Your questions down here")
    elif request.method == "POST":
        try:
            log = Log(logtext=str(request.POST), timestamp=datetime.datetime.now())
            log.save(force_insert=True)

            ##################

            # <QueryDict: {'token': ['sUoeDIGYKcWoVHC11tBnOx2Z'], 'team_id': ['TA2SX1M2B'], 'team_domain': ['techguidesczm'], 'channel_id': ['GAA12L3Q9'], 'channel_name': ['privategroup'], 'user_id': ['UAAD7BAA2'], 'user_name': ['friendship.sai1996'], 'command': ['/askus'], 'text': ['Ask me'], 'response_url': ['https://hooks.slack.com/commands/TA2SX1M2B/352279176883/nFzHrX81iWbl2C82HadxN4Yv'], 'trigger_id': ['351683324272.342915055079.3f3d64387f2c4b3e8a6310a704c404a9']}>
            #################
            token = request.POST["token"]
            team_id = request.POST["team_id"]
            team_domain = request.POST["team_domain"]
            # enterprise_id=request.POST["enterprise_id"]
            # enterprise_name=request.POST["enterprise_name"]
            channel_id = request.POST["channel_id"]
            channel_name = request.POST["channel_name"]
            user_id = request.POST["user_id"]
            user_name = request.POST["user_name"]
            command = request.POST["command"]
            text = request.POST["text"]
            response_url = request.POST["response_url"]
            trigger_id = request.POST["trigger_id"]
            new_data = SlackAskUs(token=token,
                                  team_id=team_id,
                                  team_domain=team_domain,
                                  channel_id=channel_id,
                                  channel_name=channel_name,
                                  user_id=user_id,
                                  user_name=user_name,
                                  command=command,
                                  text=text,
                                  response_url=response_url,
                                  trigger_id=trigger_id)
            new_data.save()
            #############################################
            log = Log(logtext=str(request.POST), timestamp=datetime.datetime.now())
            log.save(force_insert=True)
            # token = request.POST['token']
            # team_id = request.POST['team_id']
            # team_domain = request.POST["team_domain"]
            # channel_id = request.POST['channel_id']
            # user_name = request.POST['user_name']
            # state_params = token
            # user_id = request.POST['user_id']
            response = {}
            user = User.objects.filter(team_domain=team_domain, user_name_slack=user_name, state_params="created")
            print(user)
            if len(user) == 1:
                response = {
                    "text": "Ok! Thats a great question.. One of your community member will get back to you soon! ",
                    "attachments": [
                        {
                            "text": "Your question was posted to Collaborizm Community",
                        }
                    ]

                }

            else:
                user_new = User(user_name_slack=user_name,
                                slack_token=token,
                                access_token_fb='',
                                team_domain=team_domain,
                                team_id=team_id,
                                channel_id=channel_id,
                                user_name_czm='',
                                state_params=token)
                user_new.save()
            qstr_fb = urlencode({'state_params': token, "user_id": user_id, 'user_name': user_name, 'token': token,
                                 'team_domain': team_domain, "response_url": response_url})
            url_fb = "https://tangodjango.herokuapp.com/please/collab/fbauth?" + qstr_fb

            r = requests.post('https://hooks.slack.com/services/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', json={
                "text": "Question from {} Workspace".format(
                    "Techguides" if team_domain == "techguidesczm" else team_domain),
                "attachments": [{"text": str(text),
                                 "author_name": "Asked by {}".format(user_name)
                                 }, {
                                    "title": "See Question on Collaborizm here : ",
                                    "text": "https://www.collaborizm.com/thread/Hyq6_lp2M"
                                }]
            }, headers={"Content-Type": "application/json"})
            response_ = {
                "text": "Ok! Thats a great question.. One of your community member will get back to you soon! ",
                "attachments": [
                    {
                        "text": "To access the collaborizm community we need to authenticate your facebook as a security check…",
                        "callback_id": "login_option",
                        "color": "#3AA3E3",
                        "attachment_type": "default",
                        "actions": [
                            {
                                "name": "sign_in",
                                "text": "Sign In",
                                "type": "button",
                                "value": "signin",
                                "url": url_fb
                            },
                            {
                                "name": "sign_in",
                                "text": "Sign Up",
                                "type": "button",
                                "value": "signup",
                                "url": "https://www.collaborizm.com/login"
                            },
                            {
                                "name": "sign_in",
                                "text": "Nope Thanks",
                                "style": "danger",
                                "type": "button",
                                "value": "nope",
                                "confirm": {
                                    "title": "Are you sure?",
                                    "text": "Signing Into collaborizm would post the question to the community from right here",
                                    "ok_text": "Yes",
                                    "dismiss_text": "No"
                                }
                            }
                        ]
                    }
                ]
            } if len(user) == 0 else response

            return json_response(response_)
        except MultiValueDictKeyError:
            return json_response({
                "response_type": "ephemeral",
                "text": "Oops! I think there is some issue with this command. Please check back later"
            })


def showQuestions(request):
    try:
        questions = SlackAskUs.objects.all()
        return render(request, 'please/questions.html', {'questions': questions})
    except Exception:
        return json_response({"message": "Something went wrong"})


def auth(request):
    return render(request, 'please/slack_add.html')


def collab_redirect(request):
    try:
        payload = {"client_id": settings.CREDS['client_id'], "client_secret": settings.CREDS['client_secret'],
                   "redirect_uri": "https://tangodjango.herokuapp.com/please/collab/auth/redirect"}
        r = requests.get('https://slack.com/api/oauth.access?code=' + request.GET["code"], params=payload)
        json_r = json.loads(r.text)
        space = AuthenticatedSpaces(access_token=json_r["access_token"],
                                    scope=json_r["scope"],
                                    user_id=json_r["user_id"],
                                    team_name=json_r["team_name"],
                                    team_id=json_r["team_id"],
                                    incoming_webhook_channel=json_r["incoming_webhook"]["channel"],
                                    incoming_webhook_channel_id=json_r["incoming_webhook"]["channel_id"],
                                    incoming_webhook_configuration_url=json_r["incoming_webhook"]["configuration_url"],
                                    incoming_webhook_url=json_r["incoming_webhook"]["url"],
                                    bot_user_id=json_r["bot"]["bot_user_id"],
                                    bot_access_token=json_r["bot"]["bot_access_token"])
        space.save()
        log = Log(logtext=str(r.text), timestamp=datetime.datetime.now())
        log.save(force_insert=True)

        return HttpResponse("Success!")
    except Exception:

        return HttpResponse("Error encountered")


@csrf_exempt
def collab_broadcast(request):
    try:
        space = AuthenticatedSpaces.objects.all()
        token = request.POST["token"]
        team_id = request.POST["team_id"]
        team_domain = request.POST["team_domain"]
        # enterprise_id=request.POST["enterprise_id"]
        # enterprise_name=request.POST["enterprise_name"]
        channel_id = request.POST["channel_id"]
        channel_name = request.POST["channel_name"]
        user_id = request.POST["user_id"]
        user_name = request.POST["user_name"]
        command = request.POST["command"]
        text = request.POST["text"]
        response_url = request.POST["response_url"]
        trigger_id = request.POST["trigger_id"]
        new_data = SlackAskUs(token=token,
                              team_id=team_id,
                              team_domain=team_domain,
                              channel_id=channel_id,
                              channel_name=channel_name,
                              user_id=user_id,
                              user_name=user_name,
                              command=command,
                              text=text,
                              response_url=response_url,
                              trigger_id=trigger_id)
        new_data.save()
        for s in space:
            r = requests.post(url=s.incoming_webhook_url,
                              json={"text": "New message from Collaborizm", 'attachments': [{"text": text}]},
                              headers={"Content-Type": "application/json"})

        response = {"text": "Broadcasting done!"}

        return json_response(response)
    except Exception:
        return json_response({
            "response_type": "ephemeral",
            "text": "Oops! I think there is some issue with this command. Please check back later"
        })


@csrf_exempt
def fbauth(request):
    try:
        if request.method == "GET":
            log = Log(logtext=str(request.GET), timestamp=datetime.datetime.now())
            log.save(force_insert=True)
            if "code" in request.GET and "state" in request.GET:
                code = request.GET["code"]
                state = json.loads(request.GET['state'])
                #print(state)
                token = state["token"]
                team_domain = state["team_domain"]
                user_name = state["user_name"]
                response_url = state["response_url"]
                user = User.objects.filter(team_domain=team_domain, user_name_slack=user_name,
                                           state_params=token)
                if len(user) == 0:
                    return json_response({"status": "failed", "message": "Oops! No user exists"})
                else:
                    user = user[0]
                    user.access_token_fb = code

                    query_loggedin = """
                                    mutation{
                                         authentication{
                                           slackbot(fb_code:\"""" + code + """\"){
                                             user_id
                                             token
                                           }
                                         }
                                        }
                                    """
                    r = requests.post("https://api.oomloop.com/graphql", json={"query": query_loggedin})
                    collab_json = json.loads(r.text)
                    print(collab_json)
                    czm_user = None
                    try:
                        czm_user = collab_json["data"]["authentication"]["slackbot"]["user_id"]
                        user.access_token_fb = collab_json["data"]["authentication"]["slackbot"]["token"]
                    except:
                        return json_response({"status": "failed", "message": "Error fetching information from graphql"})
                    user.state_params = "created"
                    user.user_name_czm = czm_user
                    user.save(force_update=True)
                    # collab_json["data"]["auth"][""]
                    requests.post(response_url,
                                  json={"text": "You are successfully authenticated with facebook and Collaborizm"},
                                  headers={"Content-Type": "application/json"})
                    return json_response(
                        {"status": "success", "message": "Your Collaborizm account was successfully authenticated"})
            else:
                token = request.GET['token']
                # team_id = request.GET['team_id']
                team_domain = request.GET["team_domain"]
                # channel_id = request.GET['channel_id']
                # user_id = request.GET['user_id']
                user_name = request.GET['user_name']
                response_url = request.GET["response_url"]
                state_params = token
                user_id = request.GET['user_id']
                return render(request, 'please/fb_auth.html',
                              {'state_params': state_params, "user_id": user_id, 'user_name': user_name, 'token': token,
                               'team_domain': team_domain, "response_url": response_url})

        elif request.method == "POST":
            log = Log(logtext=str(request.POST), timestamp=datetime.datetime.now())
            log.save(force_insert=True)
            token = request.POST['token']
            team_id = request.POST['team_id']
            team_domain = request.POST["team_domain"]
            channel_id = request.POST['channel_id']
            user_id = request.POST['user_id']
            user_name = request.POST['user_name']
            state_params = token
            user_id = request.POST['user_id']

            user = User.objects.filter(team_domain=team_domain, user_name_slack=user_name,
                                              state_params="created")
            if len(user) == 1:
                # User exists.. no need to save
                # api call to post question to collaborizm
                pass
            else:
                user_new = User(user_name_slack=user_name,
                                slack_token=token,
                                access_token_fb='',
                                team_domain=team_domain,
                                team_id=team_id,
                                channel_id=channel_id,
                                user_name_czm='',
                                state_params=token)
                user_new.save(force_insert=True)
                return render(request, 'please/fbauth.html',
                              {'state_params': state_params, "user_id": user_id, 'user_name': user_name, 'token': token,
                               'team_domain': team_domain})
    except MultiValueDictKeyError:
        return json_response({"error": "Oops!! You crash-landed on this page"})


@csrf_exempt
def user_register_fb(request):
    try:
        if request.method == "POST":
            token = request.POST['token']
            team_domain = request.POST["team_domain"]
            user_id = request.POST['user_id']
            user_name = request.POST['user_name']
            state_params = request.POST["state_params"]
            access_token_fb = request.POST["access_token_fb"]
            response_url = request.POST['response_url']

            user = User.objects.filter(team_domain=team_domain, user_name_slack=user_name, state_params=state_params)
            if len(user) == 0:
                return json_response({"status": "failed", "message": "Didn't perform FB authentication"})
            else:
                user = user[0]
                user.access_token_fb = access_token_fb
                user.state_params = "created"
                user.save(force_update=True)
                query_loggedin = """
                mutation{
                     authentication{
                       facebook(code:"{""" + access_token_fb + """}"){
                         first_name
                         id
                         facebook_id
                       }
                     }
                    }
                """
                r = requests.post("https://api.oomloop.com/graphql", json={"query": query_loggedin})
                collab_json = json.loads(r.text)
                print(collab_json)
                # collab_json["data"]["auth"][""]
                requests.post(response_url, json={"text": "You are successfully authenticated with facebook"},
                              headers={"Content-Type": "application/json"})
                return json_response({"status": "success", "message": "authentication successful"})
        else:
            return json_response({"status": "failed", "message": "Oops!! Someone crashed on this page while flying"})
    except:
        return json_response({"status": "failed", "message": "User doesnot exists"})
