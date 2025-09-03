# FormApp
🔐 Step 1: Set Up Google Sheets API
Go to the Google Cloud Console.
Navigate to APIs & Services > Credentials.
Click Create Credentials > Service Account.
Fill in the details and create the service account.
After creation, click on the service account and go to the Keys tab.
Click Add Key > Create new key > JSON.

This will download a JSON file with the required fields (client_email, private_key, token_uri, etc.).

1.1 Get credentials.json
    Go to: Google Cloud Console
    Create a project
    Enable Google Sheets API
    Create Service Account, download JSON key → save as credentials.json
    Share your Google Sheet with the service account email (from JSON)

1.2 Create a Google Sheet
    Create a new Google Sheet
    First row: headers matching your fields
    Note the Sheet ID from the URL:
    https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit

1. Create a Service Account





2. Replace Your credentials.json
Replace your current credentials.json with the one you just downloaded.
3. Share Your Google Sheet with the Service Account

Open your Google Sheet.
Click Share and general access (allow anyone with editor access).