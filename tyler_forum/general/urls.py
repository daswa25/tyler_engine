from django.urls import path
from .views import RegisterTylerView,LoginTylerView,ForumView,LogOutView,getCodeView,forgerView,BlogPost,SeeOtherPost,games,searchPost,friendsList

urlpatterns=[
    path('register',RegisterTylerView.as_view(),name='register'),
    path('login',LoginTylerView.as_view(),name='login'),
    path('logout',LogOutView.as_view(),name='logout'),
    path('forum',ForumView.as_view(),name='forum'),
    path('search_blog',searchPost.as_view(),name='search-post'),
    path('getcode',getCodeView.as_view(),name="get-code"),
    path('reset_password',forgerView.as_view(),name="forget-password"),
    path('blog_post',BlogPost.as_view(),name="post-blog"),
    path('see_post/<int:id>',SeeOtherPost.as_view(),name='see-other-post'),
    path('games',games.as_view(),name='games'),
    path('chat',friendsList.as_view(),name='chat')
]