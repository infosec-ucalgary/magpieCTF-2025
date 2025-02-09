import http.server
import socketserver
import ssl
from threading import Thread

# Custom HTTP handler to serve the key in plaintext
class KeyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"Received GET request for {self.path}")
        if self.path == "/hidden-key":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            try:
                with open("/home/deikas/key.pem", "rb") as key_file:
                    content = key_file.read()
                    print(f"Serving key.pem content: {content[:50]}...")  # Print part of the key
                    self.wfile.write(content)
            except FileNotFoundError:
                print("Error: key.pem file not found!")
                self.wfile.write(b"Error: key.pem file not found!")
            return


# Custom HTTPS handler for the rest of the traffic
class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        # Redirect only if the Host header matches and the request is NOT for an existing file
        host = self.headers.get('Host', '')
        if host.startswith("89.167.8.45") and not self.path.endswith((".html", ".jpg", ".png", ".zip", ".css", ".js")):
            self.send_response(301)
            self.send_header('Location', f'http://5p-18-21-Cyber-Solutions.com{self.path}')
            self.end_headers()
            print(f"Redirecting to http://5p-18-21-Cyber-Solutions.com{self.path}")
            return

        # Serve files properly
        super().do_GET()
        
        
# Run an HTTP server for the hidden key
def run_http_server():
    with socketserver.TCPServer(("89.167.8.45", 8080), KeyHandler) as httpd:
        print("Serving HTTP on 89.167.8.45:8080 for hidden key")
        httpd.serve_forever()

# Run an HTTPS server for other traffic
def run_https_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.set_ciphers("RSA")  # Enforce RSA key exchange
    context.load_cert_chain(certfile="/home/deikas/cert.pem", keyfile="/home/deikas/key.pem")

    with socketserver.TCPServer(("89.167.8.45", 443), NoCacheHandler) as httpd:
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print("Serving HTTPS on 89.167.8.45:443")
        httpd.serve_forever()


# Start both servers
http_thread = Thread(target=run_http_server)
https_thread = Thread(target=run_https_server)
http_thread.start()
https_thread.start()
http_thread.join()
https_thread.join()

