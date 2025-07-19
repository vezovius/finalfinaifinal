
from flask import Flask
from threading import Thread

<<<<<<< HEAD
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"
=======
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot çalışıyor!"
>>>>>>> 5d776aea62a13e35e0aa578dec1455e0e69966b6

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
