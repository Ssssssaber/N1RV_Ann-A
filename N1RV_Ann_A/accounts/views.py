from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from accounts.forms import SignUpForm


class RegisterView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('main:index')