from flask import Flask
from geocode import *

app = Flask(__name__)





if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5001)