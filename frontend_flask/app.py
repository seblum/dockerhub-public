from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    IP = "0.0.0.0"
    PORT = "5001"
    r = requests.get(f"http://{IP}:{PORT}/data")
    data = r.json()
    return render_template('index.html', d=data)
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5002')