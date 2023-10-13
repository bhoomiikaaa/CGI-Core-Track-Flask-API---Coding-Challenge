from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)

# MongoDB connection setup (assuming a MongoDB container named "db" is running)
client = MongoClient("mongodb://db:27017/")
db = client.customer_db
customers = db.customers

parser = reqparse.RequestParser()
parser.add_argument('customerName', type=str, required=True, help="Customer name cannot be blank!")
parser.add_argument('customerMobile', type=str, required=True, help="Mobile number must be provided!")
parser.add_argument('customerAddress', type=str, required=True, help="Address must be provided!")


class CustomerResource(Resource):
    def get(self, customer_id=None):
        if customer_id:
            customer = customers.find_one({"_id": ObjectId(customer_id)})
            if customer:
                # Convert ObjectId to string
                customer['customerId'] = str(customer['_id'])
                return {
                    "customerId": customer['customerId'],
                    "customerName": customer['customerName'],
                    "customerMobile": customer['customerMobile'],
                    "customerAddress": customer['customerAddress']
                }, 200
            return {"message": "Customer not found"}, 404
        customer_data = []
        for customer in customers.find():
            customer_data.append({
                "customerId": str(customer['_id']),
                "customerName": customer['customerName'],
                "customerMobile": customer['customerMobile'],
                "customerAddress": customer['customerAddress']
            })
        return customer_data, 200

    def post(self):
        args = parser.parse_args()
        new_customer = {
            "customerName": args['customerName'],
            "customerMobile": args['customerMobile'],
            "customerAddress": args['customerAddress']
        }
        result = customers.insert_one(new_customer)
        new_customer['customerId'] = str(result.inserted_id)
        return {
            "customerId": new_customer['customerId'],
            "customerName": new_customer['customerName'],
            "customerMobile": new_customer['customerMobile'],
            "customerAddress": new_customer['customerAddress']
        }, 201


api.add_resource(CustomerResource, '/customer', '/customer/<string:customer_id>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
