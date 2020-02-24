from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.views.generic.base import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView 

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from blog.models import Post, Comment, Category

from blog.forms import PostForm, CommentForm


# # Basic Class Base View
# class Home(View):
# 	def get(self, request):
# 		posts = Post.objects.all()
# 		return render(request, "blog/home.html",{"posts":posts})


# # Basic Class Base View
# class PostDetail(View):
# 	def get(self, request, pk):
# 		post = Post.objects.get(pk=pk)
# 		return render(request, "blog/post_detail.html",{"post":post})


# # Basic Class Base View
# class PostCreate(View):
# 	def get(self, request):
# 		form = PostForm()
# 		return render(request, 'blog/post_form.html',{'form':form})


# 	def post(self, request):
# 		form = PostForm(request.POST or None)
# 		if form.is_valid():
# 			print(form)
# 			form.save()
# 			return redirect('home')
# 		return render(request, 'blog/post_form.html',{'form':form})


class PageContextMixin(object):
	page_title = None

	def get_context_data(self, **kwargs):
		context = super(PageContextMixin, self).get_context_data(**kwargs)
		context['page_title'] = self.page_title
		return context
		
# Generic Class Base View - (List of Posts)
class Home(PageContextMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = '-pub_date'
    paginate_by = 4
    page_title = "Home"


# Generic Class Base View - (List of User Posts)
@method_decorator(login_required, name='dispatch')
class Dashboard(View):
	def get(self, request, *args, **kwargs):
		view = Home.as_view(
			template_name = 'blog/admin_page.html',
			paginate_by = 5
			)
		return view(request, *args, **kwargs)


# # Generic Class Base View - (Post Display View)
# class PostDisplayView(DetailView):
# 	model = Post
# 	template_name = 'blog/post_detail.html'	


# 	def get_object(self):
# 		object = super(PostDisplayView, self).get_object()
# 		object.view_count += 1
# 		object.save()
# 		return object


# 	def get_context_data(self, **kwargs):
# 		context = super(PostDisplayView, self).get_context_data(**kwargs)
# 		context['comments'] = Comment.objects.filter(post=self.get_object())
# 		context['form'] = CommentForm()
# 		return context


# Generic Class Base View - (Post Display View)
class PostDisplayView(PageContextMixin, SingleObjectMixin, View):
	model = Post
	page_title = "Detail"


	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.view_count += 1
		self.object.save()
		post = self.get_context_data(instance=self.object)
		return render(request, 'blog/post_detail.html',post)


	def get_context_data(self, **kwargs):
		context = super(PostDisplayView, self).get_context_data(**kwargs)
		context['comments'] = Comment.objects.filter(post=self.get_object())
		context['form'] = CommentForm()
		return context


# Generic Class Base View - (Comment View)
class PostCommentView(FormView):
	form_class = CommentForm
	template_name = 'blog/post_detail.html'


	def form_valid(self, form):
		form.instance.by = self.request.user
		post = Post.objects.get(pk=self.kwargs['pk'])
		form.instance.post = post
		form.save()
		return super(PostCommentView, self).form_valid(form)


	def get_success_url(self):
		return reverse('post_detail', kwargs={'pk':self.kwargs['pk']})


# Generic Class Base View - (Post Detail View)
class PostDetailView(View):
	def get(self, request, *args, **kwargs):
		view = PostDisplayView.as_view()
		return view(request, *args, **kwargs)


	def post(self, request, *args, **kwargs):
		view = PostCommentView.as_view()
		return view(request, *args, **kwargs)


# Generic Class Base View - (Post Create View)
class PostCreateView(CreateView):
	model = Post
	fields = ('title','category','content')


	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(PostCreateView, self).form_valid(form)


# Generic Class Base View - (Post Update View)
class PostUpdateView(UpdateView):
	model = Post
	fields = ('title','category','content')


# Generic Class Base View (Post Delete View)
class PostDeleteView(DeleteView):
	model = Post
	success_url = reverse_lazy('dashboard')


class PostCategoryView(ListView):
	model = Post
	template_name = 'blog/post_category.html'
	context_object_name = 'posts'


	def get_queryset(self):
		self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
		return Post.objects.filter(category=self.category)


	def get_context_data(self, **kwargs):
		context = super(PostCategoryView, self).get_context_data(**kwargs)
		context['category'] = self.category
		return context