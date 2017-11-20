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
    """
    def setCalId(self, calid):
        self.calId = calid
    """
###################################
# other funcs

# make list of days between range
def getDayList(beginDate, endDate):
    daysList = []
    begin = arrow.get(beginDate)
    end = arrow.get(endDate)
    print('END DATE: ', end)
    for begintime in arrow.Arrow.range('day', begin, end):
        day = {}
        freetime = timeblock(begintime.isoformat(), begintime.ceil('day'), 'free', 'free time')
        day['start'] = begintime.isoformat()
        day['end'] = begintime.ceil('day').isoformat()
        blocks = []
        blocks.append(freetime)
        day['agenda'] = blocks 
        daysList.append(day)
    print('GET DAYS: ', daysList)
    return daysList

def populateDaysAgenda(daysList, eventsByCalSum):
    
    daysAgenda = []
    for day in daysList:
        daysAgenda.append(day)

    for calSum, eventList in eventsByCalSum.items():
        #daysAgenda = []

        for count, day in enumerate(daysList):
            newDay = {}
            for name, entry in day.items():
                newDay[name] = entry
            
            for event in eventList:
                eventStart = arrow.get(event.start)
                eventEnd = arrow.get(event.end)
                dayStart = arrow.get(day['start'])
                dayEnd = arrow.get(day['end'])
                
                # event within boundaries of day
                if eventEnd <= dayEnd and eventStart >= dayStart:
                    """
                    print('CALENDAR SUMMARY: ', calSum)
                    print('BEFORE PASS: ', day)
                    for stuff in day['agenda']:
                        print('STUFF: ', stuff)
                        print('TYPE:  ', stuff.type)
                        print('START: ', stuff.start)
                        print('END:   ', stuff.end)
                        print('-------------------------------')
                    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&') 
                    """
                    #newDay = {}
                    newDay = cutUpFreeTime(day, event)
                    """
                    print('AFTER PASS: ', newDay) 
                    for stuff in newDay['agenda']:
                        print('STUFF: ', stuff)
                        print('TYPE:  ', stuff.type)
                        print('START: ', stuff.start)
                        print('END:   ', stuff.end)
                        print('-------------------------------')
                    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&') 
                    """
            daysAgenda[count] = newDay
    for days in daysAgenda:
        days['agenda'] = sortByDates(days['agenda'])
        days['agenda'] = freeTimeMaint(days['agenda'])
    return daysAgenda


def populateDaysAgendaByCal(daysAgenda, eventsByCalSum):
    """create new lists/dicts"""
    # daysAgendaByCal = { 'alSum': daysAgenda[{day},{day}], 'calSum2': daysAgenda[{},{}]}
    daysAgendaByCal = {}
    """for each list of events organized by calendar summary""" 
    # eventsByCalSum = {'calendar summary': [event, event...] }
    for calSum, eventList in eventsByCalSum.items():
        #######
        # daysAgenda = [{'start': [datetime iso], 'end': [datetime iso], 'agenda': [free, event, free...], { 'start':...}]
        #              = list of days chosen from range selected
        #######
        """
        1. go through each event in each list and place into appropriate day in list of days. 
        """
        #for count, day in enumerate(daysAgendaByCal[calSum]):
        # create new days agenda for each calendar
        #newDaysAgenda = getDayList(daysAgenda[0]['start'], daysAgenda[-1]['end']) 
        daysAgendaByCal[calSum] = getDayList(daysAgenda[0]['start'], daysAgenda[-1]['end'])
        #print('-----newDaysAgenda: ', newDaysAgenda)
        #daysAgendaByCal[calSum] = newDaysAgenda
        for count, day in enumerate(daysAgendaByCal[calSum]):
            newDay = {}
            for event in eventList:
                eventStart = arrow.get(event.start)
                eventEnd = arrow.get(event.end)
                dayStart = arrow.get(day['start'])
                dayEnd = arrow.get(day['end'])
                """
                # all day event:
                # REQ: set freetime endtime to beginning of event start
                if eventStart == dayStart:

                    # find num of days
                    numOfDays = eventEnd.day - eventStart.day
                    while numOfDays != 0:
                        

                # event goes from one day to another
                else if

                """
                # event within boundaries of day
                if eventEnd <= dayEnd and eventStart >= dayStart:
                    """
                    print('CALENDAR SUMMARY: ', calSum)
                    print('BEFORE PASS: ', day)
                    for stuff in day['agenda']:
                        print('STUFF: ', stuff)
                        print('TYPE:  ', stuff.type)
                        print('START: ', stuff.start)
                        print('END:   ', stuff.end)
                        print('-------------------------------')
                    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&') 
                    """
                    newDay = cutUpFreeTime(day, event)
                    """
                    print('AFTER PASS: ', newDay) 
                    for stuff in newDay['agenda']:
                        print('STUFF: ', stuff)
                        print('TYPE:  ', stuff.type)
                        print('START: ', stuff.start)
                        print('END:   ', stuff.end)
                        print('-------------------------------')
                    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&') 
                    """
                    daysAgendaByCal[calSum][count] = newDay
                    #day = newDay
                    #print('NEWDAY INFO: ', newDay)
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

