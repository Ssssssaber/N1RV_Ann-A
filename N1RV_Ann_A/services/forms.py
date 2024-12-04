from accounts.models import UserAccount
from django.forms import ModelForm, DateTimeInput
from .models import Hairdresser, Service, OrderedServices


class ServiceForm(ModelForm):

    class Meta:
        widgets = {
            'pub_date':  DateTimeInput(attrs={'type': 'date'})
        }
        exclude = {}
        model = Service


class OrderForm(ModelForm):

    class Meta:
        widgets = {
            'serve_date':  DateTimeInput(attrs={'type': 'date'})
        }
        fields = ('hairdresser', 'service', 'serve_date', 'comment')
        model = OrderedServices


class ProfileEditForm(ModelForm):
    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name', 'email', 'hairdresser_preference')
