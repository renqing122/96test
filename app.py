from flask import Flask

from views.textAnnotation import textAnnotation

app = Flask(__name__)
app.register_blueprint(textAnnotation)



@app.route("/")
def hello_world():
    return "hello"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=9100, use_reloader=False)



