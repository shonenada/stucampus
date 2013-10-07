import json
import urllib2
from string import Template

from django.http import HttpResponse


def render_json(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


def spec_json(status='Error', messages=None):
    if not messages:
        messages = []
    elif not isinstance(messages, (list, tuple)):
        messages = [messages]
    data = {'status': status, 'messages': messages}
    return render_json(data)


def get_client_ip(request):
    '''Get the ip of client'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def strfdelta(tdelta, fmt):
    """Format timedelta object"""
    class DeltaTemplate(Template):
        delimiter = "%"
    def save_zero(n):
        return '0' + str(n) if n < 10 else n

    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    d['H'] = save_zero(d['H'])
    d['M'] = save_zero(d['M'])
    d['S'] = save_zero(d['S'])
    t = DeltaTemplate(fmt)
    return t.substitute(**d)
