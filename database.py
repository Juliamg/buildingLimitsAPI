from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def initialize_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

# Example database model
class CalculationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_value = db.Column(db.Float, nullable=False)
    result = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
