# Main script and is the one that auto starts upon powerup.

#packages:
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import subprocess

class PrintRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()

        # Print the received data using HP Smart
        subprocess.run(["hp-smart-app", "print", "--printer", "HP_Smart_Tank_581", "-"], input=data, text=True)
        
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def setup_print_server():
    try:
        # Setup HTTP server for print requests
        server_address = ('SKYNET', 8080)
        httpd = ThreadedHTTPServer(server_address, PrintRequestHandler)
        print('Starting Print Server...')
        httpd.serve_forever()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    setup_print_server()



