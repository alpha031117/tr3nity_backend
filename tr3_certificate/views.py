import json
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
import logging
from utils import convert_to_readable_timestamp, get_random_cid, get_file_from_ipfs
from datetime import datetime
from vote.models import Project, Validator, vote_history, Vote
from django.db.models import F

# This would be your database or persistent storage in a real application.
used_cids = set()  # A set of already used CIDs.
# available_cids = ['QmefZjiMi2gpunqjS7nxa8BZopFNfZwSBJFcZCQR5m8duK', 'QmXZQZBV7KF3Rfv8zhvzLH2fZ1tcB7iQsLubAEiFpE3YXz']  # List of all possible CIDs.
available_cids = ['QmefZjiMi2gpunqjS7nxa8BZopFNfZwSBJFcZCQR5m8duK'] 

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

# Certificate API_KEY and API_PASSWORD
API_KEY = 'dc02fb0bf34c7fe9862b0c118f367b2d7cea272e05c7f8a1f6cfb4cb91efdd77'
API_PASSWORD = 'sk_8c4db5095554caa82d496be6babc9a9209dcad783968a57d89335b6a0c496ae8'
BASE_API_URL = 'https://service-testnet.maschain.com/api/certificate'

WALLET_ADDRESS_OWNER_ADMIN = '0x0561BA623dB25aEfBb61882d5E0f95e3412117A6'
WALLET_ADDRESS_VALIDATOR_ADMIN = '0x5305915244C582626dF29f7c61049D39c0B8B382'

OWNER_CONTRACT_ADDRESS = '0xFa3D1712858bd8a4451ff6dD4948236123BE6664'
GORV_CONTRACT_ADDRESS = '0xBB165A89B8bB2C21cC433100180AbBEC5f614035'

# Headers Credentials For Maschain API
headers = {
    'client_id': f'{API_KEY}',
    'client_secret': f'{API_PASSWORD}',
    'content-type': 'application/json'
}
    
# Test API Certificate Connection
def test_api_cert_conn(request):
    response = requests.get(BASE_API_URL, headers=headers)
    if response.status_code == 200:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)

# Get Smart Contract Certificate List
@api_view(['GET'])
def get_cert_sm_list(request):
    """
    Fetch the list of certificate's smart contract from the external API.
    
    Returns:
        JsonResponse: A JSON response with the status and data or error message.
    """

    API_URL = f'{BASE_API_URL}/get-smart-contract'

    try:
        # Make the GET request to the external API
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        
        if response.status_code == 200:
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

# Get Smart Contract Certificate
@api_view(['GET'])
def get_cert_sm(request, address):
    """
    Fetch the list of certificate's smart contract from the external API.
    
    Returns:
        JsonResponse: A JSON response with the status and data or error message.
    """

    API_URL = f'{BASE_API_URL}/get-smart-contract/{address}'

    try:
        # Make the GET request to the external API
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        
        if response.status_code == 200:
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

# Function to prepare the data for minting NFT
def prepare_nft_owner_data(researcher_address, contract_address, selected_cid, file_content, project_name, project_description, callback_url):
    return {
        'wallet_address': WALLET_ADDRESS_OWNER_ADMIN,
        'to': researcher_address,
        'contract_address': contract_address,
        'file': (f"{selected_cid}.png", file_content),
        'attributes': json.dumps([
            {"trait": "Researcher Address", "value": researcher_address},
            {"trait": "Project Name", "value": project_name},
            {"trait": "Project Description", "value": project_description}
        ]),
        'name': "Researcher NFT Certificate",
        'description': f"Researcher {selected_cid} NFT",
        'callback_url': callback_url
    }

