from flask import Flask
app = Flask(__name__)

# magit test 
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
