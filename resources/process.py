from flask_restful import Resource, reqparse
from database import db, CalculationResult

class ProcessResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('input_value', type=float, required=True, help="Input value is required.")

    def post(self):
        # Parse input
        args = self.parser.parse_args()
        input_value = args['input_value']

        # Perform calculation
        result = self.perform_calculation(input_value)

        # Store result in database
        new_record = CalculationResult(input_value=input_value, result=result)
        db.session.add(new_record)
        db.session.commit()

        return {"message": "Calculation successful", "input": input_value, "result": result}, 201

    def perform_calculation(self, input_value):
        # Example calculation
        return input_value ** 2  # Replace with your logic
