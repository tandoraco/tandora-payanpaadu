from django.db import models


class CustomDomain(models.Model):
    instance = models.OneToOneField('Instance', on_delete=models.CASCADE)
    custom_domain = models.CharField(max_length=200, unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.instance} -  {self.custom_domain}'
