from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import subprocess
import time

PORT_NUMBER = 8080

class SpotifyRemote(BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(self):
        file_name = self.path.partition('?')[0]
        argument = self.path.partition('?')[2]
        if self.path == "/":
            file_name = "index.html"
        argument = argument.partition('=')[2]
        subprocess.call(["osascript", argument + ".scpt"])

        try:
            self.send_response(200)
            if file_name.endswith(".html"):
                self.send_header("Content-type", "text/html")
            elif file_name.endswith(".css"):
                self.send_header("Content-type", "text/css")
            self.end_headers()

            f = open(curdir + sep + file_name)
            self.wfile.write(f.read())
            f.close()
        except IOError:
            self.send_error(404, 'File Not Found: %s' % file_name)


def main():
    server_address = ('', PORT_NUMBER)
    try:
        print 'Starting SpotifyRemote...'
        print time.asctime(), "Server Starts - Port: %s" % PORT_NUMBER
        server = HTTPServer(server_address, SpotifyRemote)
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        print time.asctime(), "Server Stops - Port: %s" % PORT_NUMBER
        server.socket.close()


if __name__ == '__main__':
    main()

