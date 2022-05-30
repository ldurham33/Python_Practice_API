from flask import Flask
from flask import request
from flask import make_response
import json
app = Flask(__name__)


@app.route('/recipes', methods=['GET', 'POST', 'PUT'])
def recipes():
    if request.method == 'POST':
        with open('data.json', 'r+') as file:
            data = json.load(file)
            body = request.get_json()
            if any(i["name"] == body["name"] for i in data["recipes"]):
                file.close()
                return make_response({"error": "name already exists"}, 400)
            else:
                file.close()
                return make_response(add_to_recipes(body), 201)
    elif request.method == 'PUT':
        with open('data.json', 'r+') as file:
            data = json.load(file)
            body = request.get_json()
            if any(i["name"] == body["name"] for i in data["recipes"]):
                file.close()
                return make_response(update_recipe(body), 201)
            else:
                file.close()
                return make_response({"error": "Recipe does not exist"}, 404)

    else:
        file = open('data.json')
        data = json.load(file)
        recipe_names = []
        for i in data["recipes"]:
            recipe_names.append(i["name"])
        file.close()
        return {"recipe_names": recipe_names}


@app.route('/recipes/details/<recipe>')
def show_details(recipe):
    file = open('data.json')
    data = json.load(file)
    all_recipes = data["recipes"]
    for i in all_recipes:
        if i["name"] == recipe:
            ingredients = i["ingredients"]
            num_steps = len(i["instructions"])
            file.close()
            return {"ingredients": ingredients, "num_steps": num_steps}
    return {}


def add_to_recipes(addition):
    with open('data.json', 'r+') as file:
        data = json.load(file)
        body = request.get_json()
        recipe_list = data["recipes"]
        recipe_list.append(body)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.close()
        return "None"


def update_recipe(new_recipe):
    with open('data.json', 'r+') as file:
        data = json.load(file)
        body = request.get_json()
        recipe_list = data["recipes"]
        for i in range(len(recipe_list)):
            current_recipe=recipe_list[i]
            if body["name"] == current_recipe["name"]:
                recipe_list[i] = body
        file.seek(0)
        json.dump(data, file, indent=4)
        file.close()
        return "None"
