from django.db import models
from django.utils.translation import gettext_lazy as _t
from django.utils.translation import gettext as _t2

from account.models import CustomUser

EXTERNAL_ID_MAX_LEN = 255

class Subscription(models.Model):
    class PlanChoices(models.TextChoices):
        STANDARD = 'ST', _t('Standard')
        PREMIUM = 'PR', _t('Premium')
    
    plan = models.CharField(max_length=2, choices=PlanChoices, default = PlanChoices.STANDARD)
    cost = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_t('Cost'))
    payment_provider_id = models.CharField(
        max_length=EXTERNAL_ID_MAX_LEN, verbose_name=_t('Payment Provider ID')
    )
    is_active = models.BooleanField(default=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        plan_choice = Subscription.PlanChoices(self.plan)
        return f'{self.user.first_name} {self.user.last_name}: {plan_choice.label} {_t2("subscription")}'
