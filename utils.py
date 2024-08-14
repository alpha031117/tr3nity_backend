
from datetime import datetime
import random
import ipfshttpclient

def convert_to_readable_timestamp(timestamp):
    """
    Convert a timestamp to a more readable format.
    
    Args:
        timestamp (str): The original timestamp in ISO 8601 format.
    
    Returns:
        str: The readable timestamp.
    """
    
    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# Get NFT from IPFS 
def get_file_from_ipfs(cid):
    try:
        print("Connecting to IPFS node...")
        api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
        
        print("Connection successful, retrieving file...")
        file_content = api.cat(cid)
        
        if file_content:
            print("File retrieved.")
            return file_content, None  # Return file content and no error
        else:
            return None, "No content found for the provided CID"
    
    except Exception as e:
        print(f"Error: {e}")
        return None, f"Error occurred: {e}"
    
# Get a random CID that has not been used yet.
def get_random_cid(available_cids, used_cids):
    available = list(set(available_cids) - used_cids)
    if not available:
        raise Exception("No available CIDs left.")
    
    return random.choice(available)
