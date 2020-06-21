# Importing the major libraries 
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email 
import base64
from urlextract import URLExtract
import git
import os
from generate_music import *

# Major Functions -

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    
    # Comment if not necessary
    print('Received Service Successfully!')
    return service


def get_msg_id(service, user_id, search_string):
    
    """
    Searches for messages and returns the msg_if of 
    the first message found with the search string
    """
    
    try:
        search_id = service.users().messages().list(userId=user_id, q=search_string).execute()
        number_results = search_id['resultSizeEstimate']
        
        final_list = []
        if number_results>0:
            message_ids = search_id['messages']
            
            for ids in message_ids:
                final_list.append(ids['id'])
            print(len(final_list),' message(s) received from the given search string. Searching for the latest message...')
            return (final_list[0])
        
    except(errors.HttpError, error):
        print('An error occured %s') % error
                
def get_url_from_msg_id(service, user_id, msg_id):
    
    """
    Returns the message body given the message id
    """
    extractor = URLExtract()
    
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        content = message['payload']['parts'][0]['body']['data']
        msg_body = base64.urlsafe_b64decode(content).decode('utf-8')
        clean_str = " ".join(msg_body.split())
        url = extractor.find_urls(clean_str)
        repo_url = url[1][(url[1].find('=')+1):]
        print('Url received successfully for cloning the repository!🎉 - ', repo_url)
        return(repo_url)
            
    except(errors.HttpError, error):
        print('An error occured', error)

def clone_repo(dir_to_clone, repo_url, repo_name):
    
    try:
        git.Git(dir_to_clone).clone(repo_url)
        print('Sucessfully Cloned to the repository - ', repo_name, '! 🎉')
    except:
        print('There is an error in cloning. Please check if the directory already exists?')

def clone_repo_v2(dir_to_clone, repo_url, repo_name):
    
    # This is the command line approach. This works perfectly too!
    os.chdir(dir_to_clone) # Specifying the path where the cloned project needs to be copied
    os.system('git clone '+repo_url)

def main():
    # User Id
    user_id = 'me'

    # Search String is the search parameter
    # This search string gives the best result so don't change until the message content changes
    search_string = 'https://ununu-p2p.github.io/website/'

    # Calling the get_service method to recieve service object
    service = get_service()

    # Only get the body of the message with the first ID
    msg_id = get_msg_id(service=service, user_id=user_id, search_string=search_string)

    # Get the git repository url 
    repo_url=get_url_from_msg_id(service=service, user_id=user_id, msg_id=msg_id)
    
    # Get the repository name
    repo_name = repo_url[(repo_url.rfind('/')+1):]
    
    # Specify the directory to clone
    dir_to_clone='test_repos/'    
    
    # Clone into the directory
    clone_repo(dir_to_clone, repo_url, repo_name)
    
    # Specify the input midi file_dir
    # input_file_dir= dir_to_clone+repo_name+'/resources/'+'input_file.mid'
    # Sample midi file for testing - change this
    input_file_dir='input_midi_dir/input.mid'
    
    # Generated file will be saved at the resources folder of the cloned repository with 'input_generated.mid' name
    output_file_dir = dir_to_clone+repo_name+'/resources/'+ input_file_dir[(input_file_dir.rfind('/')+1):-4] +'_generated.mid'
    
    # Call the method and generate the same given the params.
    gen_music_from_input(input_file=input_file_dir, output_dir=output_file_dir)
    
    # Add the commit & push code here!

if __name__ == "__main__":
    main()