""" logic for inserting into agenda """
def cutUpFreeTime(day, event):

    # get event times for comparison
    eventStart = arrow.get(event.start)
    eventEnd = arrow.get(event.end)

    # make new day entry
    newDay = {}
    for name, entry in day.items():
        newDay[name] = entry;
    #newDay['start'] = day['start'] 
    #newDay['end'] = day['end']
    #newDay['agenda'] = day['agenda']
    #newDay = day
    #find correct freetime block
    newFreeTime = None
    for index, timeBlock in enumerate(newDay['agenda']):
        if timeBlock.type is 'free':
            freeStart = arrow.get(timeBlock.start)
            freeEnd = arrow.get(timeBlock.end)
            # 4 cases, precedence is in order of earliest theoretical start time
            # beginning of freetime between event start and end
            if eventStart <= freeStart and eventEnd >= freeStart:
                timeBlock.start = event.end
                if freeEnd <= eventEnd:
                    del newDay['agenda'][index]
            # event start and end beetween freetime start and end
            elif eventStart > freeStart and eventEnd < freeEnd:
                newFreeTime = timeblock(eventEnd.isoformat(), timeBlock.end, 'free', 'free time')
                timeBlock.end = eventStart.isoformat()
            # end of freetime between event start and end
            elif eventStart <= freeEnd and eventEnd > freeEnd:
                timeBlock.end = event.start 
            # event bigger than freetime
            elif eventStart <= freeStart and eventEnd >= freeEnd:
                del newDay['agenda'][index]
    newDay['agenda'].append(event)
    if newFreeTime:
        newDay['agenda'].append(newFreeTime)
    #newDay['agenda'] = sortByDates(newDay['agenda'])
    #newDay['agenda'] = freeTimeMaint(newDay['agenda'])
    #newDay['agenda'] = sortByDates(newDay['agenda'])
    
    return newDay

""" maintenance to see if freetime under any inserted event """
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
            index = eventIndex + 1
            while index != len(agenda) - 1:
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
            freeIndex = count
            #if last in list
            if freeIndex + 1 == len(agenda):
                break
            index = freeIndex + 1
            while index != len(agenda) - 1:
                if agenda[index].type is 'event':
                    eventStart = arrow.get(agenda[index].start)
                    eventEnd = arrow.get(agenda[index].end)
                    freeEnd = arrow.get(agenda[freeIndex].end) 
                    if freeEnd > eventStart and freeEnd < eventEnd:
                        agenda[freeIndex].end = agenda[index].start
                index += 1

    return agenda 

# sorting 
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

def differenceCheck(start, end):
    time = end - start
    print('SECONDS PRINT ------------------------------------------', time.seconds)
