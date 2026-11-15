from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Mock databases
ACCOUNTS = {
    "12345": {"name": "John Doe", "balance": 1500.00, "status": "Active"},
    "67890": {"name": "Jane Smith", "balance": 4250.50, "status": "Active"}
}

# In-memory store for support tickets
TICKETS = {}

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Bank Customer Care API",
        "version": "1.0.0",
        "endpoints": {
            "GET /balance/<account_number>": "Check account balance",
            "POST /support": "Submit a support ticket",
            "GET /support/<ticket_id>": "Check support ticket status"
        }
    })

@app.route("/balance/<account_number>", methods=["GET"])
def check_balance(account_number):
    account = ACCOUNTS.get(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({
        "account_number": account_number,
        "name": account["name"],
        "balance": account["balance"],
        "currency": "USD"
    })

@app.route("/support", methods=["POST"])
def support_ticket():
    data = request.get_json() or {}
    account_number = data.get("account_number")
    issue = data.get("issue")
    
    if not account_number or not issue:
        return jsonify({"error": "Missing account_number or issue description"}), 400
        
    # Generate a unique ticket ID and store it
    ticket_id = f"TICK-{random.randint(10000, 99999)}"
    TICKETS[ticket_id] = {
        "account_number": account_number,
        "issue": issue,
        "status": "Open - Under Review"
    }
    
    return jsonify({
        "status": "Success",
        "message": "Support ticket logged successfully.",
        "ticket_id": ticket_id
    }), 201

@app.route("/support/<ticket_id>", methods=["GET"])
def check_ticket(ticket_id):
    ticket = TICKETS.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    return jsonify({
        "ticket_id": ticket_id,
        "account_number": ticket["account_number"],
        "issue": ticket["issue"],
        "status": ticket["status"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)