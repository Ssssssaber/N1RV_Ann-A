from django.contrib.auth.forms import UserCreationForm
from accounts.models import UserAccount


class SignUpForm(UserCreationForm):

    class Meta:
        model = UserAccount
        fields = ('username', 'password1', 'password2')