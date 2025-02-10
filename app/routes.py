### app/routes.py
from flask import Blueprint, render_template, redirect, url_for, session

# Import shared utilities instead of directly from app.calendar
from .utils import get_calendar_service, sync_events

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def home():
    return "Welcome to the Calendar AI App!"

@routes_bp.route('/dashboard')
def dashboard():
    if 'credentials' not in session:
        return redirect(url_for('auth.login'))
    
    service = get_calendar_service(session['credentials'])
    events = sync_events(service)
    return render_template('dashboard.html', events=events)