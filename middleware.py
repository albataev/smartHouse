import csv
import datetime
from os import listdir
from os.path import isfile, join

def get_data(file_name):
    # file_name is temporary workaround for tranzition to DB storage
    data_from_file = None
    if file_name != 'favicon.ico' and ('/' + file_name) in get_paths().keys():
        data_from_file = read_data_from_csv(file_name) #list of rows as list with values
    else:
        print('No such file: ', file_name)
    data = "['time', 'Tkol', {id: 'Tniz1', label: 'Tniz'}, 'Tyl', 'dT', 'STns', 'STnag', 'Tkom', 'Tkol2'],\n"
    if data_from_file is not None:
        for row in data_from_file:
            tmp_row = []
            tmp_row.append("'" + str(row[8]) + "'")
            tmp_row += row[:-1]
            data += '[' + ', '.join(tmp_row) + '],\n'
        data = '[\n' + data[:-2] + '\n]'
    return data

def read_data_from_csv(file_name):
    data_list = []
    if file_name != '':
        fname = './data/' + file_name
    else:
        fname = './data/' + (datetime.datetime.now().strftime("%Y_%m_%d")) + '.csv'
    print('Data from path ', fname, ' requested')
    with open(fname, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in filereader:
            data_list.append(row)
    return data_list[1:]

def get_available_data():
    onlyfiles = [f for f in listdir('./data/') if isfile(join('./data/', f))]
    onlyfiles.sort(reverse=True)
    file_list = ''
    for f in onlyfiles:
        file_list += '<p><a href=' + f + '>' + f.split('.')[0].replace('_', '.') + '</a></p>'
    return file_list

def get_paths():
    paths = {'/': {'status': 200}}
    onlyfiles = [f for f in listdir('./data/') if isfile(join('./data/', f))]
    for elem in onlyfiles:
        paths['/' + elem] = {'status': 200}
    return paths

def get_data_date(file_to_process):
    if file_to_process != '':
        return file_to_process.split('.')[0].replace('_', '.')
    else:
        return datetime.datetime.now().strftime("%Y.%m.%d")