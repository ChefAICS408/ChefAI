import main
from flask import Flask, Response, request, render_template, url_for, redirect, session
import requests
import json
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from azure.cognitiveservices.search.imagesearch.models import ImageType, ImageAspect, ImageInsightModule
from msrest.authentication import CognitiveServicesCredentials

from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods = ['GET','POST'])
def login():
	token = request.args.get('idtoken')
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
		session['name'] = idinfo['name']
	except ValueError:
		# Invalid token
		pass
	return render_template("ingredients.html", name = session['name'])

@app.route("/logout")
def logout():
	session['name'] = "Guest"
	return render_template("index.html")

@app.route("/ingredients")
def ingredients():
		return render_template("ingredients.html", name = session['name'])

@app.route("/newrecipe", methods = ['POST'])
def ingredients_post():
	list1 = request.form['ingredients_include']
	list2 = request.form['ingredients_exclude']
	try:
		togglestr = request.form['toggle']
	except KeyError:
		togglestr = "off"
	list1 = list1.split(",")
	list2 = list2.split(",")
	if(togglestr == 'on'):
		togglebool = True
	else:
		togglebool = False
	dict, included = obj.onClickSubmit(list1,list2,togglebool)
	if dict is None:
		return render_template("recipe.html", value=dict, search = first_image_result.content_url, name = session['name'], error = True, newrecipe = True)
	subscription_key = "021602f9aea34fd1987400057e71fb9e"
	client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))
	image_results = client.images.search(
        query= dict['title'],
        image_type=ImageType.photo, # Could be the str "AnimatedGif"
        aspect=ImageAspect.wide # Could be the str "Wide"
    )

	if image_results.value:
		first_image_result = image_results.value[0]
	else:
		print("Couldn't find image results!")
		#print(search_url)
	if(len(dict) == 0):
		return None
	return render_template("recipe.html", value=dict, search = first_image_result.content_url, name = session['name'], include_list = included, list_1 = list1, newrecipe = True, include_len = len(included), list_len = len(list1))


@app.route("/allrecipes/<int:page>")
def allrecipes(page):
	if(page < 1):
		page = 1
	if(page > 2004):
		page = 2004
	list = obj.get10recipes(page, obj.sortby, obj.order)
	return render_template("allrecipes.html", value=list, page_cnt = page, sortval = obj.sortby, orderval = obj.order, name = session['name'])

@app.route("/allrecipes/1", methods= ['POST'])
def allrecipes_post():
	obj.sortby = request.form['sort_by']
	orderbyval = request.form['order']
	if(orderbyval == "Asc"):
		obj.order = "0"
	elif( orderbyval == "Desc"):
		obj.order = "1"

	list = obj.get10recipes(1, obj.sortby, obj.order)
	return render_template("allrecipes.html", value=list, page_cnt = 1, sortval = obj.sortby, orderval = obj.order, name = session['name'])

@app.route("/recipe/<int:page_cnt>/<int:recipe_id>")
def recipe(page_cnt, recipe_id):

	dict = obj.getRecipe(page_cnt,recipe_id, obj.sortby)
	session['recipe_dict'] = dict
	subscription_key = "021602f9aea34fd1987400057e71fb9e"
	client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))
	image_results = client.images.search(
        query= dict['title'],
        image_type=ImageType.photo, # Could be the str "AnimatedGif"
        aspect=ImageAspect.wide # Could be the str "Wide"
    )

	if image_results.value:
		first_image_result = image_results.value[0]
	else:
		print("Couldn't find image results!")
		#print(search_url)
	if(len(dict) == 0):
		return None
	return render_template("recipe.html", value=dict, search = first_image_result.content_url, name = session['name'], newrecipe = False)

@app.route("/cookingmode")
def cookingmode():
	dict = session.get('recipe_dict', None)
	return render_template("cookingmode.html", value = dict, name = session['name'])

if __name__ == '__main__':
	obj = main.ML()
	app.config["SECRET_KEY"] = "ITSASECRET"
	app.run(debug=True,host="localhost")
