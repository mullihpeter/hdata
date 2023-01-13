
from django.shortcuts import get_object_or_404

from django.core.exceptions import PermissionDenied

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy

from .models import Image


class ImageListView(ListView):
    model = Image

    template_name = 'image_app/list.html'

    context_object_name = 'images'


class ImageTagListView(ImageListView):
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


class ImageDetailView(DetailView):
    model = Image

    template_name = 'image_app/detail.html'

    context_object_name = 'image'


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image

    fields = ['title', 'description', 'image', 'tags']

    template_name = 'image_app/create.html'

    success_url = reverse_lazy('image:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class UserIsSubmitter(UserPassesTestMixin):

    # Custom method
    def get_photo(self):
        return get_object_or_404(Image, pk=self.kwargs.get('pk'))

    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().owner
        else:
            raise PermissionDenied('Sorry you are not allowed here')


class ImageUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'image_app/update.html'

    model = Image

    fields = ['title', 'description', 'tags']

    success_url = reverse_lazy('image:list')


class ImageDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'image_app/delete.html'

    model = Image

    success_url = reverse_lazy('image:list')