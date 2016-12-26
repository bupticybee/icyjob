from django.db import models

# Create your models here.

class JobModel(models.Model):
	class Meta:
		db_table = 'jobinfo'
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=100)
	url = models.CharField(max_length=200,db_index=True)
	email = models.CharField(max_length=100)
	content = models.TextField()
	time = models.DateTimeField(db_index=True)
	type = models.CharField(max_length=10,db_index=True)
	jobtag = models.CharField(max_length=10,db_index=True)
	tags = models.TextField()
	
class TagModel(models.Model):
	class Meta:
		db_table = 'tag'
	id = models.AutoField(primary_key=True)
	tag = models.CharField(max_length=20)

class JobTagModel(models.Model):
	class Meta:
		db_table = 'jobtag'
	url = models.CharField(max_length=200,primary_key=True)
	time = models.DateTimeField(db_index=True)
	tagid = models.IntegerField()
	type = models.CharField(max_length=10,db_index=True)
