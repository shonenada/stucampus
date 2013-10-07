from django.conf.urls import patterns, url

from stucampus.apply.views import Index, PlaceList, Show


urlpatterns = patterns(
    '',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^place$', PlaceList.as_view(), name='PlaceList'),
    # url(r'^place/south-gym$', SouthGym.as_view(), name='place-south-gym')
    url(r'^place/(?P<place>[a-z-]+?)$', Show.as_view(), name='place-show'),
)
