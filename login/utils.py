from django.contrib.auth import get_user_model # type: ignore
from django.http import JsonResponse # type: ignore
import requests # type: ignore

def create_subadmin(username, password):
    User = get_user_model()
    user = User.objects.create_user(username=username, password=password)
    user.is_staff = True
    user.is_superuser = False
    user.is_subadmin = True
    user.save()
    return user

def is_superadmin(user):
    return user.is_authenticated and user.is_superuser

def fetch_data_from_google_sheets():
    try:
        url="https://script.google.com/macros/s/AKfycbwXaP_FH_flHgAGMRjaKO7lkeWia6EbjoZ5-6OQxssQD7UAuwNAh59tbmB0F3FYD15f/exec"
        response = requests.get(url,timeout=9000)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        return JsonResponse({'error': f'HTTP error occurred: {err}', 'status_code': response.status_code})
    except ValueError:
        return JsonResponse({'error': 'Unable to decode response as JSON.', 'response_text': response.text})

# def send_data_to_google_sheets(first_name,last_name,email,country_code,phone_number,password,sheetname):
#     url="https://script.google.com/macros/s/AKfycbwXaP_FH_flHgAGMRjaKO7lkeWia6EbjoZ5-6OQxssQD7UAuwNAh59tbmB0F3FYD15f/exec"
#     details = {
#         "firstname": first_name,
#         "lastname":last_name,
#         "email": email,
#         "country_code":country_code,
#         "phoneNumber": phone_number,
#         "password":password,
#         "sheetName":sheetname
#     }
#     response = requests.post(url, json=details, timeout=9000)
#     res = response.text
#     return JsonResponse({'message': res} , safe = False)

# def send_data_to_google_sheet2(companyname,officialmale,country_code,mobilenumber,password,linkedinprofile,company_person_name,agreed_to_terms,sheetname):
#     url="https://script.google.com/macros/s/AKfycbwXaP_FH_flHgAGMRjaKO7lkeWia6EbjoZ5-6OQxssQD7UAuwNAh59tbmB0F3FYD15f/exec"
#     details = {
#                 "companyname":companyname,
#                 "officialmail":officialmale,
#                 "countrycode":country_code,
#                 "mobilenumber":mobilenumber,
#                 "password":password,
#                 "linkedInProfile":linkedinprofile,
#                 "companypersonname":company_person_name,
#                 "agreedtoterms":agreed_to_terms,
#                 "sheetName":sheetname
#     }
#     response = requests.post(url, json=details, timeout=9000)
#     res = response.text
#     return JsonResponse({'message': res} , safe = False)

# def send_data_to_google_sheet3(university,officialmale,country_code,mobilenumber,password,linkedinprofile,college_person_name,agreed_to_terms,sheetname):
#     url="https://script.google.com/macros/s/AKfycbwXaP_FH_flHgAGMRjaKO7lkeWia6EbjoZ5-6OQxssQD7UAuwNAh59tbmB0F3FYD15f/exec"
#     details = {
#                 "university":university,
#                 "officialmail":officialmale,
#                 "countrycode":country_code,
#                 "mobilenumber":mobilenumber,
#                 "password":password,
#                 "linkedinProfile":linkedinprofile,
#                 "collegepersonname":college_person_name,
#                 "agreedtoterms":agreed_to_terms,
#                 "sheetName":sheetname
#     }

#     response = requests.post(url, json=details,timeout=9000)
#     res = response.text
#     return JsonResponse({'message': res} , safe = False)

# def send_data_to_google_sheet4(consultant_name,official_email,country_code,mobile_number,password,linkedin_profile,consultant_person_name,agreed_to_terms,sheetName):
#     url="https://script.google.com/macros/s/AKfycbwXaP_FH_flHgAGMRjaKO7lkeWia6EbjoZ5-6OQxssQD7UAuwNAh59tbmB0F3FYD15f/exec"
#     details = {
#                 'name': consultant_name,
#                 'email': official_email,
#                 'countrycode':country_code,
#                 'mobileNumber': mobile_number,
#                 'password': password,
#                 'linkedinProfile': linkedin_profile,
#                 "consultantpersonname":consultant_person_name,
#                 "agreedtoterms":agreed_to_terms,
#                 'sheetName':sheetName
#             }

