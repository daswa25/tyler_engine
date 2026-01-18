from mailbox import Message
from math import e
from os import execv
from sys import exception
from django.forms import model_to_dict
from django.shortcuts import render,redirect
from django.core.mail import EmailMessage
from django.http import JsonResponse
# it do cred methods
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login,authenticate,logout
from .serializers import UserSerializers,ForgetPassword,PostBlog,searchBlogSerializer
from .models import User,blog,messages
from django.contrib.auth import get_user_model
from random import randint
from django.db.models import Q,Count
from django.forms.models import model_to_dict
import datetime
code=""
def code_rand():
    return  
def err_func(errs):
    flat_errors=""
    for field,flat_err in errs.items():
        for error in flat_err:
            flat_errors+=f"<li><a style='color:red'>{field}-{str(error)}</a></li>"
    return flat_errors
# Create your views here.
class RegisterTylerView(APIView):
    def get(self, request):
        return render(request,"general/register.html",{"register":"Welcome to the universe tyler"})
    def post(self,request):
        serializers=UserSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'Message':True})
        error_msg=serializers.errors
        flat_errors=err_func(error_msg)
        return Response({'Error':flat_errors})
class LoginTylerView(APIView):
    def get(self, request):
        #lgn=User.objects.all()
        #user_das=User.objects.get(email='daswadayalan@gmail.com')
        return render(request,"general/login.html",{"bio":'',"user":''})
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Email: {email}, Password: {password}")

        # Check if user exists with email
        try:
            user = User.objects.get(email=email)
            print("User found:", user.email)
        except User.DoesNotExist:
            print("User does not exist")
            return Response({"Error": "User not found"})

        # Check password manually
        if user.check_password(password):
            print("Password matches")
        else:
            print("Password does NOT match")

        # Now try authenticate
        user_auth = authenticate(request, username=email, password=password)
        print("Authenticate returned:", user_auth)

        if user_auth:
            login(request, user_auth)
            user_auth.alive = 1
            user_auth.save()
            request.session['user_id'] = user_auth.id
            return Response({"Message": True})
        return Response({"Error": "Invalid Credentials"})


class ForumView(APIView):
    def get(self,request):
        
        sess_id = request.session.get('user_id')  # safely get user_id from session
        blog_id= request.GET.get('blog_id')
        edit = request.GET.get('edit')
        #Just viewing the posted blogs
        if sess_id is not None:
            try:
                if edit is not None:
                    blogs= blog.objects.get(pk=blog_id)
                    blog_title=blogs.blog_title
                    blog_content=blogs.blog_content
                    return Response({"blog_title":blog_title,"blog_content":blog_content,"Message":True})
                else:
                    user_details = User.objects.get(id=sess_id)
                    blogs=blog.objects.order_by('-date_joined')
                    return render(request, "general/dashboard.html", {"user_id": user_details,"blogs":blogs})
            except User.DoesNotExist:
            # user not found, redirect to login
                return redirect("/api/login")
        else:
        # session key not found, redirect to login

            return redirect("/api/login")
class LogOutView(APIView):
    def get(self,request):
        sess_id=request.session['user_id']
        user_auth=User.objects.get(id=sess_id)
        user_auth.alive=0
        user_auth.save()
        request.session.flush()
        logout(request)
        return Response({"Message":True})
class getCodeView(APIView):
  
    def post(self, request):
        email = request.POST.get('email')
        if not email:
            return Response({"Error": "Email is required"})

        code = randint(100000, 999999)  # avoid starting with 0

        html_content = f"""<!DOCTYPE html><html><body>
            <h1>Your Security Code</h1>
            <div class='bg-dark'><h1>{code}</h1></div>
            <a class='text-primary'>For support: durdendas@gmail.com</a>
        </body></html>"""

        try:
            email_html = EmailMessage(
                'Security Code for Password Reset',
                html_content,
                'durdendas@gmail.com',
                [email]
            )
            email_html.content_subtype = "html"
            email_ok = email_html.send()

            if email_ok:
                try:
                    user = User.objects.get(email=email)
                    user.security_code = code
                    user.save()
                    return Response({"Message": True})
                except User.DoesNotExist:
                    return Response({"Error": "User not found"})

            else:
                return Response({"Error": "Email could not be sent"})

        except Exception as e:
            return Response({"Error": str(e)})

        # ✅ final fallback
        return Response({"Error": "Unknown error occurred"})

        
class forgerView(APIView):
    def post(self,request):
        upserializers=ForgetPassword(data=request.data)
        if upserializers.is_valid():
            try:
                upserializers.save()
                return Response({"Message":True})
            except Exception as e:
                return Response({'Error':str(e)})
        error_msg=upserializers.errors
        print(upserializers.errors)
        flat_errors=err_func(error_msg)
        return Response({'Error':flat_errors})

class BlogPost(APIView):
    #Read (CRED- Create Read Edit And Delete)
    def get(self,request):
        blog_id=blog.objects.filter(id=request.method.GET('user_id'))
        print(request.method.GET('user_id'))
        #return Response({"user_id":request.method.GET('user_id')})

    def post(self,request):
        edit_it= request.POST.get('edit_it',False) in [True,"true",1,"1","True"]
        delete_it= request.POST.get('delete_it',False) in [True,"true",1,"1","True"]
        blog_id=request.POST.get('blog_id')
        #edit
        if edit_it and blog_id:
            try:
                instance=blog.objects.get(id=blog_id,user_id=request.user)
                serializers=PostBlog(instance,data=request.data)
            except blog.DoesNotExist:
                return Response({"Error":"Blog Not Found or Permission Denied"})
        #delete
        elif delete_it and blog_id:
            try:
                instance= blog.objects.get(id=blog_id,user_id=request.user)
                serializers=PostBlog()
                serializers.delete(instance)
                return  Response({"Message":True})
            except blog.DoesNotExist:
                return  Response({"Error":"Blog not found or permission denied"})
        #create
        else:

            serializers=PostBlog(data=request.data)
        if serializers.is_valid():
           # session_id=request.session['user_id']
            serializers.save(user_id=request.user)
            return Response({"Message":True})
        return Response({"error":serializers.errors})
