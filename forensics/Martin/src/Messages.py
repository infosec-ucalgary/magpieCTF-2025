from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def serve_text():
    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Server': 'Werkzeug/1.0.1 Python/3.6.9',
        'X-Krypto-change': 'v=b3;q=0.9, 7-layer-shift',
    }
    return Response(
        "magpieCTF{E7_RyFwA0_0x977700ypx}",
        headers=headers,
        status=200,
        mimetype='text/html'
    ), 200, {'Connection': 'close'}

if __name__ == '__main__':
    from werkzeug.serving import WSGIRequestHandler
    import ssl

    # Path to your certificate and key files
    CERT_PATH = '/home/deikas/cert.pem'
    KEY_PATH = '/home/deikas/key.pem'

    # Force HTTP/1.0
    WSGIRequestHandler.protocol_version = "HTTP/1.0"

    # Add TLS support with RSA-only cipher enforcement
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(certfile=CERT_PATH, keyfile=KEY_PATH)

    # Enforce RSA key exchange to ensure decryptability
    context.set_ciphers('RSA')

    # Run the Flask app with HTTPS
    app.run(host='10.0.21.78', port=443, ssl_context=context)

