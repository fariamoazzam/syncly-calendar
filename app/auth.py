### app/auth.py

from flask import Blueprint, redirect, request, session, url_for
from google_auth_oauthlib.flow import Flow
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

auth_bp = Blueprint('auth', __name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, '../client_secret.json')
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Initialize OAuth flow
flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri='http://localhost:5000/auth/callback'
)

def refresh_credentials_if_expired(credentials_data):
    """
    Check if the token has expired and refresh it using the refresh token.
    """
    creds = Credentials(
        token=credentials_data['token'],
        refresh_token=credentials_data['refresh_token'],
        token_uri=credentials_data['token_uri'],
        client_id=credentials_data['client_id'],
        client_secret=credentials_data['client_secret'],
        scopes=credentials_data['scopes']
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Update session with new credentials
        session['credentials'] = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
    return creds


@auth_bp.route('/login')
def login():
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)


@auth_bp.route('/callback')
def callback():
    if 'state' not in session or session['state'] != request.args.get('state'):
        return "Invalid state parameter", 400

    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(url_for('routes.dashboard'))


@auth_bp.route('/logout')
def logout():
    session.clear()
    return "Logged out successfully."