# Mint Certificate Owner
def mint_cert_owner(request, researcher_address, project_name, project_description):
    mint_headers = {
        'client_id': f'{API_KEY}',
        'client_secret': f'{API_PASSWORD}'
    }

    API_URL = f'{BASE_API_URL}/mint-certificate'
    CALLBACK_URL = 'https://127.0.0.1:8000/'

    try:
        # Validate input
        if not researcher_address or not project_name or not project_description:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

        # Select a random CID
        selected_cid = get_random_cid(available_cids, used_cids)
        logger.info(f'Selected CID: {selected_cid}')

        # Get file content from IPFS
        file_content, error = get_file_from_ipfs(selected_cid)
        if error:
            return JsonResponse({'status': 'error', 'message': error}, status=404)

        logger.info('File content retrieved successfully')

        # Prepare the data for minting the NFT
        data = prepare_nft_owner_data(
            researcher_address,
            OWNER_CONTRACT_ADDRESS,
            selected_cid,
            file_content,
            project_name,
            project_description,
            CALLBACK_URL
        )

        # logger.info(data['wallet_address'])

        # Send POST request to mint the NFT
        response = requests.post(
            API_URL,
            headers=mint_headers,
            data={
                'wallet_address': data['wallet_address'],
                'to': data['to'],
                'contract_address': data['contract_address'],
                'attributes': data['attributes'],
                'name': data['name'],
                'description': data['description'],
                'callback_url': data['callback_url']
            },
            files={'file': data['file']}
        )
        
        # Log response status and content
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response Text: {response.text}")

        # Check if the response is JSON
        try:
            response_data = response.json()
        except ValueError:
            logger.error("Failed to parse JSON from response. Raw response content: %s", response.text)
            return JsonResponse({'status': 'error', 'message': 'Received non-JSON response from API'}, status=500)

        # Mark the CID as used if minting is successful
        used_cids.add(selected_cid)

        return JsonResponse({'status': 'success', 'data': response_data})

    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        return JsonResponse({'status': 'error', 'message': f"Request error: {req_err}"}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return JsonResponse({'status': 'error', 'message': f"Unexpected error: {e}"}, status=500)

# Get List of Certificate Owner
@api_view(['GET'])
def get_owner_cert(request, researcher_address):
    """
    Fetch the list of certificate from the external API.
    
    Returns:
        JsonResponse: A JSON response with the status and data or error message.
    """
    tx_id = ""
    status = ""
    
    API_URL = f'{BASE_API_URL}/get-certificate?from={WALLET_ADDRESS_OWNER_ADMIN}&to={researcher_address}&contract_address={OWNER_CONTRACT_ADDRESS}&transaction_id={tx_id}&status={status}'

    try:
        # Make the GET request to the external API
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        
        if response.status_code == 200:
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

# Function to prepare the data for minting NFT
def prepare_nft_validator_data(validator_address, contract_address, selected_cid, file_content, callback_url):
    return {
        'wallet_address': WALLET_ADDRESS_VALIDATOR_ADMIN,
        'to': validator_address,
        'contract_address': contract_address,
        'file': (f"{selected_cid}.png", file_content),
        'attributes': json.dumps([
            {"trait": "Validator Address", "value": validator_address}
        ]),
        'name': "Validator NFT Certificate",
        'description': f"Validator {selected_cid} NFT",
        'callback_url': callback_url
    }

# Mint Certificate Validator
def mint_cert_validator(request, validator_address):
    mint_headers = {
        'client_id': f'{API_KEY}',
        'client_secret': f'{API_PASSWORD}'
    }

    API_URL = f'{BASE_API_URL}/mint-certificate'
    CALLBACK_URL = 'https://127.0.0.1:8000/'

    try:
        # Validate input
        if not validator_address:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

        # Select a random CID
        selected_cid = get_random_cid(available_cids, used_cids)
        logger.info(f'Selected CID: {selected_cid}')

        # Get file content from IPFS
        file_content, error = get_file_from_ipfs(selected_cid)
        if error:
            return JsonResponse({'status': 'error', 'message': error}, status=404)

        logger.info('File content retrieved successfully')

        # Prepare the data for minting the NFT
        data = prepare_nft_validator_data(
            validator_address,
            GORV_CONTRACT_ADDRESS,
            selected_cid,
            file_content,
            CALLBACK_URL
        )

        # logger.info(data['wallet_address'])

        # Send POST request to mint the NFT
        response = requests.post(
            API_URL,
            headers=mint_headers,
            data={
                'wallet_address': data['wallet_address'],
                'to': data['to'],
                'contract_address': data['contract_address'],
                'attributes': data['attributes'],
                'name': data['name'],
                'description': data['description'],
                'callback_url': data['callback_url']
            },
            files={'file': data['file']}
        )
        
        # Log response status and content
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response Text: {response.text}")

        # Check if the response is JSON
        try:
            response_data = response.json()
        except ValueError:
            logger.error("Failed to parse JSON from response. Raw response content: %s", response.text)
            return JsonResponse({'status': 'error', 'message': 'Received non-JSON response from API'}, status=500)

        # Mark the CID as used if minting is successful
        used_cids.add(selected_cid)

        # Add the validator to the offchain database
        Validator(validator_address=validator_address, reputation_score=0, created_at=datetime.now()).save()

        return JsonResponse({'status': 'success', 'data': response_data})

    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        return JsonResponse({'status': 'error', 'message': f"Request error: {req_err}"}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return JsonResponse({'status': 'error', 'message': f"Unexpected error: {e}"}, status=500)

# Get List of Certificate Validator
def get_validator_cert(request, validator_address):
    """
    Fetch the list of certificate from the external API.
    
    Returns:
        JsonResponse: A JSON response with the status and data or error message.
    """

    tx_id = ""
    status = ""
    
    API_URL = f'{BASE_API_URL}/get-certificate?from={WALLET_ADDRESS_VALIDATOR_ADMIN}&to={validator_address}&contract_address={GORV_CONTRACT_ADDRESS}&transaction_id={tx_id}&status={status}'

    try:
        # Make the GET request to the external API
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        
        if response.status_code == 200:
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

# When project research is published, store project's details & mint NFT for the researcher
def publish_research(request, researcher_address, project_name, project_description, funding_amount):
    # Store project details
    project = Project(project_name=project_name, project_description=project_description, funded_amount=funding_amount, pub_date=datetime.now(), user_address=researcher_address)
    project.save()

    # Store the votePoll for the project
    votePoll = Vote(project=project, vote_result=0)
    votePoll.save()

    # Mint NFT for the researcher
    mint_cert_owner(request, researcher_address, project_name, project_description)

    # Retrieve all vote histories for this project
    vote_histories = vote_history.objects.filter(project=project)

    # Update the reputation score for each validator who voted for this project
    for vote in vote_histories:
        if vote.vote.vote_result == 1:
            Validator.objects.filter(validator_address=vote.validator_address).update(
                reputation_score=F('reputation_score') + 1
            )
    
    return JsonResponse({'status': 'success', 'message': 'Research published successfully'})
