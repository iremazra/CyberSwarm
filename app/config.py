import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'postgresql://cyberswarm:cyberswarm@db:5432/cyberswarm')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False