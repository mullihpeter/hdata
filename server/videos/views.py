from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from .forms import VideoUploadForm
from django.views.generic import DetailView, DeleteView, UpdateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


class VideoDetailView(DetailView):
    template_name = "video/video-detail.html"
    model = Video


class GeneralVideoListView(ListView):
    model = Video
    template_name = 'video/video-list.html'
    context_object_name = 'videos'
    ordering = ['-upload_date']


def search(request):
    if request.method == "POST":
        query = request.POST.get('title', None)
        if query:
            results = Video.objects.filter(title__contains=query)
            return render(request, './video/search.html', {'videos': results})

    return render(request, 'video/search.html')


class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    success_url = "/"
    template_name = 'video/post-video.html'
    fields = ['title', 'description', 'video']

    # this is to make sure that the logged-in user is the one to upload the content
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class VideoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    template_name = 'video/post-video.html'
    success_url = "/"
    fields = ['title', 'description', 'video']

    # this is to make sure that the logged-in user is the one to upload the content
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    # this function prevents other people from updating other user's videos
    def test_func(self):
        video = self.get_object()
        if self.request.user == video.owner:
            return True
        return False


class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "video/video-confirm-delete.html"
    success_url = "/"
    model = Video

    def test_func(self):
        video = self.get_object()
        if self.request.user == video.owner:
            return True
        return False


class UserVideoListView(ListView):
    model = Video
    template_name = "video/user_videos.html"
    context_object_name = 'videos'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Video.objects.filter(owner=user).order_by('-upload_date')









