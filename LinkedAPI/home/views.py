from django.http import HttpResponse
from django.shortcuts import render
from django.utils.http import urlencode
import urllib.parse
import requests,json

# Create your views here.
client_id="78l8w40ecuiqn8"
client_secret="dEom2PsSuYscE1wN"
redirect_url=urllib.parse.quote("http://127.0.0.1:8000/user")
scope=urllib.parse.quote("w_member_social,r_emailaddress,r_liteprofile,openid,profile,email")
userId=None



def home(request):
    
    url=f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&state=987654321&scope={scope}&client_id={client_id}&redirect_uri={redirect_url}"
    context={"url":url}

    return render(request, "home/index.html",context)

def user(request):
    if request.method=="GET":
        #Getting the Authentication code form the url
        auth_code= request.GET["code"]
        state= request.GET["state"]
        context={"auth_code":auth_code, "state":state}
        #url to get the access token
        access_token_url=f"https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={auth_code}&redirect_uri={redirect_url}"

        data= requests.get(url=access_token_url)
        data=data.json()
        access_token=data["access_token"]
        context["access_token"]=access_token


        LnPUrl="https://api.linkedin.com/v2/me"
        global head
        head = {'Authorization': 'Bearer {}'.format(access_token)}
        user_data = requests.get(LnPUrl, headers=head)
        user_data=user_data.json()
        context["user_data"]=user_data
        name= user_data["localizedLastName"]+" "+user_data["localizedFirstName"]
        global userId
        userId=user_data["id"]
        context["name"]=name
    

    return render(request,'home/action.html',context)


def share(request):
    if request.method=="GET":
        value=request.GET.get('type')
        if value=='text':
            return render(request,'home/share/text_post.html')
        elif value=="link":
            return render(request,'home/share/article_post.html')
        elif value=='image':
            return render(request,'home/share/img_post.html')
        else:
            return HttpResponse("Invalid Option")
        
def txt_post(request):
    json_txt_post={
        "author": "urn:li:person:{userID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": 
        {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "hi"
            },
            "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    if request.method=="POST":
        txt_data= request.POST.get('data')
        
        json_txt_post['author']=f"urn:li:person:{userId}"
        json_txt_post['specificContent']['com.linkedin.ugc.ShareContent']['shareCommentary']["text"]=txt_data

        context={"userId":userId,"txt_data":txt_data,"body":json_txt_post,"header":head}
        # return render(request,'home/share/sample.html',context)

        url = 'https://api.linkedin.com/v2/ugcPosts'
        
        response = requests.post(url=url, headers=head, json=json_txt_post)
        response=response.json()
        print(response)

        return HttpResponse("The post is sucessfully posted "+response['id'])

def article_post(request):
    json_article_post={
    "author": "",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "Learning more about LinkedIn by reading the LinkedIn Blog!"
            },
            "shareMediaCategory": "ARTICLE",
            "media": [
                {
                    "status": "READY",
                    "description": {
                        "text": "Official LinkedIn Blog - Your source for insights and information about LinkedIn."
                    },
                    "originalUrl": "https://blog.linkedin.com/",
                    "title": {
                        "text": "Official LinkedIn Blog"
                    },
                    "thumbnails":[{
                        "url":""
                    }]

                }
            ]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
    }

    if request.method=="POST":
        f_data=request.POST.get('f_data')
        l_title=request.POST.get('l_title')
        l_desc=request.POST.get('l_desc')
        l_url=request.POST.get('l_url')
        t_type=request.POST.get('t_type')

        json_article_post['author']=f"urn:li:person:{userId}"
        json_article_post['specificContent']['com.linkedin.ugc.ShareContent']['shareCommentary']["text"]=f_data
        json_article_post['specificContent']['com.linkedin.ugc.ShareContent']['media'][0]['description']['text']=l_desc
        json_article_post['specificContent']['com.linkedin.ugc.ShareContent']['media'][0]['title']['text']=l_title
        json_article_post['specificContent']['com.linkedin.ugc.ShareContent']['media'][0]['originalUrl']=l_url
        json_article_post['visibility']['com.linkedin.ugc.MemberNetworkVisibility']=t_type
        json_article_post['specificContent']['com.linkedin.ugc.ShareContent']['media'][0]['thumbnaiils'][0]['url']=l_url
        url="https://api.linkedin.com/v2/ugcPosts"
        response = requests.post(url=url, headers=head, json=json_article_post)
        response=response.json()

        return HttpResponse("The article was sucessfully posted "+response['id'])



    return render(request,'home/share/article_post.html')


def img_post(request):
    if request.method=="POST":
        f_data=request.POST.get('f_data')
        image_file = request.FILES['img']
        img_binary_data=image_file.read()
        img_title=request.POST.get('img_title')
        img_desc=request.POST.get('img_desc')
        t_type=request.POST.get('t_type')

        #REGISTERING THE IMAGE
        reg_url='https://api.linkedin.com/v2/assets?action=registerUpload'
        reg_url_body={
            "registerUploadRequest": {
            "recipes": [
                "urn:li:digitalmediaRecipe:feedshare-image"
            ],  
            "owner": "",
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
            }
        }

        reg_url_body['owner']=f"urn:li:person:{userId}"
        reg_resp=requests.post(url=reg_url, headers=head, json=reg_url_body)
        reg_resp=reg_resp.json()
        return HttpResponse(reg_resp)
        # upload_url=reg_resp['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        # asset=reg_resp['value']['asset']

        # upload_resp=requests.post(url=upload_url,headers=head ,files={'image': img_binary_data})
        # upload_resp=upload_resp.json()
        # print(upload_resp)
        

        

    return render(request,'home/share/img_post.html')


def send_invitation(request):
    invitation_body={
    "invitee": "urn:li:email:test@linkedin.com",
    "message": {
        "com.linkedin.invitations.InvitationMessage": {
            "body": "Let's connect!"
        }
    }
    }
    if request.method=="POST":
        invitee=request.POST.get('invitee')
        msg=request.POST.get('msg')


        url="https://api.linkedin.com/v2/invitations"
        invitation_body["invitee"]=f"urn:li:person:{invitee}"
        invitation_body["message"]["com.linkedin.invitations.InvitationMessage"]["body"]=msg

        response = requests.post(url=url, headers=head, json=invitation_body)
        response=response.json()
        
        return HttpResponse(response)



    return render(request,'home/invitation/send_invitation.html')