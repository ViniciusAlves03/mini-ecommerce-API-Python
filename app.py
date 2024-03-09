from flask import Flask
from utils.db import db
from routes.UserRoutes import userBp
from routes.StoreRoutes import storeBp
from routes.ProductRoutes import productBp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost:3306/teste_flask'  # Conexão com o banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(userBp)
app.register_blueprint(storeBp)
app.register_blueprint(productBp)

if __name__ == '__main__':
    #db.init_app(app)
    app.run(debug=True)
