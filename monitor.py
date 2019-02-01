import urllib.request
import csv
import os.path
import datetime
import time
import contextlib
from collections import OrderedDict
import json
import pymongo
from middleware import get_settings

SETTINGS = get_settings()
if SETTINGS['test_mode'] == 'on':
    BASE_URL = SETTINGS['base_url_test']
    FILE_SAVING_FOLDER = SETTINGS['monitor']['file_saving_folder_test']
else:
    BASE_URL = SETTINGS['base_url_prod']
    FILE_SAVING_FOLDER = SETTINGS['monitor']['file_saving_folder_prod']
DATA_URL = '{}{}'.format(BASE_URL, SETTINGS['data_path'])
CONNECT_TIMEOUT = SETTINGS['monitor']['connect_timeout']
REQUEST_INTERVAL_IN_SECONDS = SETTINGS['monitor']['request_interval_in_seconds']
AVERAGELEN = SETTINGS['monitor']['averagelen'] # average length
THRESHOLD = SETTINGS['monitor']['threshold'] # how many times more or less param values are still valid
DIGITS_TO_ROUND = SETTINGS['monitor']['digits_to_round'] # number of digits after comma
CONTINUOUS_ERROR_COUNT = SETTINGS['monitor']['continuous_error_count']
#global variables
dataAccumulatorFilled = False
dataAccumulatorInitialized = False
data_accumulator = {}

def fill_database(json_data):
    try:
        # mongoServer = connect('monitor_data', username='myUserAdmin', password='abc123', host='localhost')
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["serega_monitor"]
        mycol = mydb["monitor_data"]
        # mydict = {"name": "John", "address": "Highway 37"}
        # mycol.insert_one(mydict)
        # mydict = {"name": "Peter", "address": "Lowstreet 27"}
        x = mycol.insert_one(json_data)
        print(x.inserted_id)
        # print(mydb.list_collection_names())
    except Exception as e:
        print(e)


def fill_data_accumulator(param_name, param_val, increment_error_counter=False, reset_errors=False, init=False):
    global data_accumulator
    if (param_val > 150):
        param_val = 1
    if (param_val < -100):
        param_val = -1
    if init:
        print('initializing: Name: {}; value: {}'.format(param_name, param_val))
        data_accumulator[param_name]['accumulator'].append(param_val)
        data_accumulator[param_name]['errorCount'] = 0
    if not increment_error_counter or data_accumulator[param_name]['errorCount'] > CONTINUOUS_ERROR_COUNT:
        data_accumulator[param_name]['accumulator'].append(param_val)
        if len(data_accumulator[param_name]['accumulator']) > AVERAGELEN:
            data_accumulator[param_name]['accumulator'].pop(0)
    if increment_error_counter:
        data_accumulator[param_name]['errorCount'] += 1
    if reset_errors:
        data_accumulator[param_name]['errorCount'] = 0


def prepare_chart_data(response):
    global data_accumulator
    global dataAccumulatorFilled
    global dataAccumulatorInitialized
    formatted_result = OrderedDict()
    print('response: ', response)
    for element in response:
        param_name = element.split('=')[0]
        param_val = round(float(element.split('=')[1]), DIGITS_TO_ROUND)
        data_accumulator.setdefault(param_name, {'accumulator': [], 'errorCount': 0})
        if len(data_accumulator[param_name]['accumulator']) < AVERAGELEN:
            fill_data_accumulator(param_name, param_val, init=True)
            formatted_result = False
        else:
            dataAccumulatorInitialized = True
            if sum(data_accumulator[param_name]['accumulator']) == 0 or param_name == 'STns' or param_name == 'STnag' or param_name == 'dT':
                formatted_result[param_name] = round(param_val, DIGITS_TO_ROUND)
                if param_val != 0 and param_name != 'STns' and param_name != 'STnag':
                    fill_data_accumulator(param_name, param_val)
            else:
                average = (sum(data_accumulator[param_name]['accumulator'])) / AVERAGELEN
                otklonenie = param_val / average
                if ((otklonenie > (1 / THRESHOLD)) and ( otklonenie < THRESHOLD)):
                    fill_data_accumulator(param_name, param_val,  reset_errors=True)
                    formatted_result[param_name] = round(average, DIGITS_TO_ROUND)
                else:
                    fill_data_accumulator(param_name, param_val, increment_error_counter=True)
                    formatted_result[param_name] = round((sum(data_accumulator[param_name]['accumulator'])) /
                                                         AVERAGELEN, DIGITS_TO_ROUND)
                    print('{} inCorrect: {}; Srednie: {}\nCorrected: {}; Errors: {}'.
                          format(param_name, param_val, data_accumulator[param_name]['accumulator'],
                                 sum(data_accumulator[param_name]['accumulator']) / AVERAGELEN,
                          data_accumulator[param_name]['errorCount']))
    if formatted_result:
        formatted_result['time'] = datetime.datetime.now().strftime("%H:%M")
    print('Corrected Result:\n', formatted_result)
    # print('Data Accumulator: ')
    # for key in data_accumulator.keys():
    #     print(key, data_accumulator[key])
    return formatted_result

def write_to_file(data_from_api):
    newFile = os.path.isfile(filename)
    with open(filename, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', dialect='excel', fieldnames=data_from_api.keys())
        if not newFile:
            writer.writeheader()
        writer.writerow(data_from_api)


while True:
    filename = '{}{}.csv'.format(FILE_SAVING_FOLDER, datetime.datetime.now().strftime("%Y_%m_%d"))
    try:
        print('Connecting: ', datetime.datetime.now().strftime("%Y:%m:%d:%H:%M:%S"))
        with contextlib.closing(urllib.request.urlopen(DATA_URL, timeout=CONNECT_TIMEOUT)) as f:
            resp = f.read().decode().split('<')[0].replace(' ', '').split(';')
        res = prepare_chart_data(resp)
        if res:
            print("WRITING: ", filename)
            write_to_file(res)
            print(json.dumps(res))
            res['created'] = datetime.datetime.now()
            fill_database(res)
        if not dataAccumulatorInitialized:
            print('IN IF: dataAccumulatorFilled: ', dataAccumulatorInitialized)
            time.sleep(1)
    except Exception as e:
        res = False
        print('Error occured during requesting data: ', e)
        #raise e
    print('Sleeping: ', REQUEST_INTERVAL_IN_SECONDS, datetime.datetime.now().strftime("%H:%M:%S"))
    time.sleep(REQUEST_INTERVAL_IN_SECONDS)
