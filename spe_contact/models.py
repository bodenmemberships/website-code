from django.db import models
from spe_blog.models import Publication


# Create your models here.
class PublicationSubscription(models.Model):
    customer_id = models.CharField(max_length=12, blank=True, null=True)
    publication = models.ForeignKey(Publication)
    email = models.EmailField()

    def __unicode__(self):
        return self.publication.code + ": " + self.email
