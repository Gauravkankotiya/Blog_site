import imp
from django.utils import timezone
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse,reverse_lazy
from blog.models import Post,Comment,UserProfileInfo
from blog.forms import PostForm,CommentForm,UserForm
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin # this is called mixin it is same as property decorators in function based views
from django.views.generic import (TemplateView,ListView,
        DetailView,CreateView,UpdateView,DeleteView)
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post


    def get_queryset(self): # this is how u can grab list by sql query in class based views
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        # here __lte calls 'Lookeups' and it means less than or equal to and -publisshed_date give date in decending order


class PostDetailView(DetailView):
    model = Post

class CreatePostView(CreateView,LoginRequiredMixin):  
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')

##################################################
##################################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)


@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit =False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
        
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})


@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)


@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk  # we store this pk because if comment was deleted then we haven't be able to retrive that post from 'comment.post.pk'
    comment.delete()
    return redirect('post_detail',pk=post_pk)


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse_lazy('post_list'))


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user=user_form.save()
            user.set_password(user.password) # this will hash the password
            user.save()

            registered = True
            
        else:
            print(user_form.errors)
    
    else:
        user_form = UserForm()
    
    return render(request,'registration/registration.html',
    {'user_form':user_form,
    'registered':registered})


