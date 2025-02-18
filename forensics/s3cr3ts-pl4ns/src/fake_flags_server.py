from flask import Flask, Response
import random
import string

app = Flask(__name__)

def generate_random_flag():
    """Generate a random flag of the format zntcvrPGS{random_string_with_underscores}."""
    random_string = ''.join(
        random.choices(string.ascii_lowercase + string.digits + "_", k=20)
    )
    return f"zntcvrPGS{{{random_string}}}"

def rot13_encode(text):
    """Encode the given text using ROT13."""
    return text.translate(str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"
    ))

@app.route('/')
def serve_text():
    # Generate and encode the flag
    flag = generate_random_flag()
    encoded_flag = rot13_encode(flag)

    # Define custom headers
    headers = {
        'Content-Type': 'text/plain; charset=utf-8',
        'Server': 'Werkzeug/2.1.2 Python/3.10',
        'X-Krypt': 'r0t13'
    }

    # Return the response as plain text
    return Response(
        encoded_flag,
        headers=headers,
        status=200,
        mimetype='text/plain'
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
    context.load_cert_chain(certfile='/home/deikas/cert.pem', keyfile='/home/deikas/key.pem')

    # Enforce RSA key exchange ciphers only
    context.set_ciphers('RSA')
    # Run the Flask app with HTTPS
    app.run(host='10.0.12.77', port=443, ssl_context=context)

