from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def index():
    with open('names.txt', 'r') as f:
        names = f.readlines()
    engineer = random.choice(names).strip()
    chosen = "Amit"
    print(f"DEBUG : {chosen}")
    return render_template('index.html', engineer=engineer, names=names)

if __name__ == '__main__':
    app.run(port=10000)
