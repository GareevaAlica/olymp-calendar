import google_auth_oauthlib.flow
from flask import session, redirect, url_for, request
import requests

import app
from app.models import User
from config import CLIENT_SECRET

SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/userinfo.email']


@app.views.app.route('/oauth_authorize')
def authorize():
    if 'credentials' in session:
        del session['credentials']
    if 'user_email' in session:
        del session['user_email']
    flow = \
        google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRET,
                                                                scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = url_for('oauth_callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    # Store the state so the callback can verify the auth server response.
    session['state'] = state
    return redirect(authorization_url)


@app.views.app.route('/oauth_callback')
def oauth_callback():
    if 'state' not in session:
        return redirect('main')
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth_callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    if 'calendar' not in authorization_response:
        return redirect('exit')
    try:
        flow.fetch_token(authorization_response=authorization_response)
    except:
        return redirect('exit')
    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = dict(
        token=credentials.token,
        refresh_token=credentials.refresh_token,
        token_uri=credentials.token_uri,
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scopes=credentials.scopes
    )
    user_email = get_user_email(credentials.token)
    session['user_email'] = user_email
    try:
        User.try_add_user(user_email, credentials)
    except:
        return redirect('exit')
    return redirect(url_for('choose_olympiads'))


def get_user_email(access_token):
    r = requests.get(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        params={'access_token': access_token})
    return r.json()['email']
