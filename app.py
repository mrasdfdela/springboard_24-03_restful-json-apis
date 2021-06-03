"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-is-as-secret-does'

connect_db(app)

@app.route('/api/cupcakes')
def get_cupcakes():
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    req = request.json
    new_cupcake = Cupcake(
                flavor = req.get('flavor'),
                size = req.get('size'),
                rating = req.get('rating'),
                image = req.get('image')
    )

    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake=new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    req = request.json


    cupcake.flavor = req.get('flavor', cupcake.flavor)
    cupcake.size = req.get('size', cupcake.size)
    cupcake.rating = req.get('rating', cupcake.rating)
    cupcake.image = req.get('image', cupcake.image)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(msg="deleted")

@app.route('/')
def home_page():
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return render_template('home_page.html', cupcakes=cupcakes)