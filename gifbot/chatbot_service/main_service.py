from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hey, this fucking thing works!"

if __name__ == "__main__":
    app.run(port=80)
