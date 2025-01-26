from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Hardcoded values
SPREADSHEET_ID = "1KJ4uF6RlmjfBftpgwFVJQU0cpeJdUBpWEqBIKGuizEk"
RANGE_NAME = "Sheet1!A1:D1"

def append_to_google_sheet(values):
    try:
        # Authenticate using the service account credentials
        credentials = Credentials.from_service_account_file("credentials.json")
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()

        # Append data to the sheet
        body = {"values": values}
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption="RAW",
            body=body
        ).execute()

        updated_cells = result.get("updates", {}).get("updatedCells", 0)
        return updated_cells
    except Exception as e:
        raise RuntimeError(f"Error interacting with Google Sheets: {str(e)}")