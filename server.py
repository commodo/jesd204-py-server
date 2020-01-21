#!/usr/bin/python

import threading

import SocketServer
import BaseHTTPServer

from collections import deque
from SimpleHTTPServer import SimpleHTTPRequestHandler

class SimpleHTTPRequestHandlerWithPOST(SimpleHTTPRequestHandler):

    req_vars = None

    def do_POST(self):
        content_length = int(self.headers["content-length"])
        req_str = ''
        if (content_length):
            to_read = content_length
            while len(req_str) < content_length:
                _req_str = self.rfile.read(to_read)
                to_read -= len(_req_str)
                req_str += _req_str

        self.send_response(200)
        self.end_headers()

        if self.req_vars is None:
            self.req_vars = {}
        req_vars = self.req_vars
        req_vars_strs = req_str.split('&')
        for req_var_str in req_vars_strs:
            key_value = req_var_str.split('=')
            if len(key_value) != 2:
                continue
            key = urllib.unquote(key_value[0])
            value = urllib.unquote(key_value[1])
            if not (key in req_vars.keys()):
                req_vars[key] = value
            elif isinstance(req_vars[key], deque):
                req_vars[key].append(value)
            else:
                value1 = req_vars[key]
                req_vars[key] = deque()
                req_vars[key].append(value1)
                req_vars[key].append(value)


class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass

class JESD204HTTPServer(ThreadedHTTPServer):
    pass

req_handler = SimpleHTTPRequestHandlerWithPOST

server = JESD204HTTPServer(('', 2000), req_handler)

server_thread = threading.Thread(target=server.serve_forever)

#server_thread.setDaemon(True)
server_thread.start()
