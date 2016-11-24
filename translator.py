'''
author : Praveen Kumar Bodigutla
'''
from __builtin__ import staticmethod
from datetime import datetime
from datetime import date
import calendar

'''
Examples for tags and corresponding values
<TDSS>:['days', 'hours', 'day', 'soon', 'chance', 'time', 'last', 'left', 'hour', 'limited', 'deal', 'flash', 'friday', 'call', 'tomorrow', 'weekend', 'hrs', 'week', 'period', 'break', 'hr', 'out', 'minute']
<TPRD>:['everyday', 'fridays', 'tuesday', 'daily', 'day']
<ETPZ>:['et', 'pt', 'ct', 'est', 'cst', 'pdt', 'pst', 'edt', 'pacific', 'central', 'time']
<ETPHN>:['DIGIT']
<ETPHS>:['midnight', 'tonight', 'sunday', 'twilight', 'noon', 'midday', 'hours', 'hour', 'close']
<BTPYN>:['DIGIT']
<BTPAP>:['am', 'pm']
<TDPS>:['final', 'president', 'last', 'one', 'ending', 'limited', 'same', 'supplies', 'DIGIT', 'earth', 'ends', 'hours', 'all', 'flash', 'mother', 'few', 'four', 'two', 'quantites', 'mothers', 'valentine', 'black', 'eod', 'week', 'quantities', 'day', 'days', 'this', 'fools', 'spring', 'running', 'patrick', 'limted']
<BTPZ>:['pt', 'et', 'est', 'edt', 'pacific', 'pst', 'ct']
<ETPMN>:['DIGIT']
<BTPMS>:['august', 'march', 'september', 'april', 'february', 'july', 'aug', 'october']
<BTPmN>:['DIGIT']
<BTPDS>:['now', 'today', 'tomorrow', 'tuesday', 'monday', 'mon', 'sat', 'thursday', 'wednesday', 'saturday', 'friday', 'thurs', 'fri']
<BTPMN>:['DIGIT']
<ETPAP>:['pm', 'am']
<ETPYN>:['DIGIT']
<ETPmN>:['DIGIT']
<BTPHS>:['now', 'midday', 'noon', 'midnight']
<TDPN>:['DIGIT']
<BTPHN>:['DIGIT']
<ETPDN>:['DIGIT']
<BTPDN>:['DIGIT']
<ETPDS>:['saturday', 'tomorrow', 'thursday', 'weekend', 'today', 'sunday', 'monday', 'wednesday', 'midnight', 'tuesday', 'tonight', 'friday', 'todays', 'mothers', 'day', 'presidents', 'march']
<ETPMS>:['march', 'february', 'august', 'mar', 'september', 'december', 'april', 'may', 'october', 'feb', 'november', 'jan', 'july', 'aug', 'apr']'''

import time
from datetime import date
import datetime
from abc import ABCMeta
from time import mktime
from datetime import timedelta
import copy
from utils import utils

timeStringAlias = {
             'days' : 'day',
             'hours' : 'hour',
             'minutes' : 'minute',
             'hrs' : 'hour',
             'hours':'hour',
             'hr' : 'hour',
             'second' : 'second',
             'sec' : 'second',
             'minute' : 'minute',
             'hour' : 'hour',
             'day' : 'day',
             'min' : 'minute',
             'year' : 'year',
             'years' : 'year',
             'yr' : 'year',
             'tomorrow' :'tomorrow',
             'tom' : 'tomorrow',
             'eod' : 'day',
             'midday' : 'noon',
             'noon' : 'noon',
             'now'  : 'now',
             'midnight' : 'midnight',
             'period' : 'day',
             'month' : 'month',
             'saturday':'saturday',
             'sunday' : 'sunday',
             'sun' : 'sunday',
             'sat' : 'saturday',
             'mon' : 'monday',
             'monday' : 'monday',
             'tuesday' : 'tuesday',
             'tue' : 'tuesday',
             'wed' : 'wednesday',
             'thu' : 'thursday',
             'thurs':'thursday',
             'fri' : 'friday',
             'wednesday' : 'wednesday',
             'thursday' : 'thursday',
             'friday' : 'friday',
             'january' : 'january',
             'jan' : 'january',
             'february' : 'february',
             'feb' : 'february',
             'mar' : 'march',
             'march' : 'march',
             'april' : 'april',
             'apr' : 'april',
             'may' : 'may',
             'june' : 'june',
             'jun' : 'june',
             'july' : 'july',
             'jul' : 'july',
             'aug' : 'august',
             'august' : 'august',
             'oct' : 'october',
             'october' : 'october',
             'sept' : 'september',
             'september' : 'september',
             'november' : 'november',
             'nov' : 'november',
             'dec' : 'december',
             'december' :'december',
             'et' : 'est',
             'pt' : 'pst',
             'pst' : 'pst',
             'pdt' : 'pst',
             'est' : 'est',
             'edt' : 'est',
             'central' : 'ct',
             'central time' : 'ct',
             'weekend' : 'weekend',
             'today' : 'day'
             }

