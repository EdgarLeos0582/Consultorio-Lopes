from flask import Flask
from database import db

app = Flask(__name__)

from routes.index import index_bp
from routes.pacientes import pacientes_bp
from routes.doctores import doctores_bp

app.register_blueprint(index_bp)
app.register_blueprint(pacientes_bp, url_prefix='/pacientes')
app.register_blueprint(doctores_bp, url_prefix='/doctores')

if __name__ == "__main__":
    app.run(debug=True)