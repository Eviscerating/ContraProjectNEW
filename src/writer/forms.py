from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm
from common.django_utils import AsyncModelFormMixin
from writer.models import Article
from account.models import CustomUser

class ArticleForm(ModelForm, AsyncModelFormMixin):
    class Meta:
        model = Article
        fields = (
            'title',
            'content',
            'is_premium',
        )

class UpdateUserForm(ModelForm, AsyncModelFormMixin):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
        )

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})