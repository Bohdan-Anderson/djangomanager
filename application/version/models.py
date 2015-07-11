from django.db import models
from django.template.defaultfilters import slugify


class Project(models.Model):
	title = models.CharField(max_length=500,blank=True,null=True)
	location = models.TextField(max_length=1000,blank=True,null=True)
	created = models.DateTimeField(auto_now=True)
	editable = models.DateTimeField(blank=True,null=True)
	slug = models.SlugField(blank=True)

	def save(self,*args, **kwargs):
		self.slug = slugify(self.title)
		super(Project, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title