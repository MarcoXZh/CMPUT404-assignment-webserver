import SocketServer
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright Â© 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

import os

class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        path = self.data.split(" ")[1]
        fullpath = os.path.normpath(os.getcwd() + "/www" + path)
        try:
            if not fullpath.startswith(os.getcwd() + "/www"):
                raise IOError
            elif not os.path.exists(fullpath):
                self.respond(404, None);
            elif os.path.isdir(fullpath) and path[-1] != "/":
                self.respond(301, path);
            else:
                if os.path.isdir(fullpath):
                    fullpath += "/index.html"
                self.respond(200, fullpath);
        except IOError:
            self.respond(404, None);
    pass # def handle(self)

    def respond(self, code, url):
        msg = ""
        if code == 404:
            msg = "HTTP/1.1 404 Not Found\n"
            msg += "Content-Type: text/html; charset=UTF-8\n\n"
            msg += "PAGE NOT FOUND\n"
        elif code == 301:
            msg = "HTTP/1.1 301 Moved Permanently\n"
            msg += "Location: " + url + "/\n\n"
            msg += "PAGE HAS BEEN MOVED PERMANENTLY\n"
        elif code == 200:
            msg = "HTTP/1.1 200 OK\n"
            if url.endswith(".html"):
                msg += "Content-Type: text/html; charset=UTF-8\n\n"
            elif url.endswith(".css"):
                msg += "Content-Type: text/css; charset=UTF-8\n\n"
            else:
                msg += "Content-Type: text/plain; charset=UTF-8\n\n"                
            file = open(url, "r")
            msg += file.read()
            file.close()
        self.request.sendall(msg)
    pass # def respond(self, code, url)

pass # class MyWebServer(SocketServer.BaseRequestHandler)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
pass # if __name__ == "__main__"

