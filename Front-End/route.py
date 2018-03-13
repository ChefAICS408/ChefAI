import main
from flask import Flask, Response, request, render_template, url_for, redirect
import requests
import json
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods = ['GET','POST'])
def login():
	print("final")
	token = request.form['idtoken']
	try:
	# Specify the CLIENT_ID of the app that accesses the backend:
		idinfo = id_token.verify_oauth2_token(token, requests.Request(), '339501366292-490ah4i6iib1j41b1skc878vib70nd0t.apps.googleusercontent.com')

		# Or, if multiple clients access the backend server:
		# idinfo = id_token.verify_oauth2_token(token, requests.Request())
		# if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
		#     raise ValueError('Could not verify audience.')

		if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
			raise ValueError('Wrong issuer.')

		# If auth request is from a G Suite domain:
		# if idinfo['hd'] != GSUITE_DOMAIN_NAME:
		#     raise ValueError('Wrong hosted domain.')

		# ID token is valid. Get the user's Google Account ID from the decoded token.
		userid = idinfo['sub']
	except ValueError:
		# Invalid token
			pass
	return "ee"

@app.route("/ingredients", methods = ['GET','POST'])
def ingredients():
	print("idhar")
	if(request.method == "GET"):
		name = "Guest"
	else:
		#idinfo = request.form['id_token']
		#name = idinfo['name']
		name = "temp"
	print("aaaaaaa")
	return render_template("ingredients.html", value=name)

@app.route("/newrecipe", methods = ['POST'])
def ingredients_post():
	list1 = request.form['ingredients_include']
	list2 = request.form['ingredients_exclude']
	togglestr = request.form['toggle']
	list1 = list1.split(",")
	list2 = list2.split(",")
	if(togglestr == 'on'):
		togglebool = True
	else:
		togglebool = False
	dict = obj.onClickSubmit(list1,list2,togglebool)
	if(len(dict) == 0):
		return None
	return render_template("recipe.html", value=dict)


@app.route("/allrecipes/<int:page>")
def allrecipes(page):
	if(page < 1):
		page = 1
	if(page > 2004):
		page = 2004
	list = obj.get10recipes(page, obj.sortby, obj.order)
	return render_template("allrecipes.html", value=list, page_cnt = page, sortval = obj.sortby, orderval = obj.order)

@app.route("/allrecipes/1", methods= ['POST'])
def allrecipes_post():
	obj.sortby = request.form['sort_by']
	orderbyval = request.form['order']
	if(orderbyval == "Asc"):
		obj.order = "0"
	elif( orderbyval == "Desc"):
		obj.order = "1"

	list = obj.get10recipes(1, obj.sortby, obj.order)
	return render_template("allrecipes.html", value=list, page_cnt = 1, sortval = obj.sortby, orderval = obj.order)

@app.route("/recipe/<int:page_cnt>/<int:recipe_id>")
def recipe(page_cnt, recipe_id):

	dict = obj.getRecipe(page_cnt,recipe_id, obj.sortby)
	subscription_key = "c741ec48817b42b297565fb499cccc39"
	assert subscription_key
	search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
	search_term = dict['title']
	headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
	params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML"}
	response = requests.get(search_url, headers=headers, params=params)
	response.raise_for_status()
	search_results = response.json()
	search_url = search_results['images']['value'][0]['contentUrl']
	print(search_url)
	if(len(dict) == 0):
		return None
	return render_template("recipe.html", value=dict, search = search_url)

@app.route("/cookingmode", methods = ['GET','POST'])
def cookingmode():
	recipe = request.form['data']
	print(recipe)

if __name__ == '__main__':
	obj = main.ML()
	app.run(debug=True,host="localhost")
