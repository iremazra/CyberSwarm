# app/nodes/__init__.py
from flask import Blueprint 
nodes_bp = Blueprint('nodes', __name__) # prefix'i sildik
from . import routes # Rotaları blueprint'e bağlamak için ŞART