#     response = requests.post(url, json=details, timeout=9000)
#     res = response.text
#     return JsonResponse({'message': res} , safe = False)


from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import datetime

# Path to the service account key file
SERVICE_ACCOUNT_FILE = r"C:\Users\HP\Downloads\\collegecue-910d0-firebase-adminsdk-bvx8y-88393bd12b.json"

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Authenticate using the service account
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID of the spreadsheet to update
SPREADSHEET_ID = '1HDhRKup9caEx97v3SOayA0wQpcAwNFtr7mxC4kjtifY'

def send_data_to_google_sheets(first_name, last_name, email, country_code, phone_number, password, sheetname):
    sheet_range = f"{sheetname}!A1"
    today = datetime.now()
    formatted_date = today.strftime("%d/%m/%Y")

    if sheetname == "Sheet1":
        row_data = [
            first_name, last_name, email,
            country_code, phone_number, password, formatted_date
        ]
    else:
        return JsonResponse({'message': "Invalid sheet name"} , safe=False)

    body = {
        'values': [row_data]
    }

    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=sheet_range,
        valueInputOption='RAW', body=body).execute()

    return JsonResponse({'message': f"{result.get('updates').get('updatedCells')} cells updated in {sheetname}."} , safe=False)


def send_data_to_google_sheet2(companyname,officialmale,country_code,mobilenumber,password,linkedinprofile,company_person_name,agreed_to_terms,sheetname):
    sheet_range = f"{sheetname}!A1"
    today = datetime.now()
    formatted_date = today.strftime("%d/%m/%Y")

    if sheetname == "Sheet2":
        row_data = [
            companyname, officialmale,country_code,mobilenumber,password,linkedinprofile,company_person_name,agreed_to_terms,formatted_date
        ]
    else:
        return JsonResponse({'message': "Invalid sheet name"} , safe=False)

    body = {
        'values': [row_data]
    }
    
    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=sheet_range,
        valueInputOption='RAW', body=body).execute()
    
    return JsonResponse({'message': f"{result.get('updates').get('updatedCells')} cells updated in {sheetname}."} , safe=False)

def send_data_to_google_sheet3(university,officialmale,country_code,mobilenumber,password,linkedinprofile,college_person_name,agreed_to_terms,sheetname):
    sheet_range = f"{sheetname}!A1"
    today = datetime.now()
    formatted_date = today.strftime("%d/%m/%Y")

    if sheetname == "Sheet3":
        row_data = [
            university,officialmale,country_code,mobilenumber,password,linkedinprofile,college_person_name,agreed_to_terms,formatted_date
        ]
    else:
        return JsonResponse({'message': "Invalid sheet name"} , safe=False)
    
    body = {
        'values': [row_data]
    }
    
    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=sheet_range,
        valueInputOption='RAW', body=body).execute()
    
    return JsonResponse({'message': f"{result.get('updates').get('updatedCells')} cells updated in {sheetname}."} , safe=False)
    
def send_data_to_google_sheet4(consultant_name,official_email,country_code,mobile_number,password,linkedin_profile,consultant_person_name,agreed_to_terms,sheetName):
    sheet_range = f"{sheetName}!A1"
    today = datetime.now()
    formatted_date = today.strftime("%d/%m/%Y")
    if sheetName == "Sheet4":
        row_data = [
            consultant_name,official_email,country_code,mobile_number,password,linkedin_profile,consultant_person_name,agreed_to_terms,formatted_date
        ]
    else:
        return JsonResponse({'message': "Invalid sheet name"} , safe=False)
    
    body = {
        'values': [row_data]
    }
    
    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=sheet_range,
        valueInputOption='RAW', body=body).execute()
    
    return JsonResponse({'message': f"{result.get('updates').get('updatedCells')} cells updated in {sheetName}."} , safe=False)



#Initial code:
# from django.contrib.auth import get_user_model # type: ignore
# from django.http import JsonResponse # type: ignore
# import requests # type: ignore

# def create_subadmin(username, password):
#     User = get_user_model()
#     user = User.objects.create_user(username=username, password=password)
#     user.is_staff = True
#     user.is_superuser = False
#     user.is_subadmin = True
#     user.save()
#     return user

