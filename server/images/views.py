
from django.shortcuts import get_object_or_404

from django.core.exceptions import PermissionDenied

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy

from .models import Image


class PhotoListView(ListView):
    model = Image

    template_name = 'image_app/list.html'

    context_object_name = 'photos'


class PhotoTagListView(PhotoListView):
    template_name = 'image_app/taglist.html'

    # Custom function
    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context


class PhotoDetailView(DetailView):
    model = Image

    template_name = 'image_app/detail.html'

    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Image

    fields = ['title', 'description', 'image', 'tags']

    template_name = 'image_app/create.html'

    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):
        form.instance.submitter = self.request.user

        return super().form_valid(form)


class UserIsSubmitter(UserPassesTestMixin):

    # Custom method
    def get_photo(self):
        return get_object_or_404(Image, pk=self.kwargs.get('pk'))

    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')


class PhotoUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'image_app/update.html'

    model = Image

    fields = ['title', 'description', 'tags']

    success_url = reverse_lazy('photo:list')


class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'image_app/delete.html'

    model = Image

    success_url = reverse_lazy('photo:list')