timeStringToNumberAlias = {
                           'february' : 2,
                           'january' : 1,
                           'march' : 3,
                           'april' : 4,
                           'may' : 5,
                           'june' : 6,
                           'july' : 7,
                           'august' : 8,
                           'september' : 9,
                           'october' : 10,
                           'november' : 11,
                           'december' : 12,
                           'sunday' : 6,
                           'monday' : 0,
                           'tuesday' : 1,
                           'wednesday' : 2,
                           'thursday' : 3,
                           'friday' : 4,
                           'saturday' : 5,
                           'zero' :0,
                           'two' : 2,
                           'one' : 1,
                           'three': 3,
                           'four' : 4,
                           'five' : 5,
                           'six' : 6,
                           'seven' : 7,
                           'eight' : 8,
                           'nine' : 9,
                           }
tagTimeAlias = {
                'BTPYN' : 'year',
                'BTPMN' : 'month',
                'BTPHN' : 'hour',
                'BTPmN' : 'minute',
                'BTPDN' : 'day',
                'ETPYN' : 'year',
                'ETPMN' : 'month',
                'ETPDN' : 'day',
                'ETPHN' : 'hour',
                'ETPmN' : 'minute'
                }

AllowedValues = {                 
                 'minMonth' : 1,
                 'maxMonth' : 12,
                 'minYear'  : 2015,
                 'maxYear'  : 2016,
                 'sminYear'  : 15,
                 'smaxYear'  : 16,
                 'maxDay'   : 31,
                 'minDay'   : 1, 
                 'minMinute': 00,
                 'maxMinute' : 59,
                 'minHour'  :00,
                 'maxHour'  : 23,
                 'minSecond' : 00,
                 'maxSecond' : 59                  
                 }

# Alias from non standard time prefix suffix to standard prefix_suffix
timeDurationOffsetAliases = {
                    ('limited','time') : ('2','days'),
                    ('limited','period') : ('2','days'),
                    ('supplies','last'):('2','days'),
                    ('last', 'chance'):('1','day'),
                    ('last', 'day'):('1','day'),
                    ('last', 'minute'):('1','day'),
                    ('final', 'day'):('1','day'),
                    ('ends', 'soon'):('2','days'),
                    ('ending', 'soon'):('2','days'),
                    ('last', 'call'):('1','day'),
                    ('flash', 'sale'):('1','day'),
                    ('flash', 'deal'):('1','day'),
                    ('flash', ''):('1','day'),
                    ('running', 'out'):('1','day'),
                    ('run', 'out'):('1','day'),
                    ('same', 'day'):('1','day'),
                    ('qualtities', 'limited'):('1','day'),
                    ('all','day'):('1','day'),
                    ('eod',''):('1','day'),
                    ('few','hours'):('1','day'),
                    ('couple','hours'):('2','hours'),
                    ('couple','days'):('2','days'),
                    ('hours','left'):('1','day'),
                    ('few','days'):('7','days'),
                    ('final','hours'):('1','day'),
                    ('this', 'week'):('7','days'), #Use better offset here
                    ('', 'week'):('7','days'),
                    ('', 'day'):('1','day'),
                    ('this', 'day'):('1','day')
                }


