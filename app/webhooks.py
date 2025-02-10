### app/webhooks.py
from flask import Blueprint, request

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    # Process webhook data
    return "Webhook received", 200