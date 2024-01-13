from django.db import models


class Currencies(models.Model):
	name = models.CharField(max_length=3)

	class Meta:
		verbose_name_plural = "Currencies"

	def __str__(self):
		return self.name
