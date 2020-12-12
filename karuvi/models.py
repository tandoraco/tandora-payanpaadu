from django.db import models


# This model is to test the working of storage backend defined in payanpaadu app.
class Profile(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    picture = models.ImageField(null=False, blank=False)

    def __str__(self):
        return self.name
