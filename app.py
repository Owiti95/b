# # # app.py
# # from flask import Flask
# # from flask_sqlalchemy import SQLAlchemy
# # from flask_bcrypt import Bcrypt
# # from flask_jwt_extended import JWTManager
# # from flask_migrate import Migrate
# # from routes.admin_routes import admin_bp
# # from routes.user_routes import user_bp
# # from models import db
# # from flask_cors import CORS

# # # Initialize extensions
# # bcrypt = Bcrypt()
# # jwt = JWTManager()
# # migrate = Migrate()

# # def create_app():
# #     app = Flask(__name__)
# #     app.config.from_object('config.Config')  # Config from config.py

# #     # Initialize extensions
# #     db.init_app(app)
# #     bcrypt.init_app(app)
# #     jwt.init_app(app)
# #     migrate.init_app(app, db)
# #     CORS(app, supports_credentials=True)

# #     # Register Blueprints
# #     app.register_blueprint(admin_bp, url_prefix='/admin')
# #     app.register_blueprint(user_bp, url_prefix='/user')

# #     return app

# # if __name__ == '__main__':
# #     app = create_app()
# #     app.run(debug=True)


# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager
# from flask_migrate import Migrate
# from flask_cors import CORS
# from datetime import datetime
# from routes.admin_routes import admin_bp
# from routes.user_routes import user_bp
# from models import db, Transaction
# from requests.auth import HTTPBasicAuth
# import requests
# import os
# import base64
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Initialize extensions
# bcrypt = Bcrypt()
# jwt = JWTManager()
# migrate = Migrate()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('config.Config')  # Load config from config.py

#     # Initialize extensions
#     db.init_app(app)
#     bcrypt.init_app(app)
#     jwt.init_app(app)
#     migrate.init_app(app, db)
#     CORS(app, supports_credentials=True)

#     # M-Pesa configuration
#     app.config["CONSUMER_KEY"] = os.getenv("CONSUMER_KEY")
#     app.config["CONSUMER_SECRET"] = os.getenv("CONSUMER_SECRET")
#     app.config["SHORTCODE"] = os.getenv("SHORTCODE")
#     app.config["PASSKEY"] = os.getenv("PASSKEY")
#     app.config["BASE_URL"] = os.getenv("BASE_URL")

#     # Register Blueprints
#     app.register_blueprint(admin_bp, url_prefix='/admin')
#     app.register_blueprint(user_bp, url_prefix='/user')

#     # M-Pesa Routes
#     @app.route("/buyGoods", methods=["POST"])
#     def buy_goods():
#         data = request.get_json()
#         amount = data.get("amount")
#         phone_number = data.get("phone_number")
#         transaction_id = str(datetime.timestamp(datetime.now()))  # Unique transaction ID

#         # Save transaction in database
#         new_transaction = Transaction(id=transaction_id, amount=amount, phone_number=phone_number)
#         db.session.add(new_transaction)
#         db.session.commit()

#         # Generate M-Pesa payload
#         timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#         password_str = f"{app.config['SHORTCODE']}{app.config['PASSKEY']}{timestamp}"
#         password = base64.b64encode(password_str.encode()).decode("utf-8")
#         access_token = get_access_token(app)

#         headers = {"Authorization": f"Bearer {access_token}"}
#         endpoint = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#         payload = {
#             "BusinessShortCode": app.config["SHORTCODE"],
#             "Password": password,
#             "Timestamp": timestamp,
#             "TransactionType": "CustomerPayBillOnline",
#             "Amount": amount,
#             "PartyA": phone_number,
#             "PartyB": app.config["SHORTCODE"],
#             "PhoneNumber": phone_number,
#             "CallBackURL": app.config["BASE_URL"] + "/callback",
#             "AccountReference": "Mpesa Integration Api",
#             "TransactionDesc": "Test Payment",
#         }

#         response = requests.post(endpoint, json=payload, headers=headers)
#         response_data = response.json()
#         return jsonify(response_data)

#     @app.route("/callback", methods=["POST"])
#     def mpesa_callback():
#         data = request.get_json()
#         callback = data.get("Body", {}).get("stkCallback", {})
#         result_code = callback.get("ResultCode")
#         transaction_id = callback.get("CheckoutRequestID")

#         if not transaction_id:
#             return jsonify({"ResultCode": 1, "ResultDesc": "Invalid transaction ID"})

#         # Update transaction status in database
#         transaction = Transaction.query.filter_by(id=transaction_id).first()
#         if transaction:
#             transaction.status = "Completed" if result_code == 0 else "Canceled"
#             db.session.commit()

#         return jsonify({"ResultCode": 0, "ResultDesc": "Callback received"})

#     return app

# # Helper function for getting access token
# def get_access_token(app):
#     endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
#     response = requests.get(
#         endpoint,
#         auth=HTTPBasicAuth(
#             app.config["CONSUMER_KEY"], app.config["CONSUMER_SECRET"]
#         ),
#     )
#     return response.json().get("access_token")

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp
from models import db
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load config from config.py

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

        # M-Pesa configuration
    app.config["CONSUMER_KEY"] = os.getenv("CONSUMER_KEY")
    app.config["CONSUMER_SECRET"] = os.getenv("CONSUMER_SECRET")
    app.config["SHORTCODE"] = os.getenv("SHORTCODE")
    app.config["PASSKEY"] = os.getenv("PASSKEY")
    app.config["BASE_URL"] = os.getenv("BASE_URL")

    # Register Blueprints
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
