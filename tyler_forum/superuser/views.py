from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from general.models import User
# Create your views here.
class forumApiView  (APIView):
    def get(self,request):
        Users_details=User.objects.all()
        return render(request,"admin/adminForum.html",{"users_info":Users_details})