from django.db import models

# Create your models here.
SOCIAL_CHOICES = (
    ('F', 'Facebook'),
    ('W', 'Whatsapp'),
    ('T', 'Twitter'),
    ('I', 'Instagram'),
    ('L', 'LinkedIn'),
    ('Y', 'Youtube'),
)

class SocialLink(models.Model):
    site = models.CharField(choices=SOCIAL_CHOICES, max_length=1,)
    link = models.URLField()

    def __str__(self):
        return dict(SOCIAL_CHOICES).get(self.site, self.link)

    def save(self,*args, **kwargs):
        social_link_qs = SocialLink.objects.filter(site=self.site)
        if social_link_qs.exists():
            self.id = social_link_qs.first().id
        super(SocialLink, self).save(*args, **kwargs)