from django.forms import ModelForm
from common.django_utils import AsyncModelFormMixin
from writer.models import Article


class ArticleForm(ModelForm, AsyncModelFormMixin):
    class Meta:
        model = Article
        fields = (
            'title',
            'content',
            'is_premium',
        )