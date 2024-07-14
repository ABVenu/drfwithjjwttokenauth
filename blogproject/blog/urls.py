from django.urls import path,include
from .views import RegisterView,LoginView,LogoutView,PostView,PostDetailView,AuthorPostsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('posts/', PostView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostView.as_view(), name='postseditdelete'),
    path('posts/detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('author/posts/', AuthorPostsView.as_view(), name='author_posts'),  # URL for author posts

]
