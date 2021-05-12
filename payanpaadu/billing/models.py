import json
from json import JSONDecodeError

from django.db import models

from tandorautils.settings import DEFAULT_PLAN_FEATURES

NOT_APPLICABLE = 'NA'
INVOICE_URL = 'https://invoices.razorpay.com/v1/invoices/{invoice_id}/pdf?download=1'


class PricePlan(models.Model):
    name = models.CharField(max_length=100)
    monthly_price = models.FloatField()
    yearly_price = models.FloatField()
    active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    plan_features = models.TextField()

    def __str__(self):
        return self.name


class Subscription(models.Model):
    company = models.OneToOneField('Company', null=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(PricePlan, null=True, on_delete=models.DO_NOTHING)
    extra_plan_features = models.TextField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    is_yearly = models.BooleanField(default=True)
    razorpay_account_id = models.CharField(max_length=50, unique=True, db_index=True)
    razorpay_data = models.TextField()
    last_paid_time = models.DateTimeField(null=True)
    invoice_id = models.CharField(max_length=50, default=NOT_APPLICABLE)

    @property
    def all_plan_features(self):
        features = DEFAULT_PLAN_FEATURES
        if self.plan and self.plan.plan_features:
            try:
                features.update(json.loads(self.plan.plan_features))
            except JSONDecodeError:
                pass

        if self.extra_plan_features:
            try:
                features.update(json.loads(self.extra_plan_features))
            except JSONDecodeError:
                pass

        return features

    @property
    def invoice_url(self):
        if hasattr(self, 'invoice_id') and self.invoice_id != NOT_APPLICABLE:
            return INVOICE_URL.replace('{invoice_id}', self.invoice_id)
        else:
            return '~'

    def __str__(self):
        return f'{str(self.company)} is in {self.plan.name if self.plan else ""}'


class PendingInvoice(models.Model):
    company = models.OneToOneField('Company', on_delete=models.CASCADE)
    plan = models.ForeignKey('PricePlan', on_delete=models.DO_NOTHING)
    invoice_id = models.CharField(max_length=50)
    short_url = models.URLField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    expiry_time = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return f'{self.invoice_id} - {self.short_url}'