from flask import Blueprint 
auth_bp = Blueprint('auth', __name__) # prefix'i sildik
from . import routes