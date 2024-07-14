from django.shortcuts import render,get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.exceptions import AuthenticationFailed

from .serializers import UserSerializer,ProfileSerializer,PostSerializer
from .models import Profile,Post

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

import jwt,datetime
# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
       
        if serializer.is_valid():
            user = serializer.save()
            print(serializer.data.get('password'))
            profile = Profile(user=user,user_type = request.data.get('user_type'))
            profile.save()
            return Response({'message':'signup sucess', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'something went wrong', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username,password=password)
        
        if not user:
            raise AuthenticationFailed("user not found")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")
        payload = {
            'id':user.id,
            'exp':datetime.datetime.now(datetime.UTC)+datetime.timedelta(minutes=60)
        }
        jwtoken = jwt.encode(payload,'secret',algorithm='HS256')
        response = Response()
        response.set_cookie(
            key='jwtoken',
            value=jwtoken
        )
        response.data = {'messsage':'login sucessfull','jwtoken':jwtoken} 
        return response
    
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        response = Response()
        response.delete_cookie('jwtoken')
        response.data = {'messsage':'loggedout.....'} 
        return response

class PostView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        # token = request.COOKIES.get('jwtoken')
        # payload = jwt.decode(token,'secret',algorithms=['HS256'])
        # print(payload)
        # user = User.objects.filter(id=payload['id']).first()
        # print(user)
        # profile = Profile.objects.get(user=user)
        
        # the below request is coming from middleware
        # print(request.profile)
        # return Response({'msg':"hi"})
        if request.profile.user_type == 'reader':
            raise AuthenticationFailed('Unauthorised....')
        
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save(author=request.profile)
           return Response({'messsage':'Post Created', 'data':serializer.data} )
        return Response({'message':'something went wrong', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,*args,**kwargs):
        # token = request.COOKIES.get('jwtoken')
        # payload = jwt.decode(token,'secret',algorithms=['HS256'])
        # user = User.objects.filter(id=payload['id']).first()
        # profile = Profile.objects.get(user=user)
        
        # request.profile is coing from middleware
        if request.profile.user_type == 'reader':
            raise AuthenticationFailed('Unauthorised....')
        
        try:
         post_id = kwargs.get('pk')
         post = Post.objects.get(id=post_id,author=request.profile)
        except Post.DoesNotExist:
            return Response({'messsage':'Post Not Found'})
       
        
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
           serializer.save()
           return Response({'messsage':'Post Updated', 'data':serializer.data} )
        return Response({'message':'something went wrong', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,*args,**kwargs):
        # token = request.COOKIES.get('jwtoken')
        # payload = jwt.decode(token,'secret',algorithms=['HS256'])
        # user = User.objects.filter(id=payload['id']).first()
        # profile = Profile.objects.get(user=user)
        
        # request.profile is coing from middleware
        if request.profile.user_type == 'reader':
            raise AuthenticationFailed('Unauthorised....')
        
        try:
         post_id = kwargs.get('pk')
         post = Post.objects.get(id=post_id,author=request.profile)
        except Post.DoesNotExist:
            return Response({'messsage':'Post Not Found'})
        post.delete()
        return Response({'messsage':'Post Deleted'})

class PostListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AuthorPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.profile.user_type != 'author':
            return Response({'message': "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        posts = Post.objects.filter(author=request.profile)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)