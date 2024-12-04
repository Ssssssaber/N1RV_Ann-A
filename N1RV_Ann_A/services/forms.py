from accounts.models import UserAccount
from django.forms import ModelForm, DateInput, TimeInput
from .models import Hairdresser, Service, OrderedServices
from django import forms

class ServiceForm(ModelForm):
    class Meta:
        widgets = {
            'pub_date':  DateInput()
        }
        exclude = {}
        model = Service


class OrderForm(ModelForm):
    serve_time = forms.TimeField(label='Время оказания услуги')
    class Meta:
        widgets = {
            'serve_date': DateInput(attrs={'type': 'date'}),
        }
        
        fields = ('hairdresser', 'service', 'serve_date', 'serve_time', 'comment')
        model = OrderedServices

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['serve_time'].widget = TimeInput(attrs={'type': 'time'})


class ProfileEditForm(ModelForm):
    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name', 'email', 'hairdresser_preference')



class HairdresserForm(ModelForm):
    class Meta:
        model = Hairdresser
        fields = ('first_name', 'last_name', 'description', 'slug', 'image', 'services')
