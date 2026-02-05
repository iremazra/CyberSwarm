# app/analysis/__init__.py
from flask import Blueprint 
analysis_bp = Blueprint('analysis', __name__) # prefix'i sildik
from . import routes # Rotaları blueprint'e bağlamak için ŞART