"""
author:
sources:
description:
"""

import arrow

class timeblock:

    def __init__(self):
        self.start = None
        self.end = None
        self.type = None
        self.summary = None
    """
    def set(self, first, last, category, desc=None):
        self.start = first
        self.end = last
        self.type = category
        self.summary = desc if desc else None
   """
    def setStart(self, begin):
        self.start = begin

    def setEnd(self, last):
        self.end = last

    def setType(self, category):
        self.type = category

    def setSummary(self, description):
        self.summary = description

    def setCalId(self, calid)
        self.calId = calid

###################################
# other funcs

# make list of days between range
def getDayList(beginDate, endDate):
    daysList = []
    begin = arrow.get(beginDate)
    end = arrow.get(endDate)
    
    for begintime, endtime in arrow.Arrow.span_range('day', begin, end):
        day = {}
        #events = ['chea bro', 'uknoit' ]
        begintime = arrow.get(begintime)
        freetime = timeblock()
        freetime.setStart(begintime)
        freetime.setEnd(endtime)
        freetime.setType('free')
        freetime.setSummary('free time')
        #print(freetime.start, freetime.end, freetime.type, freetime.summary)
        day['start'] = begintime
        day['end'] = endtime
        blocks = []
        day['events'] = blocks
        day['events'].append(freetime)
        daysList.append(day)
        #print(day)
 
    return daysList

def populateDayList(dayList, events):

    dayListByCal = []
    for calSum in events:
        for events in calSum:
            for day in dayList:
                
