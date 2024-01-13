from django.db import models


class Country(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)

	class Meta:
		verbose_name_plural = "Countries"

	def __str__(self):
		return self.name

class City(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	url = models.CharField(max_length=256)
	country = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = "Cities"

	def __str__(self):
		return self.name

class WorldCountries(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		verbose_name_plural = "WorldCountries"

	def __str__(self):
		return self.name