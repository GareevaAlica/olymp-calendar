import os.path

import google.oauth2.credentials
import google_auth_oauthlib.flow
import flask

import app.models

SCOPES = ['https://www.googleapis.com/auth/calendar']


@app.views.app.route()
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        os.path.abspath('CLIENT SECRET'), scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for('http://localhost:5000')

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state
    return flask.redirect(authorization_url)


@app.views.app.route()
def redirected():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        os.path.abspath('CLIENT SECRET'), scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('REDIRECTED PAGE', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    flask.session['credentials'] = dict(
        token=credentials.token,
        refresh_token=credentials.refresh_token,
        token_uri=credentials.token_uri,
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scopes=credentials.scopes
    )

    return flask.redirect(flask.url_for('ХЗ ЧО ТУТ ДОЛЖНО БЫТЬ НО КРЕНДЕЛИ В СЕССИИ'))
