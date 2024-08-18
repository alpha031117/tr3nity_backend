import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
import logging
from utils import convert_to_readable_timestamp
from grants_project.models import Project, Grant
from vote_project.models import Validator, vote_history
from tr3_wallet.views import get_wallet_adrr

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
ORGANISATION_WALLET_ADDRESS = '0x6d4feEBD0c955fd7fBaFBEE20C23064f06A5a639'

# Admin Wallet Address
ADMIN_WALLET_ADDRESS = '0xDDDB77cD5D9869f94E774d7BfdB813Bc2BCb3212'

# Temperory Wallet Address
TEMPERORY_WALLET_ADDRESS = '0x7d9743ce917Be4bA54B1dC62E839D1bA27959D2e'

# Normal User Wallet Address
NORMAL_USER_WALLET_ADDRESS = '0xDffbE93AE00d7172438057DfAF435B79AFE0C16a'

# Reseacher Wallet Address
RES_WALLET_ADDRESS = '0x3003E934783dD85d40c2cf76d274c689dF5975F6'

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

# Mint Grant Token
def mint_token(amount):
    API_URL = f'{BASE_API_URL}/mint'

    try:
        data = {
                    "wallet_address":f'{ORGANISATION_WALLET_ADDRESS}',
                    "to": f'{TEMPERORY_WALLET_ADDRESS}',
                    "contract_address":f'{CONTRACT_ADDRESS}',
                    "amount":f'{amount}',
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
    
# TopUp Token
@api_view(['POST'])
def topUp_token(request):
    API_URL = f'{BASE_API_URL}/mint'

    try:
        # Get data from the request body
        data_received = request.data

        if not data_received.get('wallet_address') or not data_received.get('amount'):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
        
        data = {
                    "wallet_address":f'{TEMPERORY_WALLET_ADDRESS}',
                    "to": f'{data_received["wallet_address"]}',
                    "contract_address":f'{CONTRACT_ADDRESS}',
                    "amount":f'{data_received["amount"]}',
                    "callback_url": f'{CALLBACK_URL}'
                }
        
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

# User add fund
@api_view(['POST'])
def add_fund(request):
    API_URL = f'{BASE_API_URL}/token-transfer'

    try:
        # Get data from the request body
        data = request.data

        project_id = data.get('project_id')
        amount = data.get('amount')
        user_wallet = data.get('wallet_address')

        if not project_id or not amount:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
        
        logger.info(f"Project ID: {project_id}")
        logger.info(f"Amount: {amount}")

        # Get User Wallet Balance
        balance_data = check_balance(user_wallet)

        if balance_data:
            balance_token = balance_data.get('result')
            if float(balance_token) < float(amount):
                return JsonResponse({'status': 'error', 'message': 'Insufficient balance to make the transfer'})
        
        project = Project.objects.get(pk=project_id)

        if not project:
            return JsonResponse({'status': 'error', 'message': 'Project not found'})
        
        project.total_contributors += 1
        project.current_fund += amount

        data_json = {
            "wallet_address": f'{user_wallet}',
            "to": f'{TEMPERORY_WALLET_ADDRESS}',
            "contract_address": f'{CONTRACT_ADDRESS}',
            "amount": f'{amount}',
            "callback_url": f'{CALLBACK_URL}'
        }
        
        # Make the POST request to the external API with the data
        response = requests.post(API_URL, headers=headers, json=data_json)
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

# Check Balance Utils
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
            return response_data
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

# Check Balance API
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

# Approve Token to Reseacher's Wallet
def approve_token(self_fund, matching_fund):
    API_URL = f'{BASE_API_URL}/token-transfer'

    try:
        # Sum up approve amount
        approve_amount = self_fund + matching_fund

        data = {
            "wallet_address": f'{TEMPERORY_WALLET_ADDRESS}',
            "to": f'{RES_WALLET_ADDRESS}',
            "contract_address": f'{CONTRACT_ADDRESS}',
            "amount": f'{approve_amount}',
            "callback_url": f'{CALLBACK_URL}'
        }
        
        # Make the POST request to the external API with the data
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
    
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

# Get Revenue Commission
def revenue_commission(grant_id):
    API_URL = f'{BASE_API_URL}/token-transfer'

    try:
        revenue_commission = cal_revenue_commission(grant_id)
        data = {
            "wallet_address": f'{TEMPERORY_WALLET_ADDRESS}',
            "to": f'{ADMIN_WALLET_ADDRESS}',
            "contract_address": f'{CONTRACT_ADDRESS}',
            "amount": f'{revenue_commission}',
            "callback_url": f'{CALLBACK_URL}'
        }

        # Make the POST request to the external API with the data
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
    
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

# Calculate Revenue Commission
def cal_revenue_commission(grant_id):
    grant = Grant.objects.get(pk=grant_id)
    matching_pool = grant.matching_pool

    # Calculate the revenue commission 1%
    revenue_commission = (matching_pool * 1) / 100

    return revenue_commission

# Validator Reward
def validator_reward(project_id):
    API_URL = f'{BASE_API_URL}/token-transfer'
    validator_addrs_list = []

    try:
        validator_histories = vote_history.objects.filter(project=project_id, vote_result=1)
        for history in validator_histories:
            validator_addrs_list.append(history.validator_address)


        project = Project.objects.get(pk=project_id)
        grant = Grant.objects.get(pk=project.grant)
        grant_id = grant.id
        
        # 0.05% from revenue commission
        approve_amount = (cal_revenue_commission(grant_id) * 0.05) / 100

        for validator_addr in validator_addrs_list:
            data = {
                "wallet_address": f'{ADMIN_WALLET_ADDRESS}',
                "to": f'{validator_addr}',
                "contract_address": f'{CONTRACT_ADDRESS}',
                "amount": f'{approve_amount}',
                "callback_url": f'{CALLBACK_URL}'
            }
            
            # Make the POST request to the external API with the data
            response = requests.post(API_URL, headers=headers, json=data)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
    
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


# Get Transaction Filter To
@api_view(['GET'])
def get_transaction_filter_to(request, wallet_address):
    """
    Fetch the list of transaction from the external API.
    
    Returns:
        JsonResponse: A JSON response with the status and data or error message.
    """

    API_URL = f'{BASE_API_URL}/get-token-transaction'
    params = {
        'wallet_address': f'{wallet_address}',
        'contract_address': f'{CONTRACT_ADDRESS}',
        'filter': "to"
    }

    try:
        # Make the GET request to the external API
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

        if response.status_code == 200:
            data = response.json()
            for transaction in data.get('result', []):
                from_address = transaction.get('from')
                to_address = transaction.get('to')
                timestamp = transaction.get('timestamp')
                amount = transaction.get('amount')
                if from_address:
                    from_details = get_wallet_adrr(from_address)
                    transaction['from'] = from_details.get('result', {}).get('name', 'Unknown')
                if to_address:
                    to_details = get_wallet_adrr(to_address)
                    transaction['to'] = to_details.get('result', {}).get('name', 'Unknown')
                if timestamp:
                    readable_timestamp = convert_to_readable_timestamp(timestamp)
                    # logger.debug(f"Readable Timestamp: {readable_timestamp}")
                    transaction['timestamp'] = readable_timestamp
                if amount:
                    transaction['amount'] = f'{float(amount) / 100000000:.2f} TR3'
            return JsonResponse({'status': 'success', 'data': data})
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

# Get Transaction Filter From
@api_view(['GET'])
def get_transaction_filter_from(request, wallet_address):
    """
    Fetch the list of transaction from the external API.
    
    Returns:
        JsonResponse: A JSON response with the status and data or error message.
    """

    API_URL = f'{BASE_API_URL}/get-token-transaction'
    params = {
        'wallet_address': f'{wallet_address}',
        'contract_address': f'{CONTRACT_ADDRESS}',
        'filter': "from"
    }

    try:
        # Make the GET request to the external API
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

        if response.status_code == 200:
            data = response.json()
            for transaction in data.get('result', []):
                from_address = transaction.get('from')
                to_address = transaction.get('to')
                timestamp = transaction.get('timestamp')
                amount = transaction.get('amount')
                if from_address:
                    from_details = get_wallet_adrr(from_address)
                    transaction['from'] = from_details.get('result', {}).get('name', 'Unknown')
                if to_address:
                    to_details = get_wallet_adrr(to_address)
                    transaction['to'] = to_details.get('result', {}).get('name', 'Unknown')
                if timestamp:
                    readable_timestamp = convert_to_readable_timestamp(timestamp)
                    # logger.debug(f"Readable Timestamp: {readable_timestamp}")
                    transaction['timestamp'] = readable_timestamp
                if amount:
                    transaction['amount'] = f'{float(amount) / 100000000:.2f} TR3'

            return JsonResponse({'status': 'success', 'data': data})
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

@api_view(['GET'])
def get_combined_transactions(request, wallet_address):
    """
    Fetch and combine transactions from the external API with both 'to' and 'from' filters.
    
    Args:
        wallet_address (str): The wallet address to filter transactions.
    
    Returns:
        JsonResponse: A JSON response with the status and combined data or error message.
    """

    API_URL = f'{BASE_API_URL}/get-token-transaction'
    filters = ['to', 'from']
    combined_data = []

    try:
        for filter_type in filters:
            params = {
                'wallet_address': wallet_address,
                'contract_address': CONTRACT_ADDRESS,
                'filter': filter_type
            }

            # Make the GET request to the external API
            response = requests.get(API_URL, headers=headers, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

            if response.status_code == 200:
                data = response.json()
                transactions = data.get('result', [])
                for transaction in transactions:
                    from_address = transaction.get('from')
                    to_address = transaction.get('to')
                    timestamp = transaction.get('timestamp')
                    amount = transaction.get('amount')

                    if from_address:
                        from_details = get_wallet_adrr(from_address)
                        transaction['from'] = from_details.get('result', {}).get('name', 'Unknown')
                    if to_address:
                        to_details = get_wallet_adrr(to_address)
                        transaction['to'] = to_details.get('result', {}).get('name', 'Unknown')
                    if timestamp:
                        transaction['timestamp'] = convert_to_readable_timestamp(timestamp)
                    if amount:
                        transaction['amount'] = f'{float(amount) / 100000000:.2f} TR3'

                combined_data.extend(transactions)
            else:
                return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)

        return JsonResponse({'status': 'success', 'data': combined_data})

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