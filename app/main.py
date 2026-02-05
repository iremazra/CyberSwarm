from flask import Flask
from .config import Config
from .extensions import db

from .auth import auth_bp
from .nodes import nodes_bp
from .threats import threats_bp
from. analysis import analysis_bp
from .admin import admin_bp

from .auth import models as auth_models
from .nodes import models as node_models
from .threats import models as threat_models
from .admin import models as admin_models

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config) #Config class'ındaki tüm ayarları Flask'a yükler. Yani app.config["SQLALCHEMY_DATABASE_URI"] gibi erişilebilir.
    db.init_app(app) #SqlAlchemy'i Flask app'e bağlar.
   
    app.register_blueprint(auth_bp,url_prefix='/api/auth') #auth_bp içindeki tüm route'ları ana uygulamaya (ana flask app'ine) ekler. #bknz: app/auth/__init__.py
    app.register_blueprint(nodes_bp,url_prefix='/api/nodes') #nodes_bp içindeki tüm route'ları ana uygulamaya (ana flask app'ine) ekledik.
    app.register_blueprint(threats_bp, url_prefix='/api/threats')
    app.register_blueprint(analysis_bp,url_prefix='/api/analysis')
    app.register_blueprint(admin_bp,url_prefix='/api/admin')

    @app.route('/health') #Sistem ayakta mı kontrolü
    def health_check():
        return {"status": "healthy"}, 200
    
    return app

app=create_app()


with app.app_context():
    db.create_all()  #Veritabanı tablolarını oluşturur. Eğer tablolar zaten varsa, hiçbir şey yapmaz.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)