"""
author:
sources:
description:
"""

import arrow
from dateutil import tz

class timeblock:

    def __init__(self):
        self.start = None
        self.end = None
        self.type = None
        self.summary = 'none'
    
    def __init__(self, first, last, aType, summ):
        self.start = first
        self.end = last
        self.type = aType
        self.summary = summ

    def setStart(self, begin):
        self.start = begin

    def setEnd(self, last):
        self.end = last

    def setType(self, category):
        self.type = category

    def setSummary(self, description):
        self.summary = description

    def setCalSum(self, calsum):
        self.calSum = calsum 

###################################
# make list of days between range
def getDayList(beginDate, endDate):
    daysList = []
    
    # turn into arrow objects to use 'range'
    begin = arrow.get(beginDate)
    end = arrow.get(endDate)
    
    # make day for each span in range
    for begintime in arrow.Arrow.range('day', begin, end):
        day = {}
        freetime = timeblock(begintime.isoformat(), begintime.ceil('day').isoformat(), 'free', 'free time')
        day['start'] = begintime.isoformat()
        day['end'] = begintime.ceil('day').isoformat()
        blocks = []
        blocks.append(freetime)
        day['agenda'] = blocks 
        daysList.append(day)
    
    return daysList

############################
# consolidate all events into one 'agenda'
def populateDaysAgenda(daysList, eventsByCalSum):
    
    daysAgenda = []
    for day in daysList:
        daysAgenda.append(day)

    for calSum, eventList in eventsByCalSum.items():
        for count, day in enumerate(daysList):
            
            # make copy of passed daylist
            newDay = {}
            for name, entry in day.items():
                newDay[name] = entry
           
            for event in eventList:
                # create arrow objects for comparisons
                eventStart = arrow.get(event.start)
                eventEnd = arrow.get(event.end)
                dayStart = arrow.get(day['start'])
                dayEnd = arrow.get(day['end'])
                
                # event within boundaries of day
                if eventEnd <= dayEnd and eventStart >= dayStart:
                    newDay = cutUpFreeTime(day, event)
            daysAgenda[count] = newDay
    
    # make sure entries in presentable form
    for days in daysAgenda:
        days['agenda'] = sortByDates(days['agenda'])
        days['agenda'] = freeTimeMaint(days['agenda'])
    return daysAgenda

#######################
# splits events longer than a day that don't start or end on ceil or floor
def splitLongEvent(event):
    newEvent = timeblock(event.start,
                         arrow.get(event.start).ceil('day').isoformat(),
                         event.type,
                         event.summary)
    newList = []
    newList.append(newEvent)
    eventEndTime = arrow.get(event.end)
    indexTime = arrow.get(event.start)
    indexTime = indexTime.shift(days=1)
    indexTime = indexTime.floor('day')
    
    while indexTime != eventEndTime.floor('day'):
        newEvent = timeblock(indexTime.isoformat(),
                             indexTime.ceil('day').isoformat(),
                             event.type,
                             event.summary)
        newList.append(newEvent)
        indexTime = indexTime.shift(days=1)
        indexTime = indexTime.floor('day')
    
    # when loop terminates, at beginning of correct day
    newEvent = timeblock(indexTime.isoformat(),
                         event.end,
                         event.type,
                         event.summary)
    newList.append(newEvent)
    return newList

#######################
# split short multiple-day events
def splitShortEvent(event):
    initialEvent = timeblock(event.start,
                             arrow.get(event.start).ceil('day').isoformat(),
                             event.type,
                             event.summary)
    secondEvent = timeblock(arrow.get(event.end).floor('day').isoformat(),
                            event.end,
                            event.type,
                            event.summary)
    newEventList = []
    newEventList.append(initialEvent)
    newEventList.append(secondEvent)
    return newEventList

#######################
# split multi day event (on ceil and floor)
def splitMultiDay(event):
    eventStart = arrow.get(event.start).replace(tzinfo=tz.tzlocal())
    eventEnd = arrow.get(event.end).replace(tzinfo=tz.tzlocal())
    splitEvent = []
    for ranges in arrow.Arrow.span_range('day', eventStart, eventEnd):
        newEvent = timeblock(ranges[0].isoformat(), ranges[1].isoformat(), event.type, event.summary)
        splitEvent.append(newEvent)
    
    return splitEvent

