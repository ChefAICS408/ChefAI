import main
from flask import Flask, Response, request, render_template, url_for, redirect
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ingredients", methods = ['GET','POST'])
def ingredients():
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
	if(len(dict) == 0):
		return None
	return render_template("recipe.html", value=dict)

@app.route("/cookingmode", methods = ['GET','POST'])
def cookingmode():
	recipe = request.form['data']
	print(recipe)

if __name__ == '__main__':
	obj = main.ML()
	app.run(debug=True,host="localhost")