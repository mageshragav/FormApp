# FormApp

1. Create a Service Account

Go to the Google Cloud Console.
Navigate to APIs & Services > Credentials.
Click Create Credentials > Service Account.
Fill in the details and create the service account.
After creation, click on the service account and go to the Keys tab.
Click Add Key > Create new key > JSON.

This will download a JSON file with the required fields (client_email, private_key, token_uri, etc.).



2. Replace Your credentials.json
Replace your current credentials.json with the one you just downloaded.
3. Share Your Google Sheet with the Service Account

Open your Google Sheet.
Click Share and general access (allow anyone with editor access).