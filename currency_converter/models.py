import os

from django.db import models

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ProfilePosts(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    photo = models.ImageField(upload_to="profile_posts/%Y/%m/%d", blank=True, null=True, verbose_name=_("photo"))
    created = models.DateTimeField(verbose_name=_("created"), default=timezone.now)

    class Meta:
        verbose_name = _("profile post")
        verbose_name_plural = _("profile posts")

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.photo:
            file_path = os.path.join(settings.MEDIA_ROOT, self.photo.path)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Call the "real" delete() method
        super().delete(*args, **kwargs)


class Currencies(models.Model):
    name = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.name
