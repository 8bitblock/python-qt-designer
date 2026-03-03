from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Restrict CORS to the local server origin to fix security vulnerability
        origin = f"http://127.0.0.1:{self.server.server_port}"
        self.send_header('Access-Control-Allow-Origin', origin)
        SimpleHTTPRequestHandler.end_headers(self)

    def log_message(self, format, *args):
        pass  # Suppress logs

def start_server(port, root_dir):
    os.chdir(root_dir)
    server = HTTPServer(('127.0.0.1', port), CORSRequestHandler)
    print(f"Starting server on port {port} serving {root_dir}")
    server.serve_forever()

def run_server_in_thread(port, root_dir):
    t = threading.Thread(target=start_server, args=(port, root_dir), daemon=True)
    t.start()
