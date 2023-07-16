from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def index():
    with open('names.txt', 'r') as f:
        names = f.readlines()
    name = random.choice(names).strip()
    return render_template('engineer.html', name=name)

if __name__ == '__main__':
    app.run(port=12000)
