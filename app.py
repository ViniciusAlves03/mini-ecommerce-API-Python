from flask import Flask
from utils import db
from config import db_config
from routes import userBp, storeBp, productBp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_config['DB_CONNECTION']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(userBp)
app.register_blueprint(storeBp)
app.register_blueprint(productBp)

if __name__ == '__main__':
    app.run(debug=True)
