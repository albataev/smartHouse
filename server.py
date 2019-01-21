import time
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import middleware
from html_data import html_data
from io import StringIO
import gzip

# from test import middleware
# from test import html_data


# Tkol=1.9 ;Tniz=12.3 ;Tyl=0.1 ;dT=-10.3 ;STns=0 ;STnag=0 ;Tkom=10.1; Tbat=9.9
SETTINGS = middleware.get_settings('settings.json')
PORT_NUMBER = SETTINGS['port_number']
if SETTINGS['test_mode'] == 'on':
    PORT_NUMBER = PORT_NUMBER = SETTINGS['port_number_test']
HOST_NAME = '0.0.0.0'
PATHS = middleware.get_paths()
API_PATHS = {
    '/on1': {'status': 200},
    '/off1': {'status': 200},
    '/on2': {'status': 200},
    '/off2': {'status': 200},
}

RESOURCES_PATHS = {
    '/style.css': {'status': 200},  # remove workaround for 404
    '/favicon.ico': {'status': 200}
}

TEST_API_PATHS = {
    '/on1_test': {'status': 200}
}

class MyHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Accept-encoding', 'gzip,deflate')
        self.end_headers()

    def do_GET(self):
        if self.path not in PATHS.keys() and self.path not in API_PATHS.keys():
            print('NO paths: ', self.path)
            self.respond({'status': 404})
        if self.path in PATHS.keys():
            self.respond(PATHS[self.path])
            print('PATH ACESSED: ', self.path)
        if self.path in RESOURCES_PATHS.keys():
            self.respond(RESOURCES_PATHS[self.path])
            print('PATH ACESSED: ', self.path)
        if self.path in API_PATHS.keys():
            self.respond(API_PATHS[self.path])
        # else:
        #     print('NO paths: ', self.path)
        #     self.respond({'status': 404})

    def do_POST(self):
        # just example, no used for now
        paths = {
            '/q': {'status': 200}
        }

        if self.path in paths:
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)  # <--- Gets the data itself
            decoded = post_data.decode()
            print(json.loads(decoded)['password'])
            print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                  str(self.path), str(self.headers), post_data.decode('utf-8'))
            self.respond(paths[self.path])
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        else:
            self.respond({'status': 500})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        print('Request passed in browser: ', path)
        file_to_process = path.split('/')[1]
        print('fkjnwpjngwortngpwrtngpowrtnhwoirht', path.split('/')[1])
        if path in PATHS.keys():
            request_data = middleware.get_data(file_to_process)
            chart_data = request_data['chart_data']
            # status_nasos_nagrev = request_data['status_nasos_nagrev']
            status_nasos_nagrev = middleware.get_updated_relay_state()
            final_content = html_data.format(chart_data = chart_data,
                                             status_nasos_nagrev = status_nasos_nagrev,
                                             history_data = middleware.get_available_data(),
                                             grafic_date = middleware.get_data_date(file_to_process))
            return bytes(final_content, 'UTF-8')
        if path in API_PATHS:
            final_content = middleware.process_api_request(path)
            return bytes(final_content, 'UTF-8')
        else:
            final_content = '<h3>404 page not found</h3>'
            return bytes(final_content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))