#######################
# function not used for current implementation, but possibly for future (partly operational)
def populateDaysAgendaByCal(daysAgenda, eventsByCalSum):
    
    ##### create new lists/dicts ######
    # daysAgendaByCal = { 'alSum': daysAgenda[{day},{day}], 'calSum2': daysAgenda[{},{}]}
    daysAgendaByCal = {}
    
    ##### for each list of events organized by calendar summary #####
    # eventsByCalSum = {'calendar summary': [event, event...] }
    for calSum, eventList in eventsByCalSum.items():
        #######
        # daysAgenda = [{'start': [datetime iso], 'end': [datetime iso], 'agenda': [free, event, free...], { 'start':...}]
        #              = list of days chosen from range selected
        #######
        
        daysAgendaByCal[calSum] = getDayList(daysAgenda[0]['start'], daysAgenda[-1]['end'])
        
        for count, day in enumerate(daysAgendaByCal[calSum]):
            newDay = {}
            for event in eventList:
                eventStart = arrow.get(event.start)
                eventEnd = arrow.get(event.end)
                dayStart = arrow.get(day['start'])
                dayEnd = arrow.get(day['end'])
                
                # event within boundaries of day
                if eventEnd <= dayEnd and eventStart >= dayStart:
                    newDay = cutUpFreeTime(day, event)
                    daysAgendaByCal[calSum][count] = newDay
    #temporary debugging statement
    """ 
    for calsums, agenda in daysAgendaByCal.items():
        print('CALENDAR SUMMARY: ', calsums)
        print('##############################################')
        for days in agenda:
            print('DAY: ', days)
            for entries, values in days.items():
                if entries is 'agenda':
                    for stuff in values:
                        print('STUFF: ', stuff)
                        print('TYPE:  ', stuff.type)
                        print('START: ', stuff.start)
                        print('END:   ', stuff.end)
                        print('-------------------------------')
    
    return daysAgendaByCal
    """

###################################
# essentially creates new freetime blocks
def cutUpFreeTime(day, event):

    # get event times for comparison
    eventStart = arrow.get(event.start)
    eventEnd = arrow.get(event.end)

    # make new day entry
    newDay = {}
    for name, entry in day.items():
        newDay[name] = entry;
    
    # prepare new freetime block
    newFreeTime = None

    #find correct freetime block
    for index, timeBlock in enumerate(newDay['agenda']):
        if timeBlock.type is 'free':
            freeStart = arrow.get(timeBlock.start)
            freeEnd = arrow.get(timeBlock.end)
            
            ##### 5 cases, precedence is in order of earliest theoretical start time  #####
            # 1. beginning of freetime between event start and end
            if eventStart <= freeStart and eventEnd >= freeStart:
                timeBlock.start = event.end
                if freeEnd <= eventEnd:
                    del newDay['agenda'][index]
            # 2. event start and end beetween freetime start and end
            elif eventStart > freeStart and eventEnd < freeEnd:
                newFreeTime = timeblock(eventEnd.isoformat(), timeBlock.end, 'free', 'free time')
                timeBlock.end = eventStart.isoformat()
            # 3. end of freetime between event start and end
            elif eventStart <= freeEnd and eventEnd > freeEnd:
                timeBlock.end = event.start 
            # 4. event bigger than freetime
            elif eventStart <= freeStart and eventEnd >= freeEnd:
                del newDay['agenda'][index]
           # 5. move to next block(takes places of else statement)

    # append with event
    newDay['agenda'].append(event)
    
    # add newly created freetime to end of list, if created
    if newFreeTime:
        newDay['agenda'].append(newFreeTime)
    
    return newDay

##################################################
# maintenance to fix overlapping event or free end times
def freeTimeMaint(aAgenda):
    agenda = []
    for entry in aAgenda:
        agenda.append(entry)

    for count, timeBlock in enumerate(agenda):
        if timeBlock.type is 'event':
            # determine indices for event and what's next block
            eventIndex = count
            #if last in list
            if eventIndex + 1 == len(agenda):
                break
            index = count + 1
            while index != len(agenda):
                if agenda[index].type is 'free':
                    freeStart = arrow.get(agenda[index].start)
                    freeEnd = arrow.get(agenda[index].end)
                    eventEnd = arrow.get(agenda[eventIndex].end) 
                    if freeStart < eventEnd and freeEnd < eventEnd:
                        del agenda[index]   
                    elif eventEnd > freeStart and eventEnd < freeEnd:
                        agenda[index].start = agenda[eventIndex].end
                index += 1
        # if block type is free
        else:
            # check if freetime time length < 1 minute
            time = arrow.get(timeBlock.end) - arrow.get(timeBlock.start) 
            if time.seconds <= 60:
                del agenda[count]
                continue
            freeIndex = count
            #if last in list
            if freeIndex + 1 == len(agenda):
                break
            index = count + 1
            while index != len(agenda):
                if agenda[index].type is 'event':
                    eventStart = arrow.get(agenda[index].start)
                    eventEnd = arrow.get(agenda[index].end)
                    freeEnd = arrow.get(agenda[freeIndex].end) 
                    if freeEnd > eventStart:
                        agenda[freeIndex].end = agenda[index].start
                index += 1
    return agenda 

##################################################
# to sort by start time 
def sortByDates(agenda):
    blockSort = []
    for block in agenda:
        blockSort.append(arrow.get(block.start))
    
    sortedBlocks = []
    blockSort.sort()
    for index, time in enumerate(blockSort):
        
        for blocks in agenda:
            if arrow.get(blocks.start) == time:
                sortedBlocks.append(blocks)
 
    return sortedBlocks

def spanGreaterThanDay(start, end):
    
    time = end - start
    print(time.days)
    if time.days >= 1:
        return True
    else:
        return False
