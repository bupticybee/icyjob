from django.conf.urls import include, url
from web import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'icyjob.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index,name='index'),
    url(r'^article$', views.article,name='article'),
    url(r'^api/article$', views.api_article,name='api_article'),
    url(r'^api/article_raw$', views.api_article_raw,name='api_article_raw'),
    url(r'^api/tags$', views.api_tags,name='api_tags'),
    #url(r'^admin/', include(admin.site.urls)),
]
