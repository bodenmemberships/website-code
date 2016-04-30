from django.forms import ModelForm
from .models import PublicationSubscription


class PublicationSubscriptionForm(ModelForm):
    class Meta:
        model=PublicationSubscription
        exclude=[]