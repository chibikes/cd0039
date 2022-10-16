import os
import sys
from turtle import title
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all(app)

# ROUTES
@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks')
def get_drinks():
    drinks = Drink.query.all()
    short_drinks = [drink.short() for drink in drinks]
    return jsonify({
        "sucess": True,
        "drinks": short_drinks
    })

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    drinks = Drink.query.all()
    long_drinks = [drink.long() for drink in drinks]
    return jsonify({
        "sucess": True,
        "drinks": long_drinks
    })

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    try:
        body = request.get_json()
        new_title=body.get('title', None)
        new_recipe=body.get('recipe', None)
        
        new_recipe = f"{new_recipe}"
        new_recipe = new_recipe.replace("'", '"')

        drink = Drink(title=new_title, recipe=new_recipe)
        
        drink.insert()
    except:
        print(sys.exc_info())
        abort(422)
    
    return jsonify({
        "sucess": True,
        "drinks": [drink.long()]
    })

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(drink_id):
    try:
        body = request.get_json()
        drink = Drink.query.get(drink_id)
        if drink is None:
            abort(404)
        new_title = body.get('title', None)
        new_recipe = body.get('recipe', None)

        new_recipe = f"{new_recipe}"
        new_recipe = new_recipe.replace("'", '"')
        
        drink.title = new_title or drink.title
        drink.recipe = new_recipe or drink.recipe
        drink.update()
    except:
        print(sys.exc_info())
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    drink = Drink.query.get(drink_id)
    if drink is None:
        abort(404)
    else:
        drink.delete()
    return jsonify({
        'success': True,
        # 'delete': drink_id
    })

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "Success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "Success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(401)
def method_not_allowed(error):
    return jsonify({
        "Success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401