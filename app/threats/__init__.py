# app/nodes/__init__.py
from flask import Blueprint 
threats_bp = Blueprint('threats', __name__) # prefix'i sildik
from . import routes # Rotaları blueprint'e bağlamak için ŞART