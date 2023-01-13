from django.shortcuts import redirect, render

from django.views.generic import CreateView

from django.contrib.auth.views import LoginView

from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required

from . forms import UserCreationForm, UserChangeForm, UserProfileUpdateForm

from django.urls import reverse_lazy

class SignUpView(CreateView):

    template_name = 'users/register.html'

    form_class = UserCreationForm

    success_url = reverse_lazy('image:list')

    def form_valid(self, form):
        to_return = super().form_valid(form)

        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )

        login(self.request, user)


        return to_return

class CustomLoginView(LoginView):

    template_name = 'users/login.html'

@login_required
def profile(request):
    if request.method == "POST":
        userform = UserChangeForm(request.POST, instance=request.user)
        profileform = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            return redirect("profile")
    else:
        userform = UserChangeForm(instance=request.user)
        profileform = UserProfileUpdateForm(instance=request.user.user_profile)

    context = {
        'userform': userform,
        'profileform': profileform
    }
    return render(request, 'users/profile.html', context)