from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #we don't want to keep track of modifications and we don't want to use up resources, even in production

db = SQLAlchemy(app)
import routes
with app.app_context():
    db.create_all()

# Run our application
if __name__ == '__main__':
    app.run(debug=True)