#Replace this with standard calendar
class SpecialDaysCalendar:
    @staticmethod
    def getTimeStruct(timeTuple,beginTime):

        # (month, day) values in 2016
        specialDays = {}
        specialDays[('presidents','day')] = (2,15)
        specialDays[('president','day')] = (2,15)
        specialDays[('mothers','day')] = (5,8)
        specialDays[('mother','day')] = (5,8)
        specialDays[('valentines','day')] = (2,14)
        specialDays[('valentine','day')] = (2,14)
        specialDays[('black','friday')] = (11,25)
        specialDays[('patricks','day')] = (3,17)
        specialDays[('patrick','day')] = (3,17)
        specialDays[('spring','break')] = (4,29)
        specialDays[('spring','')] = (4,29)
        specialDays[('summer','break')] = (8,30)
        specialDays[('summer','')] = (8,30)
        specialDays[('earths','day')] = (4,22)
        specialDays[('earth','day')] = (4,22)
        
        if specialDays.has_key(timeTuple):
            (month,day) = specialDays[timeTuple]
            beginTime['month'] = month
            beginTime['day'] = day 
                
        return None
         
        
class DefaultTime:
    @staticmethod  
    def getDefaultTime():
        timestruct = {}
        today = date.today()
        timestruct['month'] = today.month
        timestruct['day'] = today.day
        timestruct['year'] = today.year
        timestruct['weekday'] = today.weekday
        timestruct['timezone'] = time.tzname[0].lower()
        timestruct['hour'] = 0
        timestruct['minute'] = 0
        timestruct['second'] = 0 
        return timestruct  
    
    @staticmethod
    def getFromDateTime(reftime):
        refdate = time.strptime(reftime, "%m/%d/%y %H:%M")
        timestruct = {}
        timestruct['month'] = refdate.tm_mon
        timestruct['day'] = refdate.tm_mday
        timestruct['year'] = refdate.tm_year
        timestruct['weekday'] = refdate.tm_wday
        timestruct['hour'] = refdate.tm_hour
        timestruct['minute'] = refdate.tm_min
        timestruct['second'] = refdate.tm_sec
        #Default Timezone
        timestruct['timezone'] = time.tzname[0].lower()
        
        return timestruct
        
