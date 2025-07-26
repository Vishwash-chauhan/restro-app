
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from models.models import db, Dish
from services.dish_service import (
    get_all_dishes, get_dish_by_id, create_dish, update_dish, delete_dish, toggle_availability
)

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
def index():
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/admin/dashboard')
def dashboard():
    dishes = get_all_dishes()
    return render_template('admin/dashboard.html', dishes=dishes)

@admin_bp.route('/admin/dish/add', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        create_dish(
            request.form,
            request.files['image'],
            current_app.config['UPLOAD_FOLDER']
        )
        flash('Dish added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_edit_dish.html', form_title='Add New Dish', form_action=url_for('admin.add_dish'))

@admin_bp.route('/admin/dish/edit/<int:id>', methods=['GET', 'POST'])
def edit_dish(id):
    dish = get_dish_by_id(id)
    if request.method == 'POST':
        update_dish(
            dish,
            request.form,
            request.files['image'],
            current_app.config['UPLOAD_FOLDER']
        )
        flash('Dish updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_edit_dish.html', form_title='Edit Dish', form_action=url_for('admin.edit_dish', id=id), dish=dish)

@admin_bp.route('/admin/dish/delete/<int:id>', methods=['POST'])
def delete_dish(id):
    dish = get_dish_by_id(id)
    delete_dish(dish)
    flash('Dish deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/dishes')
def list_dishes():
    dishes = get_all_dishes()
    return render_template('admin/list_dishes.html', dishes=dishes)

@admin_bp.route('/admin/dish/toggle_availability/<int:id>', methods=['POST'])
def toggle_availability(id):
    dish = get_dish_by_id(id)
    available = toggle_availability(dish)
    flash(f"Availability for '{dish.name}' set to {'Yes' if available else 'No'}.", 'success')
    return redirect(url_for('admin.list_dishes'))
