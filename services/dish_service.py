from models.models import db, Dish
from werkzeug.utils import secure_filename
import os

def get_all_dishes():
    return Dish.query.all()

def get_dish_by_id(dish_id):
    return Dish.query.get_or_404(dish_id)

def create_dish(data, image, upload_folder):
    filename = ''
    if image:
        filename = secure_filename(image.filename)
        image.save(os.path.join(upload_folder, filename))
    new_dish = Dish(
        name=data['name'],
        image_filename=filename,
        description=data['description'],
        price_half=float(data['price_half']) if data['price_half'] else None,
        price_full=float(data['price_full']),
        category=data['category'],
        is_available='is_available' in data,
        is_vegetarian='is_vegetarian' in data,
        spice_level=data['spice_level']
    )
    db.session.add(new_dish)
    db.session.commit()
    return new_dish

def update_dish(dish, data, image, upload_folder):
    dish.name = data['name']
    dish.description = data['description']
    dish.price_half = float(data['price_half']) if data['price_half'] else None
    dish.price_full = float(data['price_full'])
    dish.category = data['category']
    dish.is_available = 'is_available' in data
    dish.is_vegetarian = 'is_vegetarian' in data
    dish.spice_level = data['spice_level']
    if image:
        filename = secure_filename(image.filename)
        image.save(os.path.join(upload_folder, filename))
        dish.image_filename = filename
    db.session.commit()
    return dish

def delete_dish(dish):
    db.session.delete(dish)
    db.session.commit()

def toggle_availability(dish):
    dish.is_available = not dish.is_available
    db.session.commit()
    return dish.is_available
