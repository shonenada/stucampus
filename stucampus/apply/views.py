#-*- coding: utf-8 -*-
from datetime import date, timedelta

from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render

from stucampus.apply.place_config import places


class Index(View):
    def get(self, request):
        return render(request, 'apply/index.html')


class PlaceList(View):
    def get(self, request):
        return render(request, 'apply/place_list.html')


class Show(View):
    '''场地申请系统要不要这么繁琐，哭给你看啊!~~~~'''
    def get(self, request, place):
        if place not in places.keys():
            return HttpResponse(status=404)
        request_place = places[place]
        days = []
        today = date.today()
        for diff in range(0, 7):
            delta = timedelta(diff)
            days.append(today + delta)
        return render(request, 'apply/show.html',
                      {'place': request_place, 'days': days})
