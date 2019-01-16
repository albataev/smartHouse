import time
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import middleware
from html_data import html_data

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 9000
PATHS = middleware.get_paths()

class MyHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path in PATHS.keys():
            self.respond({'status': 200})
        else:
            print('NO paths: ', self.path)
            self.respond({'status': 404})

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
        if path in PATHS.keys():
            final_content = html_data.format(chart_data = middleware.get_data(file_to_process),
                                             history_data = middleware.get_available_data(),
                                             grafic_date = middleware.get_data_date(file_to_process))
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

