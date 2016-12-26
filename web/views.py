from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Q
from .models import *
import urllib
import json
# Create your views here.


def index(request):
	result = JobModel.objects.order_by('-time')[:10]
	tags = TagModel.objects.all()
	tags = sorted(tags,key=lambda i:i.tag)
	for i in result:
		proto, rest = urllib.splittype(i.url)
		res, rest = urllib.splithost(rest)
		if res and res[:2] == 'm.':
			res = res[2:]
		i.urldomain = "unkonw" if not res else res
	return render(request,'views/index.html',{'articles':result,'tags':tags})

def article(request):
	id = request.REQUEST.get('id')

	if id == None:
		template = loader.get_template('views/article.html')
		return HttpResponse(template.render())

	id = int(id)
	
	article = JobModel.objects.get(id=id)
	if article != None:
		article.content = article.content.replace('\n', '<br />')
	return render(request,'views/article.html',{'article':article})

def api_tags(request):
	tags = TagModel.objects.all()
	result = []
	for tag in tags:
		item = {
			'id':tag.id,
			'tag':tag.tag.replace("_"," "),
		}
		result.append(item)
 	result = sorted(result,key=lambda i:i['tag'])
	return HttpResponse(json.dumps(result),'application/json')

def api_article_raw(request):
	id = request.REQUEST.get('id')
	assert(id != None)
	id = int(id)
	
	article = JobModel.objects.get(id=id)
	assert(article != None)
	if article != None:
		#article.content = article.content.replace('\n', '<br />')
		pass
	result = {
		'content':article.content,
		'id':article.id,
		'title':article.title,
		'email':article.email,
		'type':article.type,
		'jobtag':article.jobtag,
		'tags':article.tags,
	}
	result = json.dumps(result)
	return HttpResponse(result,'application/json')

def api_article(request):
	offset = request.REQUEST.get('offset')
	offset = int(offset)

	alltype = request.REQUEST.get('alltype','')

	alltype = alltype.split(',')
	jobtype = alltype[0] if alltype else None
	tags = alltype[1:]
	extrainfos = {}

	if not tags:
		if jobtype:	
			results = JobModel.objects.filter(type=jobtype).order_by('-time')[offset:offset + 10]

		else:
			results = JobModel.objects.order_by('-time')[offset:offset + 10]
	else:
		# TODO change these disgusting code
		q = None
		for tag in tags:
			tag = int(tag)
			q = Q(tagid=tag) if q == None else q | Q(tagid=tag)
		if jobtype:
			if q == None:
				q = Q(type=jobtype)
			else:
				q = q & Q(type=jobtype)

		tagjobobjs = JobTagModel.objects.filter(q).order_by('-time')[offset:offset + 10]
		if not tagjobobjs:
			results = []
		else:
			q_url = Q(url='whatever')
			for tagjobobj in tagjobobjs:
				q_url = q_url | Q(url=tagjobobj.url)
			if jobtype:
				q_url = Q(type=jobtype) if q_url == None else q_url & Q(type=jobtype)
			results = JobModel.objects.filter(q_url).order_by('-time')

	# ret vals
	retvals = []
	for result  in results:
		title = result.title
		# get main domain
		proto, rest = urllib.splittype(result.url)
		res, rest = urllib.splithost(rest)
		if res and res[:2] == 'm.':
			res = res[2:]
		domain = "unkonw" if not res else res
		id = result.id
		url = result.url
	
		time = result.time
		item = {
			'id':id,
			'title':title,
			'domain':domain,
			'time':str(time),
			'url':url,
			'extra':extrainfos,
		}
		retvals.append(item)
	return HttpResponse(json.dumps(retvals),'application/json')




