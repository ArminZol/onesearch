from django.db import models

# Create your models here.
class Document(models.Model):
	doc_id = models.DecimalField('ID', primary_key=True, max_digits=1000, decimal_places=0)
	title = models.TextField('Title')
	description = models.TextField('Description', blank=True, null=True)

	def __str__(self):
		return self.title


class Word(models.Model):
	word = models.CharField('Word', primary_key=True, max_length=50)

	def __str__(self):
		return self.word

class DocumentWord(models.Model):
	document = models.ForeignKey('Document', null=False, on_delete=models.CASCADE)
	word = models.ForeignKey('Word', null=False, on_delete=models.PROTECT)
	frequency = models.DecimalField('Frequency of Word in Document', max_digits=100, decimal_places=0)