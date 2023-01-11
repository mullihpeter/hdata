from django.shortcuts import render, redirect, get_object_or_404
from . models import Video
from django.views.generic import DetailView, DeleteView, UpdateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    success_url = "/"
    template_name = "stream/post-video.html"
    fields = ['title', 'description', 'video']

    # to make sure that the logged-in user is the one to upload the content
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)