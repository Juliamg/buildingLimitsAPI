from flask import Flask
from flask_restful import Api
from database import db, initialize_db
from resources.process import ProcessResource

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
initialize_db(app)

# Initialize API
api = Api(app)
api.add_resource(ProcessResource, '/process')

if __name__ == "__main__":
    app.run(debug=True)
