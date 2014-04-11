from django.conf.urls import patterns, include, url

from stucampus.szuspeech.views import index,manage_list,del_resource, set_top,ModifyResorceView, AddResourceView


urlpatterns = patterns('',
	url(r'^$',index,name = 'index'),
	url(r'^manage/$', manage_list, name='manage_list'),
    url(r'^manage/upload/$', AddResourceView.as_view(), name='add'),
    url(r'^manage/edit/$', ModifyResorceView.as_view() , name='edit'),
    url(r'^manage/del/$', del_resource, name='del_resource'),
    url(r'^manage/settotop/$', set_top, name='set_top'),
)