from django.urls import path
from blog import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	# path('', views.Home.as_view(), name='home'),    
	# path('post/<int:id>/', views.PostDetail.as_view(), name='post_detail'),
	# path('post/new/', views.PostCreate.as_view(), name='post_create'),
	path('', views.Home.as_view(), name='home'),
	path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
	path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
	path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
	path('post/new/', views.PostCreateView.as_view(), name='post_create'),
	path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
	path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('post/cat/<int:pk>/', views.PostCategoryView.as_view(), name='post_by_category'),
]