class SeeOtherPost(APIView):
    def get(self,request,id):
        blog_id= request.GET.get('blog_id')
        print(blog_id)
        try:
            user_details=User.objects.get(id=id)
            blog_post=user_details.blog_set.all()
            return  render(request,"general/see_other_post.html",{"user_post":blog_post})
        except User.DoesNotExist:
            return  Response({"Error":"Permission Denied  or Something went Wrong"})
        

class games(APIView):

    def get(self,request):
        sess_id= request.session.get('user_id')
        if sess_id:
            try :
                user_details=User.objects.get(id=sess_id)
                return render(request,"general/games/tictactoe.html",{"Welcome":"welcome to tic tac toe","user_id":user_details})
            except User.DoesNotExist:
                return redirect("/api/login")
        else:
            return redirect("/api/login")
class searchPost(APIView):
    def post(self,request):
        search_title=request.POST.get('search')
        try:
            blog_details=blog.objects.filter(Q(blog_title__icontains=search_title))
            #blog_users=blog_details.user_id.first_name
            serailizers=searchBlogSerializer(blog_details,many=True)
            
            return Response(serailizers.data)
        except blog.DoesNotExist:
            return Response({"message":True})
class friendsList(APIView):
    def get(self,request):
        try:
            # 1. Get all your friends
            # (Assuming you want to see friends even if they haven't messaged you)
            myFriends = list(User.objects.all().values('id', 'first_name', 'alive'))

            # 2. Get the specific Counts
            # Logic:
            # - pid = request.user.id  -> "I am the Receiver"
            # - read = 0               -> "Message is Unread"
            # - values('fid')          -> "Group them by the Sender (Friend)"
            chat_notifications = messages.objects.filter(
                fid=request.user.id, 
                read=0
            ).values('pid').annotate(msg_count=Count('id'))

            # 3. Create the Lookup Dictionary
            # Format: { Friend_ID : Count } -> { 2: 5, 4: 1 }
            unread_map = { item['pid']: item['msg_count'] for item in chat_notifications }

            # 4. Merge the count into your friends list
            for friend in myFriends:
                # Check if this friend's ID exists in our unread_map
                # If yes, add the count. If no, set it to 0.
                friend['msg_count'] = unread_map.get(friend['id'], 0)

            return Response({"message": True, "data": myFriends})
        except User.DoesNotExist:
            return Response({"message": False})
        
        
class chatload(APIView):
    def get(self, request):
        target_id = request.GET.get('id')
        my_id = request.GET.get('pid')
        self_or_click=request.GET.get('selforclick')
        if not target_id or not my_id:
            return Response({"message": False, "data": "Missing IDs"})
        if self_or_click is 1:
            messages.objects.filter(
                    fid=target_id, 
                    pid=my_id, 
                    read=0
                ).update(read=1)
        
        data = messages.objects.filter(
            Q(fid=target_id, pid=my_id) | Q(fid=my_id, pid=target_id)
        ).order_by('date_messaged').values('message', 'date_messaged', 'pid', 'fid')
      
   

        return Response({"message": True, "data": list(data)})
    def post(self,request):
        home_id=request.POST.get('id')
        fk_id= request.POST.get('fk_id')
        message=request.POST.get('message')
        try:
            UserDetails=User.objects.get(id=fk_id)
            
            if UserDetails:
                message=messages.objects.create(pid=home_id,fid=UserDetails,message=message) 
                return Response({"message":True,"data":"message delivered"})
            else:
                return Response({"message":False,"data":"Message not delivered"})
                
        except User.DoesNotExist:
            return Response({"message":False})
        
class UpdateBio(APIView):
    def get(self,request):
        user_id=request.GET.get('id')
        
        try:
            user_detail=User.objects.get(id=user_id)
            target_fields = ['first_name', 'last_name', 'email', 'gender', 'date_joined']
            response_data=model_to_dict(user_detail,target_fields)
            response_data_type={}
            for field_name in target_fields:
                field_obj=User._meta.get_field(field_name)
                internal_type=field_obj.get_internal_type()
                if internal_type in ['CharField', 'TextField']:
                    response_data_type[field_name] = 'text'
                elif internal_type == 'EmailField':
                    response_data_type[field_name] = 'email'
                elif internal_type in ['IntegerField', 'AutoField']:
                    response_data_type[field_name] = 'number'
                elif internal_type == 'BooleanField':
                    response_data_type[field_name] = 'checkbox'
                elif internal_type in ['DateField', 'DateTimeField']:
                    response_data_type[field_name] = 'date'
                else:
                    response_data_type[field_name] = 'text'
            return Response({"message":True,"data":response_data,"type":response_data_type})
            
        except User.DoesNotExist:
            return Response({"message":"Error"})
    def post(self,request):
        user_id=request.POST.get('id')
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        gender=request.POST.get('gender')
        try:
            user_details=User.objects.get(id=user_id)
            if user_details:
                user_details.email=email
                user_details.first_name=first_name
                user_details.last_name=last_name
                user_details.gender=gender
                user_details.save()
                return Response({"message":True,"data":"success,updated"})
                    
            
             
        except User.DoesNotExist:
            return Response({"message":"user does not exist"})
