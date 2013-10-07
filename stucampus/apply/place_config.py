#-*- coding: utf-8 -*-
from datetime import timedelta

from stucampus.utils import strfdelta


class Place(object):

    base = timedelta(hours=0)
    TIMES_TYPE_1 = [
            {'start': 8, 'end': 12},
            {'start': 14, 'end': 17},
            {'start': 17, 'end': 22.5}
        ]
    TIMES_TYPE_2 = [{'start': 8, 'end': 12}, {'start': 14, 'end': 17}]
    TIMES_TYPE_3 = [{'start': 8 + s, 'end': 8 + s + 1} for s in range(0, 12)]
    TIMES_TYPE_4 = [{'start': 8 + s, 
                     'end': 8 + (s + 1) * 0.5} for s in range(0, 31)]

    """A base model of each campus places"""
    def __init__(self, name, allow_times):
        """Initialize model

        :param name: the name of place
        :param allow_times: times which allow to apply for
        """
        self.name = name
        self.allow_times = allow_times
        self.parse()

    def parse(self):
        self.times = []
        for t in self.allow_times:
            start = timedelta(hours=t['start']) - self.base
            end = timedelta(hours=t['end']) - self.base
            format_start = strfdelta(start, "%H:%M")
            format_end = strfdelta(end, "%H:%M")
            self.times.append("%s - %s" % (format_start, format_end))


SOUTH_GYM = (Place(name=u'南区运动广场二楼', allow_times=Place.TIMES_TYPE_1),)
STU_CENTER = (
        Place(name=u'学生活动中心前广场', allow_times=Place.TIMES_TYPE_1),
        Place(name=u'一楼影视报告厅', allow_times=Place.TIMES_TYPE_1),
        Place(name=u'学生活动中心三楼天台（东）',
              allow_times=Place.TIMES_TYPE_1),
        Place(name=u'学生活动中心三楼天台（西）',
              allow_times=Place.TIMES_TYPE_1),
        Place(name=u'石头坞广场', allow_times=Place.TIMES_TYPE_1),
    )
CAMPUS = (
        Place(name=u'A座文化大厅', allow_times=Place.TIMES_TYPE_2),
        Place(name=u'CD座文化长廊', allow_times=Place.TIMES_TYPE_2),
        Place(name=u'西南餐厅前空地', allow_times=Place.TIMES_TYPE_2),
        Place(name=u'荔山餐厅前空地', allow_times=Place.TIMES_TYPE_2),
        Place(name=u'文山湖路口', allow_times=Place.TIMES_TYPE_3),
        Place(name=u'桂庙路口', allow_times=Place.TIMES_TYPE_3),
        Place(name=u'西南餐厅前空地', allow_times=Place.TIMES_TYPE_3),
        Place(name=u'荔山餐厅前空地', allow_times=Place.TIMES_TYPE_3),
    )
MEETING_ROOM = (
        Place(name=u'石头坞一楼会议室', allow_times=Place.TIMES_TYPE_4),
        Place(name=u'石头坞二楼会议室', allow_times=Place.TIMES_TYPE_4),
        Place(name=u'学生活动中心305会议室', allow_times=Place.TIMES_TYPE_4),
        Place(name=u'学生活动中心307会议室', allow_times=Place.TIMES_TYPE_4),
    )


places = {
    'south-gym': {'name': u'南区运动广场二楼', 'sub_places': SOUTH_GYM},
    'stu-center': {'name': u'学生活动中心', 'sub_places': STU_CENTER},
    'campus': {'name': u'校园文化活动露天场地', 'sub_places': CAMPUS},
    'meeting-room': {'name': u'会议室', 'sub_places': MEETING_ROOM}
}
