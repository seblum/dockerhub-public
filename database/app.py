from crypt import methods
import os
from flask import Flask, render_template
#from flask_restful import Api, Resource

app = Flask(__name__)
#api = Api (app)

# class Data(Resource):
#     def get(self):
#         return _get_data

def _get_data() -> dict:
    data_dict = {'China': '1,412,600,000',
    'India': '1,407,563,842',
    'USA': '332,951,233',
    'Indonesia' : '272,248,500',
    'Pakistan' : '235,824,862'
    }
    return data_dict

@app.route('/')
def index():
    return render_template('index.html')

#api.add_resource(Data, "/data")

# methods not necessarily needed
@app.route('/data', methods = ["POST","GET"])
def data():
    return _get_data()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')