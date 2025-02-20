from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__, template_folder='Templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_input = request.form.get('query')
    if user_input == 'casefile':
        resp = make_response(redirect('/check'))
        resp.set_cookie('name', '0')
    else:
        resp = make_response(redirect('/check'))
        resp.set_cookie('name', '-1')
    return resp

@app.route('/check')
def check():
    name = request.cookies.get('name')
    story = {
        '0': 'You have found the casefile. Proceed with your investigation.',
        '1': 'Spider is a notorious hacker known in underground circles.',
        '2': 'Spider thrived on exposing vulnerabilities and exploiting systems.',
        '3': 'Christina’s beta encryption thwarted Spider’s ability to access plaintext credentials.',
        '4': 'Spider attempted an attack on Christina’s servers but failed.',
        '5': 'Spider was arrested, marking the end of his reign of terror.',
        '6': 'Spider learned that Christina worked with the constabulary to orchestrate his arrest.',
        '7': 'Spider vowed to uncover the truth behind his arrest.',
        '8': 'Spider discovered hidden logs on a server pointing to Christina’s involvement.',
        '9': 'Spider realized Christina used her encryption device to monitor his activities.',
        '10': 'Spider uncovered an email proving Christina orchestrated his arrest. The flag is magpieCTF{chr15t1n@_3xp0$3d_$p1d3r}.'
    }
    if name in story:
        message = story[name]
    else:
        message = 'Keep investigating to reveal Spider\'s story.'
    return render_template('check.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)