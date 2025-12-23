from superuser.views import forumApiView
from django.urls import path
urlpatterns = [
    path("forum",forumApiView.as_view())
]
