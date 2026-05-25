import os
from flask import Flask
from src.api.routes import api_blueprint

def create_app():
    # Paths to frontend files relative to src/api/app.py
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    template_dir = os.path.join(base_dir, 'frontend', 'templates')
    static_dir = os.path.join(base_dir, 'frontend', 'static')

    app = Flask(__name__, 
                template_folder=template_dir, 
                static_folder=static_dir,
                static_url_path='/static')
                
    # Register blueprints
    app.register_blueprint(api_blueprint)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
