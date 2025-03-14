from flask import Flask
from src.routes import UserRoutes, AccountRoutes, TransactionRoutes

app = Flask(__name__)

# Register routes
user_routes = UserRoutes(app)
account_routes = AccountRoutes(app)
transaction_routes = TransactionRoutes(app)

if __name__ == '__main__':
    app.run(debug=True)
