import logging

log = logging.getLogger('root')

import http.server
import socketserver
from os import curdir, sep
import cgi
import json
import io

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

class myHandler(http.server.BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.pinSet = False
    
    #Handler for the GET requests
    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"
        if self.path=="/pinrequired":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if not self.pinSet:
                self.wfile.write(b'{"required": true}')
            else:
                self.wfile.write(b'{"required": false}')
            return

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path, 'rb') 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
        if self.path=="/pin":
            self.handlePin()


    def handlePin(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

           

        data = json.loads(self.data_string)
        print(data['pin'])
        if (data['pin'] == 1111):
            self.send_response(200)
        else:
            self.send_response(503)
        self.end_headers()
        return


with socketserver.TCPServer(("", PORT), myHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

# if __name__ == "__main__":
    # log.debug('Starting SMS Gateway backend application')