class BeginEndTime:
    logger = utils.getLogger()
    def __init__(self,wordLabelTuples,referenceDate):        
        self.tagMap = {}
        durationTuples = []
        prefix = ""
        
        for t in wordLabelTuples:
            (label,word) = (t[0],t[1])
            #Remove the angled Braces around the label
            label = label[1:len(label)-1]
              
            #Get all TDPS and TDSS (prefix,suffix) tuples  
            if label == "TDSS":                    
                if prefix != "":
                    durationTuple = (prefix,word)
                    durationTuples.append(durationTuple)
                    prefix = ""
                    continue
                else:
                    BeginEndTime.logger.debug("Duration suffix without a prefix :{}".format(t))
                                        
            if label == "TDPN" or label == "TDPS":
                if prefix != "":
                     durationTuple = (prefix,'')
                     durationTuples.append(durationTuple)                                     
                prefix = word
                continue                 
                        
            self.tagMap = utils.addKeyValue(self.tagMap,label,word)
        
        if prefix != "":
            durationTuples.append((prefix,''))
                
        if len(durationTuples) != 0:
            self.tagMap["TIME_PERIOD"] = durationTuples
            
        print "printing tagmap..."
        print self.tagMap
        self.tagMap = self.__validate(self.tagMap)
        self.beginTime = self.__getBeginTime(self.tagMap, referenceDate)            
        self.endTime = self.__getEndTime(self.beginTime,self.tagMap)
        
        
    # Convert hours to 24 hour format 
    def _convertTo24(self,tagMap, hourkey, ampmKey):        
        newValues = []        
        if hourkey in tagMap.keys():
            values = tagMap[hourkey]
            for val in values:
                val = int(val)
                if ampmKey in tagMap.keys():
                    ampm = 0 # 0 for am, 1 for pm
                    if "am" in tagMap[ampmKey]:
                         ampm = 0
                    else:
                        if "pm" in tagMap[ampmKey]:
                            ampm = 1
                        
                    if ampm == 1:
                        if (val < 12 ):
                            val += 12
                newValues.append(val)
            tagMap[hourkey]= newValues            
        return tagMap
    
    #Convert year digit to a standard 4 digit format
    def _convertTo4digitYear(self,tagMap,yearKey):
        if yearKey not in tagMap.keys():
            return tagMap
        
        newValues = []        
        t = date.today()
        
        #Using the current century as the base
        yr_2 = str(t.year)[:2]
        values = tagMap[yearKey]
        for val in values:
            newVal = val
            if len(val) == 2:
                year = yr_2 + val   
                newVal = int(year)
            newValues.append(newVal)
        tagMap[yearKey] = newValues
        
        return tagMap 
            
    # calculate time stamp for (prefix,suffix) tuples  
    def __calculateDurationOffset(self,timeTuple, endTime): 
        offsetTime = SpecialDaysCalendar.getTimeStruct(timeTuple, endTime)
        if offsetTime != None:
            return offsetTime
        
        prefixstring = timeTuple[0]
        suffixString = timeTuple[1]       
        
        prefix = None        
        if timeDurationOffsetAliases.has_key(timeTuple):
            aliasTimeTuple = timeDurationOffsetAliases[timeTuple]
            prefixstring = aliasTimeTuple[0]
            suffixString = aliasTimeTuple[1]
    
        try:
            if prefixstring != "":
                if prefixstring in timeStringToNumberAlias.keys():
                    prefix = timeStringToNumberAlias[prefixstring]
                else:
                    prefix = int(prefixstring)
            else:
                prefix = int(timeTuple[0])
            
        except ValueError as v:
            BeginEndTime.logger.debug("TDP can not be converted to integer".format(v))
            return endTime
        else:      
            if suffixString in timeStringAlias.keys():
                suffixString = timeStringAlias[suffixString]+"s"
                offset = None

                if suffixString == "days":
                    #Including current day as well
                    offset = timedelta(days=(prefix-1))
                
                if suffixString == "hours":
                    offset = timedelta(hours=prefix)
                
                if suffixString == "seconds":
                    offset = timedelta(seconds=prefix)
                
                if suffixString == "months":    
                    offset = timedelta(months=prefix)
                
                if suffixString == "minutes":    
                    offset = timedelta(minutes=prefix)
                            
                stTime =  datetime.datetime(endTime['year'], endTime['month'], endTime['day'], endTime['hour'],endTime['minute'], endTime['second'])
                newDate = stTime + offset
        
                endTime['year'] = newDate.year
                endTime['month'] = newDate.month
                endTime['day'] = newDate.day
                endTime['hour'] = newDate.hour
                endTime['minute'] = newDate.minute
                endTime['second'] = newDate.second
            else:
                BeginEndTime.logger.debug("Invalid suffix:{}".format(suffixString))
                
        return endTime
    
    def __calculateDayOffset(self,beginTime,daystring,isbeginDay = True):
        if daystring == "today" or daystring == "eod" or daystring == "midnight" or daystring =="day":
            if isbeginDay:
                return beginTime
            else:
                beginTime['hour'] = 23
                beginTime['minute'] = 59
                beginTime['second'] = 59
                return beginTime
            
        if daystring == "now":
            return beginTime 
        
        if daystring == "weekend":
            if isbeginDay == True:
                daystring = "friday"
            else:
                daystring = "sunday"
        
        if daystring == "weekend":
            if isbeginDay == True:
                daystring = "monday"
            else:
                daystring = "friday" 
        
        days_ahead = 0
        if daystring == "tomorrow":
            days_ahead = 1
        else:
            try:
                weekday = timeStringToNumberAlias[daystring]
                days_ahead = weekday - beginTime["weekday"]
                if days_ahead <= 0:
                    days_ahead += 7
            except KeyError:
                BeginEndTime.logger.debug("Invalid daystring:{}".format(daystring))
    
                if isbeginDay == False:
                    #Default offset of one day
                    days_ahead = 1
                else:
                    return beginTime
                    
        d = datetime.datetime(beginTime['year'], beginTime['month'], beginTime['day'], beginTime['hour'],beginTime['minute'], beginTime['second'])
        newDate =  d + datetime.timedelta(days_ahead)
                
        beginTime['year'] = newDate.year
        beginTime['month'] = newDate.month
        beginTime['day'] = newDate.day
        beginTime['hour'] = newDate.hour
        beginTime['minute'] = newDate.minute
        beginTime['second'] = newDate.second
        beginTime['weekday'] = newDate.weekday()
        
        if isbeginDay == False:
            beginTime["hour"] = 23
            beginTime["minute"] = 59
            beginTime["second"] = 59

        return beginTime
    
    
    def __calculateHourOffset(self,beginTime,hourstring):
        if hourstring == "now":
            return beginTime
        
        if hourstring == "tonight" or hourstring=="midnight":
            beginTime['hour'] = 23
            beginTime['minute'] = 59
            beginTime['second'] = 59
            
        if hourstring == "noon":
            beginTime['hour'] = 12
            beginTime['minute'] = 0
            beginTime['second'] = 0
            
        return beginTime
    
    def __validate(self,tagMap):
        for key in tagMap.keys():
            validValues = []
            for value in tagMap[key]:
                if key[len(key)-1] == "N":                
                    try: 
                        intvalue = int(value)
                        if key == 'BTPMN' or key == "ETPMN":
                            if intvalue > AllowedValues['maxMonth'] or intvalue < AllowedValues['minMonth']:
                                raise ValueError("Invalid Month :{}".format(value))
                            else:
                                validValues.append(value)
                        elif key == 'BTPmN' or key == 'ETPmN':
                            if intvalue > AllowedValues['maxMinute'] or intvalue < AllowedValues['minMinute']:
                                raise ValueError("Invalid Minute :{}".format(value))
                            else:
                                validValues.append(value)
                        elif key == 'BTPHN' or key == 'ETPHN':
                            if intvalue > AllowedValues['maxHour'] or intvalue < AllowedValues['minHour']:
                                raise ValueError("Invalid Hour :{}".format(value))
                            else:
                                validValues.append(value)                                                
                        elif key == 'BTPDN' or key == 'ETPDN':
                            if intvalue > AllowedValues['maxDay'] or intvalue < AllowedValues['minDay']:
                                raise ValueError("Invalid Day {}".format(value))
                            else:
                                validValues.append(value)
                        elif key == 'BTPYN' or key == 'ETPYN':                            
                            if len(value) == 2:
                                if intvalue > AllowedValues['smaxYear'] or intvalue < AllowedValues['sminYear']:
                                    raise  ValueError("Invalid Year {}".format(value))
                                else:
                                    validValues.append(value)
                            elif len(value) == 4:   
                                if intvalue > AllowedValues['maxYear'] or intvalue < AllowedValues['minYear']:
                                    raise  ValueError("Invalid Year {}".format(value))
                                else:
                                    validValues.append(value)
                            else:
                                raise  ValueError("Invalid Year {}".format(value))
                        else:
                            validValues.append(value)
                                
                    except ValueError as v:
                        BeginEndTime.logger.debug("Invalid Tagmap entries {}".format(v))
                else:
                    validValues.append(value)
                    
            tagMap[key] = validValues    
                
        return tagMap
        
    def __calculateRepeat(self,beginTime,repeat,repeatFrequency = 30):
       
        beginTimes = []
        d = datetime.datetime(beginTime['year'], beginTime['month'], beginTime['day'], beginTime['hour'],beginTime['minute'], beginTime['second'])
        for i in range(repeatFrequency):
            days_ahead = 0
            if repeat == "daily":
                days_ahead = i    
            newDate =  d + datetime.timedelta(days_ahead)
            beginTimenew = copy.deepcopy(beginTime)
            beginTimenew['year'] = newDate.year
            beginTimenew['month'] = newDate.month
            beginTimenew['day'] = newDate.day
            beginTimenew['hour'] = newDate.hour
            beginTimenew['minute'] = newDate.minute
            beginTimenew['second'] = newDate.second
            beginTimes.append(beginTimenew)
        return beginTimes
    
    
    def __validateDayMonthHour(self,beginTime):
        try:     
            timestring = int(datetime.datetime(beginTime['year'],beginTime['month'],beginTime['day'],beginTime['hour'],beginTime['minute']).strftime('%s'))
            return True
        except:
            return False
            
    # if time1 and time2 are equal it returns 0
    # returns -1 if time1 is greater than time2 , returns 1 otherwise
    # Compares to the minute level
    # if one of them is none then it returns the other timestamp     
    # If one of them is contains invalid combination of day month year then 
    #it returns 1 if time2 is valid and -1 if time1 is valid
    #if both are invalid raise an exception  
    def __compareTimes(self,time1, time2):
        
        if time1 == None and time2 == None:
            return 0
        
        if time1 == None:
            return 1
        
        validTime1 = self.__validateDayMonthHour(time1)
        validTime2 = self.__validateDayMonthHour(time2)
        
        if validTime1 == False and validTime2 == False:
            raise ValueError("invalid time1 and time2 given for comparisons")

        if  validTime1 == False:
            return 1
    
        if validTime2 == False:
            return  -1
        
        if time2 == None:
            return -1
        
        if time1["year"] == time2["year"] and time1["month"] == time2["month"]  and time1["hour"] == time2["hour"] and time1["minute"] == time2["minute"]:
            return   0
        
        if time1["year"] > time2["year"]:
            return -1
        else:
            if time1['year'] == time2['year']:                
                if time1['month'] > time2['month']:
                    return -1
                else:
                    if time1['month'] == time2['month']:
                        if time1['hour'] > time2['hour']:
                            return -1
                        else:
                            if time1['hour'] == time2['hour']:
                                if time1['minute'] > time2['minute']:
                                    return -1
                                else:
                                    return 1
                            else:
                                return 1
                    else:
                        return 1
            else:
                return 1
               
    def __getBeginTime(self,tagMap,refDate):
        
        beginTime = DefaultTime.getFromDateTime(refDate)        
        tagMap = self._convertTo24(tagMap,'BTPHN','BTPAP')
        tagMap = self._convertTo4digitYear(tagMap,'BTPYN')
        
        if 'BTPMS' in tagMap.keys():
            monthstrings = tagMap['BTPMS']
            months = []
            
            for monthstring in monthstrings:
                index = 0
                try:
                    if monthstring not in timeStringAlias.keys():
                        BeginEndTime.logger.debug("Invalid month string, not in standard form:{}".format(monthstring))
                        continue 
                    stdmonthstring = timeStringAlias[monthstring]
                    mon = timeStringToNumberAlias[stdmonthstring]
                    months.append(mon)
                    #if index == 0:
                    #    months = [mon]
                    #    index += 1
                    #else:    
                    #    months.append(mon)
                except KeyError:
                    BeginEndTime.logger.debug("Invalid monthstring {}".format(monthstring))
                                
            if len(months) >0:
                minMonth = min(months)
                beginTime['month'] = minMonth
              
        if 'BTPDS' in tagMap.keys():            
            index = 0
            for daystring in tagMap['BTPDS']: 
                if daystring not in timeStringAlias.keys():
                    BeginEndTime.logger.debug("Invalid day string, not in standard form:{}".format(daystring))
                    continue               
                stddaystring = timeStringAlias[daystring]                
                newBeginTime = self.__calculateDayOffset(beginTime,stddaystring,True)
                
                if index == 0:
                    beginTime = newBeginTime
                    index += 1
                    continue
                
                if self.__compareTimes(newBeginTime,beginTime) == 1:
                    beginTime = newBeginTime
                                     
        if 'BTPHS' in tagMap.keys():                        
            index = 0
            for hourstring in tagMap['BTPHS']:
                if hourstring not in timeStringAlias.keys():
                    BeginEndTime.logger.debug("Invalid hour string, not in standard form:{}".format(hourstring))
                    continue 
                stdhourstring = timeStringAlias[hourstring]
                newBeginTime = self.__calculateHourOffset(beginTime,stdhourstring)
                
                if index == 0:
                    beginTime = newBeginTime
                    index +=1
                    continue
                
                if self.__compareTimes(newBeginTime,beginTime) == 1:
                    beginTime = newBeginTime
                        
        
        for key in tagMap.keys():
            if key in tagTimeAlias.keys():
                if key[0] == 'B':                    
                    vals = []
                    for val in tagMap[key]:
                        try:
                            intval = int(val)
                            vals.append(intval)
                        except ValueError as v:
                            BeginEndTime.logger.debug("ERROR Converting {} for key {}, error:".format(tagMap[key], key,v))
                            
                    if len(set(vals)) > 1:
                        BeginEndTime.logger.debug("More than one string for month/year/day detected key:{} value:{}".format(key,vals))

                    if len(vals)  > 0:     
                        minval = min(vals)
                        beginTime[tagTimeAlias[key]] = minval
        
        # Handling repetitions
        #if 'BTPR' in tagMap.keys():
        #    repeatString = tagMap['BTPR']
        #    beginTime = self.__calculateRepeat(beginTime,repeatString)
         
        return beginTime               
                   
    def __getEndTime(self,beginTime, tagMap):                      

        endTime = copy.deepcopy(beginTime)
                
        tagMap = self._convertTo24(tagMap, 'ETPHN', 'ETPAP')
        tagMap = self._convertTo4digitYear(tagMap,'ETPYN')
        
        if 'TIME_PERIOD' in tagMap.keys():
            for timeTuple in tagMap['TIME_PERIOD']:
                newEndTime  = self.__calculateDurationOffset(timeTuple,endTime)
                if self.__compareTimes(endTime, newEndTime) == 1:                    
                    endTime = newEndTime
                
               
        if 'ETPMS' in tagMap.keys():
            index = 0
            for monthstring in tagMap['ETPMS']: 
                try:
                    if monthstring not in timeStringAlias.keys():
                        BeginEndTime.logger.debug("Invalid month string, not in standard form:{}".format(monthstring))                        
                        continue               
                    
                    stdmonthstring = timeStringAlias[monthstring]
                    newMon = timeStringToNumberAlias[stdmonthstring]
                
                    if index == 0:
                        endTime['month'] = newMon
                                            
                    if index > 0:    
                        if newMon > endTime['month']:
                            endTime['month'] = newMon
                                        
                    if tagMap.has_key('ETPDS') == False and tagMap.has_key('TIME_PERIOD')==False:                    
                        (weekday,maxdays)=calendar.monthrange(endTime['year'],endTime['month'])
                        endTime['day'] = maxdays
                        
                    index += 1
                except KeyError:
                    BeginEndTime.logger.debug("Invalid monthstring:{}".format(monthstring))
                    
        if 'ETPDS' in tagMap.keys():            
            for daystring in tagMap['ETPDS']:                                        
                if daystring not in timeStringAlias.keys():
                    BeginEndTime.logger.debug("Invalid day string, not in standard form:{}".format(daystring))
                    continue                
                stddaystring = timeStringAlias[daystring]
                newEndTime = self.__calculateDayOffset(endTime,stddaystring,False)
                if self.__compareTimes(newEndTime, endTime) == -1:
                    endTime = newEndTime
                               
        if 'ETPHS' in tagMap.keys():
            for hourstring in tagMap['ETPHS']:                                
                if hourstring not in timeStringAlias.keys():
                    BeginEndTime.logger.debug("Invalid hour string, not in standard form:{}".format(hourstring))
                    continue                                
                hourstring = timeStringAlias[hourstring]
                stdhourstring = timeStringAlias[hourstring]
                newEndTime = self.__calculateHourOffset(endTime,stdhourstring)
                if self.__compareTimes(newEndTime, endTime) == -1:
                    endTime = newEndTime
                
                                    
        for key in tagMap.keys():
            if key in tagTimeAlias.keys():
                if key[0] == 'E':                
                    vals = []
                    for val in tagMap[key]:
                        try:                            
                            intval = int(val)
                            vals.append(intval)              
                        except ValueError as v:
                            BeginEndTime.logger.debug("ERROR Converting {} for key {}, error:".format(tagMap[key], key,v))
                    
                    if (len(set(vals))>1):
                        BeginEndTime.logger.debug("More than one value for month/day/year key:{} value:{}".format(key,vals))
                        
                    if len(vals)  > 0:     
                        maxval = max(vals)                        
                        endTime[tagTimeAlias[key]] = maxval
                            
        if endTime["hour"] == 0 and endTime["minute"] == 0 and endTime["minute"] == 0:
            endTime['hour'] = 23
            endTime['minute'] = 59
            endTime['second'] = 59
            
        if self.__compareTimes(endTime, beginTime) == 1:
            BeginEndTime.logger.debug("EndTime less than Start Time")            
            #Default One day offset            
            endTime = copy.deepcopy(beginTime)
            endTime = self.__calculateDayOffset(endTime, "day", False)
            
        if (endTime['year'] - beginTime['year']) > 1:
            BeginEndTime.logger.debug("Endtime and beginTime are off by more than 1 year")
            #endTime['year'] = beginTime['year']                                                      
                    
        return endTime
        
    def getBeginTime(self):
        return self.beginTime
    
    def getEndTime(self):
        return self.endTime
            
        
        
        
