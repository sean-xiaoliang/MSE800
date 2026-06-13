from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_flask():
    return "<p>Hello, Flask!</p>"

@app.route("/bye")
def bye():
    return "<p>Bye, Flask!</p>"

@app.route("/Username/Sean")
def learn():
    return f"Sean is learning Flask!"

if __name__ == "__main__":
    app.run(debug=True)