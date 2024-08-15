import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
import logging
from utils import convert_to_readable_timestamp

# logger configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Token API_KEY and API_PASSWORD
API_KEY = 'd64bc76a62cab22df165372c5db4633a1911dd813a6f98df3d893c502cefbcf5'
API_PASSWORD = 'sk_dbe0530ab6011d5adac455fb7022b98363543299257975f61592ce27b398e357'
BASE_API_URL = 'https://service-testnet.maschain.com/api/token'

CALLBACK_URL = 'https://127.0.0.1:8000/'

# Contract Address
CONTRACT_ADDRESS = '0xd06e130A7ff3f4C335B072DF184D310BcCDdFddF'

# Organization Wallet Address
ORGANISATION_WALLET_ADDRESS = '0xDffbE93AE00d7172438057DfAF435B79AFE0C16a'

# Headers Credentials For Maschain API
headers = {
    'client_id': f'{API_KEY}',
    'client_secret': f'{API_PASSWORD}',
    'content-type': 'application/json'
}

# Test API Token Connection
def test_api_token_conn(request):
    response = requests.get(BASE_API_URL, headers=headers)
    if response.status_code == 200:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)

# Mint Token
@api_view(['POST'])
def topUp_token(request):
    API_URL = f'{BASE_API_URL}/mint'

    try:
        # Get data from the request body
        data_received = request.data

        if not data_received.get('wallet_address') or not data_received.get('amount'):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
        
        data = {
                    "wallet_address":f'{ORGANISATION_WALLET_ADDRESS}',
                    "to": f'{data_received["wallet_address"]}',
                    "contract_address":f'{CONTRACT_ADDRESS}',
                    "amount":f'{data_received["amount"]}',
                    "callback_url": f'{CALLBACK_URL}'
                }
        
        # logger.debug(f"Request Data: {data}")
        
        # Make the POST request to the external API with the data
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        
        if response.status_code == 200:
            logger.debug(f"Response Data: {response.json()}")
            return JsonResponse({'status': 'success', 'data': response.json()})
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - {response.status_code} - {response.text}")
        return JsonResponse({'status': 'error', 'message': f'HTTP error occurred: {http_err}'}, status=500)
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
        return JsonResponse({'status': 'error', 'message': f'Connection error occurred: {conn_err}'}, status=500)
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
        return JsonResponse({'status': 'error', 'message': f'Timeout error occurred: {timeout_err}'}, status=500)
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred: {req_err}")
        return JsonResponse({'status': 'error', 'message': f'An error occurred: {req_err}'}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return JsonResponse({'status': 'error', 'message': f'Unexpected error occurred: {e}'}, status=500)

# Transfer Token
# @api_view(['POST'])
# def transfer_token(request, capacity_used):
#     API_URL = f'{BASE_API_URL}/token-transfer'

#     try:
#         # Get the charge token value
#         charge_token = calculate_charge(float(capacity_used))

#         # Get data from the request body
#         data = request.data

#         # Check if the user's balance  is greater than the charge token
#         balance_response, balance_data = check_balance(data['wallet_address'])

#         if balance_data:
#             balance_token = balance_data.get('result')

#         else:
#             balance_token = 0 

#         logger.info(f"{float(balance_token)}")
#         logger.info(f"{float(charge_token)}")

#         if float(balance_token) < float(charge_token):
#             # logger.error(f"Insufficient balance to make the transfer")
#             return JsonResponse({'status': 'error', 'message': 'Insufficient balance to make the transfer'})
        
#         else:
#             # Update the amount field with the charge token value
#             data['amount'] = charge_token 
#             # data['callback_url'] = 'http://localhost:8000/maschain_token/callback-handler/' 
#             logger.debug(f"Request Data: {data}")
            
#             # Make the POST request to the external API with the data
#             response = requests.post(API_URL, headers=headers, json=data)
#             response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
            
#             if response.status_code == 200:
#                 logger.debug(f"Response Data: {response.json()}")
#                 return JsonResponse({'status': 'success', 'data': response.json()})
#             else:
#                 return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    
#     except requests.exceptions.HTTPError as http_err:
#         logger.error(f"HTTP error occurred: {http_err} - {response.status_code} - {response.text}")
#         return JsonResponse({'status': 'error', 'message': f'HTTP error occurred: {http_err}'}, status=500)
#     except requests.exceptions.ConnectionError as conn_err:
#         logger.error(f"Connection error occurred: {conn_err}")
#         return JsonResponse({'status': 'error', 'message': f'Connection error occurred: {conn_err}'}, status=500)
#     except requests.exceptions.Timeout as timeout_err:
#         logger.error(f"Timeout error occurred: {timeout_err}")
#         return JsonResponse({'status': 'error', 'message': f'Timeout error occurred: {timeout_err}'}, status=500)
#     except requests.exceptions.RequestException as req_err:
#         logger.error(f"An error occurred: {req_err}")
#         return JsonResponse({'status': 'error', 'message': f'An error occurred: {req_err}'}, status=500)
#     except Exception as e:
#         logger.error(f"Unexpected error occurred: {e}")
#         return JsonResponse({'status': 'error', 'message': f'Unexpected error occurred: {e}'}, status=500)
    
# Trasnfer Owner Wallet
@api_view(['POST'])
def transfer_owner(request):
    API_URL = f'{BASE_API_URL}/owner-transfer'

    try:
        # Get data from the request body
        data = request.data
        logger.debug(f"Request Data: {data}")
        
        # Make the POST request to the external API with the data
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        
        if response.status_code == 200:
            logger.debug(f"Response Data: {response.json()}")
            return JsonResponse({'status': 'success', 'data': response.json()})
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - {response.status_code} - {response.text}")
        return JsonResponse({'status': 'error', 'message': f'HTTP error occurred: {http_err}'}, status=500)
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
        return JsonResponse({'status': 'error', 'message': f'Connection error occurred: {conn_err}'}, status=500)
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
        return JsonResponse({'status': 'error', 'message': f'Timeout error occurred: {timeout_err}'}, status=500)
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred: {req_err}")
        return JsonResponse({'status': 'error', 'message': f'An error occurred: {req_err}'}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return JsonResponse({'status': 'error', 'message': f'Unexpected error occurred: {e}'}, status=500)

def check_balance(address):
    API_URL = f'{BASE_API_URL}/balance'

    try:
        # Get data from the request body
        data = {
                    "wallet_address":f'{address}',
                    "contract_address":f'{CONTRACT_ADDRESS}'
                }
        
        logger.debug(f"Request Data: {data}")
        
        # Make the POST request to the external API with the data
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        
        if response.status_code == 200:
            response_data = response.json()
            return JsonResponse({'status': 'success', 'data': response_data}), response_data
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)


    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - {response.status_code} - {response.text}")
        return JsonResponse({'status': 'error', 'message': f'HTTP error occurred: {http_err}'}, status=500)
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
        return JsonResponse({'status': 'error', 'message': f'Connection error occurred: {conn_err}'}, status=500)
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
        return JsonResponse({'status': 'error', 'message': f'Timeout error occurred: {timeout_err}'}, status=500)
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred: {req_err}")
        return JsonResponse({'status': 'error', 'message': f'An error occurred: {req_err}'}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return JsonResponse({'status': 'error', 'message': f'Unexpected error occurred: {e}'}, status=500)

@api_view(['POST'])
def check_balance_api(request):
    API_URL = f'{BASE_API_URL}/balance'

    try:
        data_received = request.data

        # Check request data is valid
        if not data_received.get('wallet_address'):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'})

         # Get data from the request body
        data = {
                    "wallet_address":f'{data_received["wallet_address"]}',
                    "contract_address":f'{CONTRACT_ADDRESS}'
                }

        logger.debug(f"Request Data: {data}")
        
        # Make the POST request to the external API with the data
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        
        if response.status_code == 200:
            response_data = response.json()
            logger.info(f"API Response Data: {response_data}")
            return JsonResponse({'status': 'success', 'data': response_data})
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - {response.status_code} - {response.text}")
        return JsonResponse({'status': 'error', 'message': f'HTTP error occurred: {http_err}'}, status=500)
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred: {conn_err}")
        return JsonResponse({'status': 'error', 'message': f'Connection error occurred: {conn_err}'}, status=500)
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error occurred: {timeout_err}")
        return JsonResponse({'status': 'error', 'message': f'Timeout error occurred: {timeout_err}'}, status=500)
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred: {req_err}")
        return JsonResponse({'status': 'error', 'message': f'An error occurred: {req_err}'}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return JsonResponse({'status': 'error', 'message': f'Unexpected error occurred: {e}'}, status=500)

# # Get Transaction Filter To
# @api_view(['GET'])
# def get_transaction_filter_to(request, wallet_address):
#     """
#     Fetch the list of transaction from the external API.
    
#     Returns:
#         JsonResponse: A JSON response with the status and data or error message.
#     """

#     API_URL = f'{BASE_API_URL}/get-token-transaction'
#     contract_address = '0xA10b5960afae880bA86cb3Bb5ec1Ae2eBAe19083'
#     params = {
#         'wallet_address': f'{wallet_address}',
#         'contract_address': f'{contract_address}',
#         'filter': "to"
#     }

#     try:
#         # Make the GET request to the external API
#         response = requests.get(API_URL, headers=headers, params=params)
#         response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

#         if response.status_code == 200:
#             data = response.json()
#             for transaction in data.get('result', []):
#                 from_address = transaction.get('from')
#                 to_address = transaction.get('to')
#                 timestamp = transaction.get('timestamp')
#                 amount = transaction.get('amount')
#                 if from_address:
#                     from_details = get_wallet_adrr(from_address)
#                     transaction['from'] = from_details.get('result', {}).get('name', 'Unknown')
#                 if to_address:
#                     to_details = get_wallet_adrr(to_address)
#                     transaction['to'] = to_details.get('result', {}).get('name', 'Unknown')
#                 if timestamp:
#                     readable_timestamp = convert_to_readable_timestamp(timestamp)
#                     # logger.debug(f"Readable Timestamp: {readable_timestamp}")
#                     transaction['timestamp'] = readable_timestamp
#                 if amount:
#                     transaction['amount'] = f'{float(amount) / 100:.2f} EVEC'
#             return JsonResponse({'status': 'success', 'data': data})
#         else:
#             return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    
#     except requests.exceptions.HTTPError as http_err:
#         logger.error(f"HTTP error occurred: {http_err} - {response.status_code} - {response.text}")
#         return JsonResponse({'status': 'error', 'message': f'HTTP error occurred: {http_err}'}, status=500)
#     except requests.exceptions.ConnectionError as conn_err:
#         logger.error(f"Connection error occurred: {conn_err}")
#         return JsonResponse({'status': 'error', 'message': f'Connection error occurred: {conn_err}'}, status=500)
#     except requests.exceptions.Timeout as timeout_err:
#         logger.error(f"Timeout error occurred: {timeout_err}")
#         return JsonResponse({'status': 'error', 'message': f'Timeout error occurred: {timeout_err}'}, status=500)
#     except requests.exceptions.RequestException as req_err:
#         logger.error(f"An error occurred: {req_err}")
#         return JsonResponse({'status': 'error', 'message': f'An error occurred: {req_err}'}, status=500)
#     except Exception as e:
#         logger.error(f"Unexpected error occurred: {e}")
#         return JsonResponse({'status': 'error', 'message': f'Unexpected error occurred: {e}'}, status=500)

# # Get Transaction Filter From
# @api_view(['GET'])
# def get_transaction_filter_from(request, wallet_address):
#     """
#     Fetch the list of transaction from the external API.
    
#     Returns:
#         JsonResponse: A JSON response with the status and data or error message.
#     """

#     API_URL = f'{BASE_API_URL}/get-token-transaction'
#     contract_address = '0xA10b5960afae880bA86cb3Bb5ec1Ae2eBAe19083'
#     params = {
#         'wallet_address': f'{wallet_address}',
#         'contract_address': f'{contract_address}',
#         'filter': "from"
#     }

#     try:
#         # Make the GET request to the external API
#         response = requests.get(API_URL, headers=headers, params=params)
#         response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

#         if response.status_code == 200:
#             data = response.json()
#             for transaction in data.get('result', []):
#                 from_address = transaction.get('from')
#                 to_address = transaction.get('to')
#                 timestamp = transaction.get('timestamp')
#                 amount = transaction.get('amount')
#                 if from_address:
#                     from_details = get_wallet_adrr(from_address)
#                     transaction['from'] = from_details.get('result', {}).get('name', 'Unknown')
#                 if to_address:
#                     to_details = get_wallet_adrr(to_address)
#                     transaction['to'] = to_details.get('result', {}).get('name', 'Unknown')
#                 if timestamp:
#                     readable_timestamp = convert_to_readable_timestamp(timestamp)
#                     # logger.debug(f"Readable Timestamp: {readable_timestamp}")
#                     transaction['timestamp'] = readable_timestamp
#                 if amount:
#                     transaction['amount'] = f'{float(amount) / 100:.2f} EVEC'

#             return JsonResponse({'status': 'success', 'data': data})
#         else:
#             return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    
#     except requests.exceptions.HTTPError as http_err:
#         logger.error(f"HTTP error occurred: {http_err} - {response.status_code} - {response.text}")
#         return JsonResponse({'status': 'error', 'message': f'HTTP error occurred: {http_err}'}, status=500)
#     except requests.exceptions.ConnectionError as conn_err:
#         logger.error(f"Connection error occurred: {conn_err}")
#         return JsonResponse({'status': 'error', 'message': f'Connection error occurred: {conn_err}'}, status=500)
#     except requests.exceptions.Timeout as timeout_err:
#         logger.error(f"Timeout error occurred: {timeout_err}")
#         return JsonResponse({'status': 'error', 'message': f'Timeout error occurred: {timeout_err}'}, status=500)
#     except requests.exceptions.RequestException as req_err:
#         logger.error(f"An error occurred: {req_err}")
#         return JsonResponse({'status': 'error', 'message': f'An error occurred: {req_err}'}, status=500)
#     except Exception as e:
#         logger.error(f"Unexpected error occurred: {e}")
#         return JsonResponse({'status': 'error', 'message': f'Unexpected error occurred: {e}'}, status=500)

# @api_view(['GET'])
# def get_combined_transactions(request, wallet_address):
#     """
#     Fetch and combine transactions from the external API with both 'to' and 'from' filters.
    
#     Args:
#         wallet_address (str): The wallet address to filter transactions.
    
#     Returns:
#         JsonResponse: A JSON response with the status and combined data or error message.
#     """

#     API_URL = f'{BASE_API_URL}/get-token-transaction'
#     contract_address = '0xA10b5960afae880bA86cb3Bb5ec1Ae2eBAe19083'
#     filters = ['to', 'from']
#     combined_data = []

#     try:
#         for filter_type in filters:
#             params = {
#                 'wallet_address': wallet_address,
#                 'contract_address': contract_address,
#                 'filter': filter_type
#             }

#             # Make the GET request to the external API
#             response = requests.get(API_URL, headers=headers, params=params)
#             response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

#             if response.status_code == 200:
#                 data = response.json()
#                 transactions = data.get('result', [])
#                 for transaction in transactions:
#                     from_address = transaction.get('from')
#                     to_address = transaction.get('to')
#                     timestamp = transaction.get('timestamp')
#                     amount = transaction.get('amount')

#                     if from_address:
#                         from_details = get_wallet_adrr(from_address)
#                         transaction['from'] = from_details.get('result', {}).get('name', 'Unknown')
#                     if to_address:
#                         to_details = get_wallet_adrr(to_address)
#                         transaction['to'] = to_details.get('result', {}).get('name', 'Unknown')
#                     if timestamp:
#                         transaction['timestamp'] = convert_to_readable_timestamp(timestamp)
#                     if amount:
#                         transaction['amount'] = f'{float(amount) / 100:.2f} EVEC'

#                 combined_data.extend(transactions)
#             else:
#                 return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)

#         return JsonResponse({'status': 'success', 'data': combined_data})

#     except requests.exceptions.HTTPError as http_err:
#         logger.error(f"HTTP error occurred: {http_err} - {response.status_code} - {response.text}")
#         return JsonResponse({'status': 'error', 'message': f'HTTP error occurred: {http_err}'}, status=500)
#     except requests.exceptions.ConnectionError as conn_err:
#         logger.error(f"Connection error occurred: {conn_err}")
#         return JsonResponse({'status': 'error', 'message': f'Connection error occurred: {conn_err}'}, status=500)
#     except requests.exceptions.Timeout as timeout_err:
#         logger.error(f"Timeout error occurred: {timeout_err}")
#         return JsonResponse({'status': 'error', 'message': f'Timeout error occurred: {timeout_err}'}, status=500)
#     except requests.exceptions.RequestException as req_err:
#         logger.error(f"An error occurred: {req_err}")
#         return JsonResponse({'status': 'error', 'message': f'An error occurred: {req_err}'}, status=500)
#     except Exception as e:
#         logger.error(f"Unexpected error occurred: {e}")
#         return JsonResponse({'status': 'error', 'message': f'Unexpected error occurred: {e}'}, status=500)