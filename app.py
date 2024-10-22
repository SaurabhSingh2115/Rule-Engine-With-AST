from flask import Flask

app = Flask(__name__)

@app.route('/')


#Testing the flask app for the first time
def index():
    return "Testing flask app"


if __name__ == '__main__':
    app.run(debug=True)