# def is_superadmin(user):
#     return user.is_authenticated and user.is_superuser

# def fetch_data_from_google_sheets():
#     try:
#         url="https://script.google.com/macros/s/AKfycbwXaP_FH_flHgAGMRjaKO7lkeWia6EbjoZ5-6OQxssQD7UAuwNAh59tbmB0F3FYD15f/exec"
#         response = requests.get(url,timeout=9000)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.HTTPError as err:
#         return JsonResponse({'error': f'HTTP error occurred: {err}', 'status_code': response.status_code})
#     except ValueError:
#         return JsonResponse({'error': 'Unable to decode response as JSON.', 'response_text': response.text})

# def send_data_to_google_sheets(first_name,last_name,email,country_code,phone_number,password,sheetname):
#     url="https://script.google.com/macros/s/AKfycbwXaP_FH_flHgAGMRjaKO7lkeWia6EbjoZ5-6OQxssQD7UAuwNAh59tbmB0F3FYD15f/exec"
#     details = {
#         "firstname": first_name,
#         "lastname":last_name,
#         "email": email,
#         "country_code":country_code,
#         "phoneNumber": phone_number,
#         "password":password,
#         "sheetName":sheetname
#     }
#     response = requests.post(url, json=details, timeout=9000)
#     res = response.text
#     return JsonResponse({'message': res} , safe = False)


# def send_data_to_google_sheet2(companyname, officialmale, country_code, mobilenumber, password, linkedinprofile, company_person_name, agreed_to_terms, sheetname):
#     try:
#         url = "https://script.google.com/macros/s/AKfycbwXaP_FH_flHgAGMRjaKO7lkeWia6EbjoZ5-6OQxssQD7UAuwNAh59tbmB0F3FYD15f/exec"
#         details = {
#             "companyname": companyname,
#             "officialmail": officialmale,
#             "countrycode": country_code,
#             "mobilenumber": mobilenumber,
#             "password": password,
#             "linkedInProfile": linkedinprofile,
#             "companypersonname": company_person_name,
#             "agreedtoterms": agreed_to_terms,
#             "sheetName": sheetname
#         }
#         response = requests.post(url, json=details, timeout=9000)
#         response.raise_for_status()
#         return JsonResponse({'message': response.text}, safe=False)
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({'error': str(e)})

# def send_data_to_google_sheet3(university, officialmale, country_code, mobilenumber, password, linkedinprofile, college_person_name, agreed_to_terms, sheetname):
#     try:
#         url = "https://script.google.com/macros/s/AKfycbwXaP_FH_flHgAGMRjaKO7lkeWia6EbjoZ5-6OQxssQD7UAuwNAh59tbmB0F3FYD15f/exec"
#         details = {
#             "university": university,
#             "officialmail": officialmale,
#             "countrycode": country_code,
#             "mobilenumber": mobilenumber,
#             "password": password,
#             "linkedinProfile": linkedinprofile,
#             "collegepersonname": college_person_name,
#             "agreedtoterms": agreed_to_terms,
#             "sheetName": sheetname
#         }
#         response = requests.post(url, json=details, timeout=9000)
#         response.raise_for_status()
#         return JsonResponse({'message': response.text}, safe=False)
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({'error': str(e)})

# def send_data_to_google_sheet4(consultant_name, official_email, country_code, mobile_number, password, linkedin_profile, consultant_person_name, agreed_to_terms, sheetName):
#     try:
#         url = "https://script.google.com/macros/s/AKfycbwXaP_FH_flHgAGMRjaKO7lkeWia6EbjoZ5-6OQxssQD7UAuwNAh59tbmB0F3FYD15f/exec"
#         details = {
#             'name': consultant_name,
#             'email': official_email,
#             'countrycode': country_code,
#             'mobileNumber': mobile_number,
#             'password': password,
#             'linkedinProfile': linkedin_profile,
#             "consultantpersonname": consultant_person_name,
#             "agreedtoterms": agreed_to_terms,
#             'sheetName': sheetName
#         }
#         response = requests.post(url, json=details, timeout=9000)
#         response.raise_for_status()
#         return JsonResponse({'message': response.text}, safe=False)
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({'error': str(e)})
