from typing import Iterable

from django import forms
from django.forms import Form, ModelForm
from django.utils.translation import gettext_lazy as _t
from asgiref.sync import sync_to_async

from common.django_utils import AsyncModelFormMixin
from .models import PlanChoice, Subscription
from account.models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm


class UpdateSubscriptionForm(Form, AsyncModelFormMixin):
    plan_choices = forms.ChoiceField(label=_t('Update Plan Choices'))
    
    def __init__(self, *args, exclude:Iterable[str] | None = None, format_fn = lambda plan_choice: plan_choice.name, **kwargs):
        super().__init__(*args, **kwargs)
        
        plan_choices = PlanChoice.objects.filter(is_active=True)
        if exclude:
            plan_choices = plan_choices.exclude(plan_code__in=exclude)
            
        self.fields['plan_choices'].choices = (
            (plan_choice.plan_code, format_fn(plan_choice))
            for plan_choice in plan_choices
        )
        
    @classmethod
    async def ainit (cls, *args, **kwargs) -> 'UpdateSubscriptionForm':
        @sync_to_async
        def call_init() -> UpdateSubscriptionForm:
            return UpdateSubscriptionForm(*args, **kwargs)
        
        return await call_init()


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