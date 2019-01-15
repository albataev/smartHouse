import urllib.request
import csv
import os.path
import datetime
import time
import contextlib
from collections import OrderedDict
from math import floor
# import mongo_test

DATA_URL = 'http://192.168.1.50/1'
# DATA_URL = 'http://localhost:8000'
CONNECT_TIMEOUT = 15
REQUEST_INTERVAL_IN_SECONDS = 40
AVERAGELEN = 4 # average length
THRESHOLD = 2 # how many times more or less param values are still valid
DIGITS_TO_ROUND = 1 # number of digits after comma
dataAccumulatorFilled = False
dataAccumulatorInitialized = False
dataAccumulator = {}

def dataProcessor(response):    
    global dataAccumulatorFilled
    global dataAccumulator
    global dataAccumulatorInitialized
    formattedResult = OrderedDict()
    print('response: ', response)
    for element in response:
        paramName = element.split('=')[0]
        paramVal = round(float(element.split('=')[1]), DIGITS_TO_ROUND)
        if not dataAccumulatorInitialized:
            dataAccumulator[paramName] = {
                'accumulator': [],
                # 'lastValue': None,
                'errorCount': 0
            }
        # START filling avg
        if len(dataAccumulator[paramName]['accumulator']) < AVERAGELEN:
            print('initializing: Name: {}; value: {}'.format(paramName, paramVal))
            if (paramVal > 100):
                paramVal = 1
            if (paramVal < -100):
                paramVal = -1
            dataAccumulator[paramName]['accumulator'].append(paramVal)
            formattedResult = False
        # END initialize avg 
        else:
            # print('dataAccumulatorFilled: ', dataAccumulatorFilled)
            dataAccumulatorFilled = True
            if sum(dataAccumulator[paramName]['accumulator']) == 0 or paramName == 'STns' or paramName == 'STnag':
                # print('In zero: ', paramName, dataAccumulator[paramName], ': ', sum(dataAccumulator[paramName]['accumulator']))
                formattedResult[paramName] = round(paramVal, DIGITS_TO_ROUND)
                if paramVal != 0 and paramName != 'STns' and paramName != 'STnag':
                    dataAccumulator[paramName]['accumulator'].append(paramVal)
            else:
                average = (sum(dataAccumulator[paramName]['accumulator'])) / AVERAGELEN
                otklonenie = paramVal / average
                inHundredRange = ((paramVal > -100) and (paramVal < 100))
                # print('(paramVal in range(-100, 100)) ', paramVal in range(-100, 100))
                if ((otklonenie > (1 / THRESHOLD)) and ( otklonenie < THRESHOLD) and inHundredRange):
                    dataAccumulator[paramName]['accumulator'].append(paramVal)
                    dataAccumulator[paramName]['accumulator'].pop(0)
                    # dataAccumulator[paramName]['lastValue'] = paramVal
                    dataAccumulator[paramName]['errorCount']=0
                    formattedResult[paramName] = round(average, DIGITS_TO_ROUND)
                    print('Correct value: ', paramName, ' = ', paramVal, '; ', dataAccumulator[paramName]['accumulator'], '; average=', round(average, 3), round(otklonenie, 3),  ((otklonenie > (1 / THRESHOLD) and ( otklonenie < THRESHOLD))))
                else:
                    dataAccumulator[paramName]['errorCount'] += 1
                    formattedResult[paramName] = round((sum(dataAccumulator[paramName]['accumulator'])) / AVERAGELEN, DIGITS_TO_ROUND)
                    print('InCorrect parameter. Name: {}; value: {}; {}; Corrected value: {}'.format(paramName, paramVal, dataAccumulator[paramName]['accumulator'], sum(dataAccumulator[paramName]['accumulator']) / AVERAGELEN))
                    # print('INCorrect parameter. No Last Value: ', paramName, ' = ', paramVal, 'Average: ', (sum(dataAccumulator[paramName]['accumulator']) / AVERAGELEN ), 'Comparation: ', (sum(dataAccumulator[paramName]['accumulator']) / AVERAGELEN < THRESHOLD))
                if dataAccumulator[paramName]['errorCount'] > 2: #if getting continuous errors - then ajust average
                    notInHundredRange = ''
                    if inHundredRange:
                        dataAccumulator[paramName]['accumulator'].append(paramVal)
                        dataAccumulator[paramName]['accumulator'].pop(0)
                    else:
                        notInHundredRange = ' AND not inHundredRange ' + paramName + ', ' + paramVal
                    print('MORE THAN 2 errors!', notInHundredRange)    
                    # dataAccumulator[paramName]['accumulator'].append(paramVal)
                    # dataAccumulator[paramName]['accumulator'].pop(0)
            # else:
                # # print('In zero: ', paramName, dataAccumulator[paramName], ': ', sum(dataAccumulator[paramName]['accumulator']))
                # formattedResult[paramName] = round(paramVal, DIGITS_TO_ROUND)
                # if paramVal != 0:
                #     dataAccumulator[paramName]['accumulator'].append(paramVal)
    dataAccumulatorInitialized = True
    if formattedResult:            
        formattedResult['time'] = datetime.datetime.now().strftime("%H:%M")
    print('Corrected Result: \n', formattedResult)
    print('Data Accumulator: ')
    for key in dataAccumulator.keys():
        print(key, dataAccumulator[key])
    return formattedResult    


while True:
    filename = './data/' + (datetime.datetime.now().strftime("%Y_%m_%d")) + '.csv'
    #filename = (datetime.datetime.now().strftime("%Y_%m_%d")) + '.csv'
    try:
        print('Connecting: ', datetime.datetime.now().strftime("%H:%M:%S"))
        with contextlib.closing(urllib.request.urlopen(DATA_URL, timeout = CONNECT_TIMEOUT)) as f:
            resp = f.read().decode().split('<')[0].replace(' ', '').split(';')
        res = dataProcessor(resp)
    except Exception as e:
        res = False
        print('Error occured during requesting data: ', e)
    if res:
        newFile = os.path.isfile(filename)
        with open(filename, 'a') as csvfile:
            # mongo_test.fill_database(fieldnames, res)
            writer = csv.DictWriter(csvfile, delimiter=';', dialect='excel', fieldnames=res.keys())
            if not newFile:
                writer.writeheader()
            writer.writerow(res)
        # print('Connecting: ', datetime.datetime.now().strftime("%H:%M:%S"))
    # print('dataAccumulatorFilled: ', dataAccumulatorFilled)
    if not dataAccumulatorFilled:
        print('IN IF: dataAccumulatorFilled: ', dataAccumulatorFilled)
        time.sleep(15)
    else:       
        time.sleep(REQUEST_INTERVAL_IN_SECONDS)
