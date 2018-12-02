from flask import Flask, request, send_file
from flask_restful import Resource, Api
from flask.ext.jsonpify import jsonify
from json import dumps
import numpy as np
import pandas as pd
from datetime import datetime
import pickle
from sklearn.ensemble import RandomForestRegressor # new package, to explain prediction
import time


def writelog(path='log.log', text=None):
	print(path)
	with open(path, 'a') as log:
		t = time.strftime('%x %X %H:%M:%S')
		log.write(t + str(text) + '\n')


writelog(text='-webservice started')


def openpkl(path=''):
	file = open(path, 'rb')
	model = pickle.load(file)
	file.close
	return model


def transform_numeric(df,column):
	df[column] = pd.to_numeric(df[column], errors='coerce')
	return df.dropna(axis=0, how='any')


class Index(Resource):
	def get(self):
		return ('''
			Preditor de qualidade de vinhos\n
			Para funcionar utilize um get no recurso "/prediction/": \n
			Com os valores das seguintes variáveis: \n
			['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',
      		 'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',
    		 'pH', 'sulphates', 'alcohol', 'type_Red', 'type_White'] \n
			separados por um hifem "-" \n
			Conforme exemplo: 	"/prediction/8.10-0.27-0.41-1.45-0.03-11.00-63.00-0.99-2.99-0.56-12.00-0-1"
			''')


class Prediction(Resource):
	def get(self, variables):

		try:
			variables = variables.split("-")
			features = []
			for feat in variables:
				features.append(float(feat))
		except:
			return jsonify('Impossible convert to float')

		if len(features) != 13:
			return jsonify('You need to pass the 13 features in the correct order and quantity described in the index.')


		cols_name = ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol', 'type_Red', 'type_White']
		X = pd.DataFrame(np.array(features).reshape(1,13), columns=cols_name)
		
		model_loaded = openpkl(r'.\models\model.pkl')

		msg = model_loaded.predict(X)

		writelog(text="Create new prediction: "+str(msg))

		return(jsonify(str(msg)))


def main():
	app = Flask(__name__)
	api = Api(app)

	api.add_resource(Index, '/')
	api.add_resource(Prediction, '/prediction/<variables>')

	app.run(port=1249, host='0.0.0.0')

if __name__ == '__main__':
	main()