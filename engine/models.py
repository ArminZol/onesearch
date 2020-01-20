from django.db import models

# Create your models here.
class Document(models.Model):
	doc_id = models.DecimalField('ID', primary_key=True, max_digits=1000, decimal_places=0)
	title = models.TextField('Title')
	description = models.TextField('Description', blank=True, null=True)

	def __str__(self):
		return self.title