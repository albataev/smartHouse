import csv
import datetime
from os import listdir
from os.path import isfile, join
import urllib.request
import contextlib
import json
import time

def get_settings(fname='settings.json'):
    try:
        with open(fname, 'r') as f:
            settings = json.loads(f.read())
            print('Settings from', fname, ':', settings)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        raise
    except ValueError as e:
        print("Value error: {}".format(e))
        raise
    except:
        print("Unexpected error")
        raise
    return settings


SETTINGS = get_settings()
CONNECT_TIMEOUT = SETTINGS['connect_timeout']
RELAY_UPDATE_TIMEOUT = SETTINGS['relay_update_timeout']
if SETTINGS['test_mode'] == 'on':
    BASE_URL = SETTINGS['base_url_test']
else:
    BASE_URL = SETTINGS['base_url_prod']
DATA_URL = '{}{}'.format(BASE_URL, SETTINGS['data_path'])

def get_data(file_name):
    # file_name is temporary workaround for tranzition to DB storage
    data_from_file = None
    res = {
        'chart_data': '',
        'data_headers': '',
        'status_nasos_nagrev': {
            'status_nasos': 0,
            'status_nagrev': 0
        }
    }
    tmp_row = None
    if file_name != 'favicon.ico' and ('/' + file_name) in get_paths().keys():
        data_from_file = read_data_from_csv(file_name) #list of rows as list with values
    else:
        print('No such file: ', file_name)
        #tbat = tkol2
    tmp_header = [data_from_file[0][-1]] + data_from_file[0][:-1]
    # proper header format: "['time', 'Tkol', 'Tniz', 'Tyl', 'dT', 'STns', 'STnag', 'Tkom', 'Tkol2', 'Tyst'],\n"
    data = "['" + ("', '").join(tmp_header) + "'],\n"
    print("data header: ", data)
    if data_from_file is not None:
        for row in data_from_file[1:]:
            time_stamp = [row[-1]]
            # row = row[:9] + time_stamp # TEMPORARY WORKAROUND, trim new params
            tmp_row = []
            tmp_row.append("'" + str(row[-1]) + "'")
            tmp_row += row[:-1]
            data += '[' + ', '.join(tmp_row) + '],\n'
        print('qqq')
        data = '[\n' + data[:-2] + '\n]'
        last_row = tmp_row
        res = {
                'chart_data': data,
                'data_headers': "['" + ("', '").join(tmp_header) + "']",
                'status_nasos_nagrev': {
                    'status_nasos': int(float(last_row[6])),
                    'status_nagrev': int(float(last_row[5]))
                    }
                }
        print('status_nasos_nagrev: ', res['status_nasos_nagrev'])
    return res

def read_data_from_csv(file_name):
    data_list = []
    if file_name != '':
        if file_name[0] == '?':
            file_name = file_name.replace('-', '_').split('=')[1] + '.csv'
        fname = '{}{}'.format('./data/', file_name)
    else:
        fname = './data/' + (datetime.datetime.now().strftime("%Y_%m_%d")) + '.csv'
    print('Data from path ', fname, ' requested')
    with open(fname, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in filereader:
            data_list.append(row)
    return data_list

# def get_available_data():
#     onlyfiles = [f.split('.')[0].replace('_', '-') for f in listdir('./data/') if isfile(join('./data/', f))]
#     onlyfiles.sort(reverse=True)
#     file_list = ''
#     for f in onlyfiles:
#         file_list += '<p><a href=?date=' + f + '>' + f.split('.')[0].replace('_', '.') + '</a></p>'
#     return file_list

def get_paths():
    paths = {'/': {'status': 200}}
    onlyfiles = [f for f in listdir('./data/') if isfile(join('./data/', f))]
    for elem in onlyfiles:
        paths['/?date=' + elem.split('.')[0].replace('_', '-')] = {'status': 200}
        paths['/' + elem] = {'status': 200}
    # print('PATHS in Middleware: \n', paths)
    return paths

def get_data_date(file_to_process):
    if file_to_process != '':
        if file_to_process[0] == '?':
            return file_to_process.split('=')[1]
        return file_to_process.split('.')[0].replace('_', '-')
    else:
        return datetime.datetime.now().strftime("%Y-%m-%d")

def process_api_request(api_path):
    error_types = {
        0: '',
        1: 'Ошибка управления реле',
        2: 'Ошибка обновления данных'
    }
    resp = {'error_code': 0,
            'error_type': '',
            'error': '',
            'status_servera_upravleniya': '',
            'status_relay': ''
            }
    print('=====Processing API request: {}{}'.format(BASE_URL, api_path))
    path = '{base_url}{api_path}'.format(base_url=BASE_URL, api_path=api_path)
    try:
        print('Connecting to API: ', path, datetime.datetime.now().strftime("%H:%M:%S"))
        with contextlib.closing(urllib.request.urlopen(path, timeout = CONNECT_TIMEOUT)) as f:
            api_resp_code = f.code
            print('api resp code ', api_resp_code)
            if api_resp_code != 200:
                print(api_resp_code)
                resp['error_code'] = 1
                resp['error'] = 'Код ответа: {}\nЗаголовки: {}\nТекст: {}'.format(api_resp_code, f.headers, f.read().decode())
                return (json.dumps(resp))
            else:
                print('else')
                resp['status_servera_upravleniya'] = {
                'code': f.code,
                'error': ''
            }
            # api_resp = f.read().decode().split('<')[0].replace(' ', '').split(';')
    except Exception as e:
        error = 'Error during querying relay: {base_url}{api_path}.\n{error}'.format(base_url=BASE_URL, api_path=api_path, error=e)
        print('error: ', error)
        resp['error_code'] = 1
        resp['error'] = error
        return (json.dumps(resp))
    print('sleeping')
    time.sleep(RELAY_UPDATE_TIMEOUT)
    updated_relay_state = get_updated_relay_state()
    print('otvet servera obnovleniya dannyh: ', updated_relay_state)
    resp['error_code'] = updated_relay_state['error_code']

    resp['error'] = updated_relay_state['error']
    resp['status_relay'] = updated_relay_state['status_relay']
    resp['error_type'] = error_types[resp['error_code']]
    print('resp sending:\n', resp)
    return json.dumps(resp)

def get_updated_relay_state():
    relay_resp = {'error_code': 0,
                  'error': '',
                  'status_relay': ''}
    try:
        print('Connecting to refresh data: ', datetime.datetime.now().strftime("%H:%M:%S"))
        with contextlib.closing(urllib.request.urlopen(DATA_URL, timeout = CONNECT_TIMEOUT)) as f:
            api_resp = f.read().decode().split('<')[0].replace(' ', '').split(';')
            relay_resp['status_relay'] = {
                "status_nasos": int(float(api_resp[4].split('=')[1])),
                "status_nagrev": int(float(api_resp[5].split('=')[1]))
            }
    except Exception as e:
        error = 'Error getting data: {base_url}. {error}'.format(base_url=DATA_URL, error=e).replace('<', '').replace('>', '')
        relay_resp = {
            'error': error,
            'error_code': 2,
            'status_relay': {
                "status_nasos": 0,
                "status_nagrev": 0
            }
        }
        print('Error occured during requesting data: ', error)
    print('updated_relay_state:\n', relay_resp)
    return relay_resp