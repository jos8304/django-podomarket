from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from allauth.account.views import PasswordChangeView

from braces.views import LoginRequiredMixin
from .mixins import LoginAndVerificationRequiredMixin, LoginAndOwnershipRequiredMixin

from .forms import PostCreateForm, PostUpdateForm, ProfileForm,CommentForm
from .models import Post, User, Comment


class IndexView(ListView):
    model = Post
    template_name = 'podomarket/index.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(is_sold=False)


class PostDetailView(DetailView):
    model = Post
    template_name = 'podomarket/post_detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
        

class PostCreateView(LoginAndVerificationRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'podomarket/post_form.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.object.id})


class PostUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'podomarket/post_form.html'
    pk_url_kwarg = 'post_id'


    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.object.id})


class PostDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Post
    template_name = 'podomarket/post_confirm_delete.html'
    pk_url_kwarg = 'post_id'
    
    def get_success_url(self):
        return reverse('index')

class CommentCreateView(LoginAndVerificationRequiredMixin, CreateView):
    http_method_names = ['post']

    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs.get('post_id'))        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.kwargs.get('post_id')})


class ProfileView(DetailView):
    model = User
    template_name = 'podomarket/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_posts'] = Post.objects.filter(author__id=self.kwargs.get('user_id'))[:8]
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'podomarket/user_post_list.html'
    context_object_name = 'user_posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(author__id=self.kwargs.get('user_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, id=self.kwargs.get('user_id'))
        return context


class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'podomarket/profile_set_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('index')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'podomarket/profile_update_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})
