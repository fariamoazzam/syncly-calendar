from flask import Flask, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

# Initialize the Flask app
app = Flask(__name__)

# Set secret key securely for production
app.secret_key = os.urandom(24)  # Replace this in production with a securely stored key.

# Allow insecure transport for testing locally (remove in production)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/calendar']

@app.route('/')
def index():
    return 'Welcome to Smart Calendar Integration! <a href="/authorize">Authorize</a>'

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session.get('state')
    if not state:
        return "Invalid State. Please start the authorization flow again.", 400

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    # Save credentials in the session
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return redirect(url_for('events'))

@app.route('/events')
def events():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))

    # Reconstruct the Credentials object from session dictionary
    credentials_dict = session['credentials']
    credentials = Credentials(
        credentials_dict['token'],
        refresh_token=credentials_dict.get('refresh_token'),
        token_uri=credentials_dict['token_uri'],
        client_id=credentials_dict['client_id'],
        client_secret=credentials_dict['client_secret'],
        scopes=credentials_dict['scopes']
    )

    # Build the Google Calendar service
    service = build('calendar', 'v3', credentials=credentials)

    try:
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])
    except Exception as e:
        return f"Error fetching events: {str(e)}"

    # Render events as simple HTML
    output = '<h1>Your Upcoming Events:</h1>'
    if not events:
        output += '<p>No upcoming events found.</p>'
    else:
        for event in events:
            summary = event.get('summary', 'No Title')
            start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', 'No Date'))
            output += f"<p>{summary} at {start}</p>"

    return output

if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)
