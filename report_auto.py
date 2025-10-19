from roc import Rocs #Operations
sheet_id = '1XwE8pkS6gejwUZCx71-1D3HAEFda06otbiu6spkwwBo'

#Google Sheet API setup
import os 
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACOUNT_FILE = 'financial-report.json'
credentials = Credentials.from_service_account_file(SERVICE_ACOUNT_FILE, scopes = SCOPES)

service = build('sheets', 'v4', credentials= credentials)

sheet = service.spreadsheets()

#Get the initial_balance, file_names
sheet_reads = sheet.values().get(spreadsheetId = sheet_id, range = 'Variables!B2:B5').execute()

input_values = sheet_reads.get('values', [])

chequeing_balance = round(float(input_values[0][0]),2)
saving_balance = round(float(input_values[1][0]),2)
chequeing_file = input_values[2][0]
saving_file = input_values[3][0]

#Initialize
monthly_report = Rocs()

#Run the ooperations
chequeing_recon = monthly_report.cheq_recon_transform(chequeing_balance, chequeing_file)
saving_recon = monthly_report.sav_recon_transform(saving_balance, saving_file)
income_sheet = monthly_report.income_transform(chequeing_file, saving_file)
expenditure_sheet = monthly_report.expenditure_transform(chequeing_file, saving_file)

#Update the csv files onto the connected sheet 'MonthlyReportAuto
cheque_recon_output = sheet.values().append(
  spreadsheetId = sheet_id,
  valueInputOption = 'RAW',
  range = 'Reconcilation!A2', #Starting cell
  body = dict(
    majorDimension = 'Rows',
    values = chequeing_recon.T.reset_index().T.values.tolist()) #Input dataframe
).execute()

saving_recon_output = sheet.values().append(
  spreadsheetId = sheet_id,
  valueInputOption = 'RAW',
  range = 'Reconcilation!H2', #Starting cell
  body = dict(
    majorDimension = 'Rows',
    values = saving_recon.T.reset_index().T.values.tolist()) #Input dataframe
).execute()

#Income-Expenditure sheet
income_output = sheet.values().append(
  spreadsheetId = sheet_id,
  valueInputOption = 'RAW',
  range = 'Income-Expenditure!A2', #Starting cell
  body = dict(
    majorDimension = 'Rows',
    values = income_sheet.T.reset_index().T.values.tolist()) #Input dataframe
).execute()

saving_recon_output = sheet.values().append(
  spreadsheetId = sheet_id,
  valueInputOption = 'RAW',
  range = 'Income-Expenditure!J2', #Starting cell
  body = dict(
    majorDimension = 'Rows',
    values = expenditure_sheet.T.reset_index().T.values.tolist()) #Input dataframe
).execute()
