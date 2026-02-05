# app/analysis/__init__.py
from flask import Blueprint 
admin_bp = Blueprint('admin', __name__) # prefix'i sildik
from . import routes # Rotaları blueprint'e bağlamak için ŞART