import json
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
import logging
from utils import convert_to_readable_timestamp, get_random_cid, get_file_from_ipfs
from datetime import datetime
from vote_project.models import Validator, Vote, vote_history
from grants_project.models import Project, Grant
from django.db.models import F


# This would be your database or persistent storage in a real application.
used_cids = set()  # A set of already used CIDs.
available_cids = ['QmUwivpSjVnzDaMEUZ47tHhmZbeao3eZQFqt2nKf5QzyaH', 'QmVWv7qDQTVeU5epzhVxBk29sAhqvw95WUJoCtVhQvnqcX', 'QmZTc14zx1ZU2potKcvq1hRdRdkn2m8NLtREBEg4zUyn5K']  # List of all possible CIDs.

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
WALLET_ADDRESS_RESERCHER_ADMIN = '0x3003E934783dD85d40c2cf76d274c689dF5975F6'
WALLET_ADDRESS_OWNER_ADMIN_1 = '0x5b3a8eCB9677F56e46d67B7e69900cE322c030d1'

OWNER_CONTRACT_ADDRESS = '0xFa3D1712858bd8a4451ff6dD4948236123BE6664'
GORV_CONTRACT_ADDRESS = '0xBB165A89B8bB2C21cC433100180AbBEC5f614035'
PDF_CONTRACT_ADDRESS = '0x161895f32A8eA73433162192819c2e36113AB4ae'

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
@api_view(['POST'])
def mint_cert_validator(request):
    mint_headers = {
        'client_id': f'{API_KEY}',
        'client_secret': f'{API_PASSWORD}'
    }

    API_URL = f'{BASE_API_URL}/mint-certificate'
    CALLBACK_URL = 'https://127.0.0.1:8000/'

    data = request.data
    validator_address = data.get('validator_address')

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

# Function to fetch token ID
def fetch_pdf_url_from_response(response, token_id_to_find):
    try:
        response_data = response.json()  # Parse the JSON response into a Python dictionary

        # Check if response_data is a dictionary and has the key 'result'
        if isinstance(response_data, dict) and 'result' in response_data:
            result_list = response_data['result']

            # Ensure 'result' is a list
            if isinstance(result_list, list):
                # Iterate over the list to find the matching nft_token_id
                for item in result_list:
                    if isinstance(item, dict) and item.get('nft_token_id') == int(token_id_to_find):
                        return item['certificate_image_file']
                
                print(f"Error: No matching 'nft_token_id' found in the result list")
            else:
                print("Error: 'result' is not a list")
        else:
            print("Error: Response data is not in the expected format")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
    
    return None

# Get List of PDF Reseacher
@api_view(['GET'])
def get_pdf_researcher(request, researcher_address, tokenID):
    """
    Fetch the list of certificate from the external API.
    
    Returns:
        JsonResponse: A JSON response with the status and data or error message.
    """

    tx_id = ""
    status = ""
    
    API_URL = f'{BASE_API_URL}/get-certificate?from={WALLET_ADDRESS_RESERCHER_ADMIN}&to={researcher_address}&contract_address={PDF_CONTRACT_ADDRESS}&transaction_id={tx_id}&status={status}'

    try:
        # Make the GET request to the external API
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        
        if response.status_code == 200:
            # Retrieve only the matched tokenID
            matched_data = fetch_pdf_url_from_response(response, tokenID)
            logger.info(f"Response Data: {matched_data}")
            return JsonResponse({'status': 'success', 'data': matched_data})
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

# Upload Research
@api_view(['POST'])
def upload_research(request):
    try:
        data_received = request.data

        required_fields = [
            'grant', 'researcher_address', 'project_name', 'project_description', 
            'start_date', 'end_date', 'team_members', 'upload_file'
        ]

        # Check for missing fields
        missing_fields = [field for field in required_fields if not data_received.get(field)]
        if missing_fields:
            return JsonResponse({
                'status': 'error', 
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }, status=400)

        grant_id = data_received.get('grant')
        researcher_address = data_received.get('researcher_address')
        project_name = data_received.get('project_name')
        project_description = data_received.get('project_description')
        start_date = data_received.get('start_date')
        end_date = data_received.get('end_date')
        team_members = data_received.get('team_members')
        upload_file = request.FILES.get('upload_file')
        aim = data_received.get('aim')
        timeline = data_received.get('timeline')

        if not upload_file:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded'}, status=400)

        pdf_upload_token = upload_nft_pdf(upload_file, researcher_address, project_name, project_description)

        if not pdf_upload_token:
            return JsonResponse({'status': 'error', 'message': 'Error uploading the file to Chain'}, status=500)
        
        logger.info(f"Grant: {grant_id}")
        logger.info(f"Researcher Address: {researcher_address}")
        logger.info(f"Project Name: {project_name}")
        logger.info(f"Project Description: {project_description}")
        logger.info(f"Start Date: {start_date}")
        logger.info(f"End Date: {end_date}")
        logger.info(f"Team Members: {team_members}")
        logger.info(f"Upload File Token ID: {pdf_upload_token}")

        grant = Grant.objects.get(pk=grant_id)

        # Store project details
        project = Project(
            grant=grant,
            name=project_name,
            description=project_description,
            aim=aim,
            timeline=timeline,
            start_time=start_date,
            end_time=end_date,
            team_members=team_members,
            pdf_uploaded=pdf_upload_token,
            created_by=researcher_address
        )

        project.save()

        # Store the votePoll for the project
        votePoll = Vote(project=project)
        votePoll.save()

        return JsonResponse({'status': 'success', 'message': 'Research uploaded successfully'})

    except Exception as e:
        logger.error(f"Error uploading research: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'An error occurred while uploading the research'}, status=500)

# When project research is published, store project's details & mint NFT for the researcher
def publish_research(request, project_id):

    try:
        # Update project's status to published
        project = Project.objects.get(pk=project_id)

        if project.status == 'published':
            return JsonResponse({'status': 'error', 'message': 'Research has already been published'}, status=400)
        
        if not project:
            return JsonResponse({'status': 'error', 'message': 'Project not found'}, status=404)

        researcher_address = project.created_by
        project_name = project.name
        project_description = project.description

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
        
        project.status = 'published'
        project.save()
        return JsonResponse({'status': 'success', 'message': 'Research published successfully'})
    
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

# Add pdf into chain
def upload_nft_pdf(file, reseacher_address, project_name, project_description):
    
    mint_headers = {
        'client_id': f'{API_KEY}',
        'client_secret': f'{API_PASSWORD}'
    }

    API_URL = f'{BASE_API_URL}/mint-certificate'
    CALLBACK_URL = 'https://127.0.0.1:8000/'

    data = {
        'wallet_address': WALLET_ADDRESS_RESERCHER_ADMIN,
        'to': reseacher_address,
        'contract_address': PDF_CONTRACT_ADDRESS,
        'file': (f"{project_name}-proposal.pdf", file),
        'attributes': json.dumps([
            {"trait": "Project Description", "value": project_description}
        ]),
        'name': "PDF NFT Certificate",
        'description': f"Proposal {project_name} NFT",
        'callback_url': CALLBACK_URL
    }
    
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

    response_json = response.json()
    result = response_json.get('result', {})
    nft_token_id = result.get('nft_token_id')


    return nft_token_id
