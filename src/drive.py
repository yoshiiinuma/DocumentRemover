"""
Handles Google Drive API requests
"""
import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
  'https://www.googleapis.com/auth/drive'
]
CREDENTIALS = 'GOOGLE_APPLICATION_CREDENTIALS'
#FIELDS = 'kind, nextPageToken, files(id, originalFilename, parents, fileExtension, kind)'
FIELDS = 'kind, nextPageToken, files(id, name, parents, fileExtension, kind)'
#FIELDS = 'kind, nextPageToken, files(id, originalFilename, parents, fileExtension, kind, mimeType)'
MIME_FOLDER = 'application/vnd.google-apps.folder'

class Drive:
    """
    Google Drive API Client
    """
    def __init__(self, conf):
        """
        Drive API Client Constructor
        """
        self.conf = conf
        self.client = None
        self.creds = None
        self.errors = []
        self.responses = {}

    def _handle_response(self, request_id, response, exception):
        """
        Saves the response for batch request into self.responses
        """
        self.responses[request_id] = { 'response': response }
        #print('Request ID: ' + request_id, response)
        if exception:
            self.responses[request_id]['exeption'] = exception
            print(exception)

    def get_batch_results(self):
        """
        Returns batch reponses
        """
        return self.responses

    def is_valid_creds(self):
        """
        Checks if credentials are valid
        """
        if self.creds and self.creds.valid:
            return True
        return False

    def setup_creds(self):
        """
        Sets up the API token
        """
        if self.creds:
            if self.creds.valid:
                return True
            #if self.creds.expired and self.creds.refresh_token:
            if self.creds.expired:
                self.creds.refresh(Request())
                print(self.creds)
                return True
        if CREDENTIALS not in self.conf:
            self.errors.append(CREDENTIALS + ' Not Provided')
            return False
        if not os.path.exists(self.conf[CREDENTIALS]):
            self.errors.append(CREDENTIALS + ' Not Found: ' + self.conf[CREDENTIALS])
            return False
        account = self.conf['DRIVE_DELEGATE_ACCOUNT']
        self.creds = service_account.Credentials \
            .from_service_account_file(self.conf[CREDENTIALS], scopes=SCOPES, subject=account)
        return True

    def connect(self):
        """
        Sets up the API client
        """
        if self.client:
            return True
        if not self.setup_creds():
            return False
        self.client = build('drive', 'v3', credentials=self.creds)
        return True

    def close(self):
        """
        Deletes client and credentials
        """
        if not self.client:
            return False
        self.client = None
        self.creds = None
        return True

    def src_folder_ids(self):
        """
        Returns src folder ids
        """
        return [
            self.conf['DRIVE_TRAVELER_IMAGES'],
            self.conf['DRIVE_TRAVELER_FILES'],
            self.conf['DRIVE_REQUEST_IMAGES'],
            self.conf['DRIVE_REQUEST_FILES'],
            self.conf['DRIVE_DOCUMENT_IMAGES'],
            self.conf['DRIVE_DOCUMENT_FILES']]

    #def get_files_by_name(self, names, page_size = 1000, page_token = '', fields = FIELDS):
    def get_files_by_name(self, names, page_size = 200, fields = FIELDS):
        """
        Returns list of files specified by the given names
        """
        if not names:
            self.errors.append('GET_FILES_BY_NAME: Names Not Provided')
            return None
        files = []
        src_folders = ' or '.join([ f"'{fid}' in parents" for fid in self.src_folder_ids()])
        search_names = ' or '.join([f"name = '{name}'" for name in names])
        query = '(' + src_folders + ') and (' + search_names + ')'
        #return self.list(query, page_size, page_token, fields)
        page_token = ''
        while True:
            rslt = self.list(query, page_size, page_token, fields)
            files += rslt['files']
            page_token = rslt.get('nextPageToken')
            if not page_token:
                break
        return files

    def get_files_in_folder(self, folder_id, page_size = 1000, page_token = '', fields = FIELDS):
        """
        Returns list of files located in the specified folder
        """
        if not folder_id:
            self.errors.append('GET_FILES_IN_FOLDER: FolderId Not Provided')
            return None
        query = f"'{folder_id}' in parents"
        return self.list(query, page_size, page_token, fields)

    def list(self, query, page_size = 1000, page_token = '', fields = FIELDS):
        """
        Returns list of files specified by the given query
        """
        if not query:
            self.errors.append('LIST: Query Not Provided')
            return None
        if not self.client:
            self.errors.append('LIST was called without Initialization')
            return None
        return self.client.files() \
                   .list(q=query, pageSize=page_size, pageToken=page_token, fields=fields) \
                   .execute()

    def create_file(self, filepath, dst_folder_id):
        """
        Creates a document in the given folder
        """
        if not self.client:
            self.errors.append('CREATE_FILE was called without Initialization')
            return None
        if not filepath:
            self.errors.append('CREATE_FILE: FilePath Not Provided')
            return None
        if not dst_folder_id:
            self.errors.append('CREATE_FILE: DestFolderId Not Provided')
            return None
        if not os.path.exists(filepath):
            self.errors.append('CREATE_FILE: File Not Exist')
            return None
        meta = { 'name': os.path.basename(filepath), 'parents': [ dst_folder_id ] }
        media = MediaFileUpload(filepath)
        return self.client.files() \
                   .create(body=meta, media_body=media, fields='id,name') \
                   .execute()

    def find_folder(self, name, dst_folder_id):
        """
        Find a folder with a specified name in the specified folder
        """
        if not self.client:
            self.errors.append('FIND_FOLDER was called without Initialization')
            return None
        if not name:
            self.errors.append('FIND_FOLDER: Name Not Provided')
            return None
        if not dst_folder_id:
            self.errors.append('FIND_FOLDER: Dest Folder ID Not Provided')
            return None
        query = f"'{dst_folder_id}' in parents and name = '{name}' and mimeType = '{MIME_FOLDER}'"
        rslt = self.client.files().list(q=query, fields='files(id,name)').execute()
        if rslt and rslt['files']:
            return rslt['files'][0]
        return None

    def create_folder(self, name, dst_folder_id):
        """
        Creates a folder in the specified folder
        Returns an exisitng folder if found one with the same name
        """
        if not self.client:
            self.errors.append('CREATE_FOLDER was called without Initialization')
            return None
        if not name:
            self.errors.append('CREATE_FOLDER: Name Not Provided')
            return None
        if not dst_folder_id:
            self.errors.append('CREATE_FOLDER: Dest Folder ID Not Provided')
            return None
        folder = self.find_folder(name, dst_folder_id)
        if folder:
            return folder
        meta = {
            'name': name,
            'mimeType': MIME_FOLDER,
            'parents': [ dst_folder_id ]
        }
        return self.client.files().create(body=meta, fields='id,name').execute()

    def copy_file(self, file_id, dst_folder_id):
        """
        Copies the specified file into the specified folder
        """
        if not self.client:
            self.errors.append('COPY was called without Initialization')
            return None
        if not file_id:
            self.errors.append('COPY: File ID Not Provided')
            return None
        if not dst_folder_id:
            self.errors.append('COPY: Dest Folder ID Not Provided')
            return None
        body = {'parents': [dst_folder_id]}
        return self.client.files().copy(fileId=file_id, body=body).execute()

    def copy_file2(self, file_id, dst_folder_id):
        """
        Copies the specified file into the specified folder
        """
        if not self.client:
            self.errors.append('COPY was called without Initialization')
            return None
        if not file_id:
            self.errors.append('COPY: File ID Not Provided')
            return None
        if not dst_folder_id:
            self.errors.append('COPY: Dest Folder ID Not Provided')
            return None
        return self.client.files() \
                   .update(fileId=file_id, addParents=dst_folder_id) \
                   .execute()

    def move_file(self, file_id, src_folder_id, dst_folder_id):
        """
        Moves the specified file from src folder to dest folder
        """
        if not self.client:
            self.errors.append('MOVE was called without Initialization')
            return None
        if not file_id:
            self.errors.append('MOVE: File ID Not Provided')
            return None
        if not src_folder_id:
            self.errors.append('MOVE: Src Folder ID Not Provided')
            return None
        if not dst_folder_id:
            self.errors.append('MOVE: Dest Folder ID Not Provided')
            return None
        return self.client.files() \
                   .update(fileId=file_id, \
                           removeParents=src_folder_id, \
                           addParents=dst_folder_id) \
                   .execute()

    def delete_file(self, file_id):
        """
        Deletes the specified file
        """
        if not self.client:
            self.errors.append('DELETE was called without Initialization')
            return None
        if not file_id:
            self.errors.append('DELETE: File ID Not Provided')
            return None
        return self.client.files().delete(fileId=file_id).execute()

    def delete_folder(self, folder_id):
        """
        Deletes the specified folder
        """
        if not self.client:
            self.errors.append('DELETE was called without Initialization')
            return None
        if not folder_id:
            self.errors.append('DELETE: Folder ID Not Provided')
            return None
        return self.client.files().delete(fileId=folder_id).execute()

    def batch_move(self, files, dst_folder_id = ''):
        """
        Moves the specified files from src folder to dest folder

        INPUT
            files:
              [{
                id:    Google Drive File ID to move DELETE DIR
                src:   Google Dirve Folder ID where the file is curretnly located
                seq:   ArchiveFileId; used for Request ID for batch request
                dst:   (OPTIONAL) Google Drive Folder ID to which the file will be moved
              }]

            dst_folder_id: Google Drive Folder ID to which the file will be moved;
                           ignored when 'dest' is provided

        OUTPUT
            All the responses for each batch request
        """
        if not self.client:
            self.errors.append('BATCH_MOVE was called without Initialization')
            return None
        if not files:
            self.errors.append('BATCH_MOVE: Files Not Provided')
            return None
        #if not dst_folder_id:
        #    self.errors.append('BATCH_MOVE: Dest Folder ID Not Provided')
        #    return None
        self.responses = {}
        service = self.client
        batch = self.client.new_batch_http_request(callback=self._handle_response)
        for obj in files:
            dst = obj['dst'] if obj.get('dst') else dst_folder_id
            print(obj)
            batch.add(service.files() \
                             .update(fileId=obj['id'], \
                                     removeParents=obj['src'], \
                                     addParents=dst),
                      request_id=obj['seq'])
        batch.execute()
        return self.responses

    def batch_copy(self, files, dst_folder_id):
        """
        Copies the specified files from src folder to dest folder

        INPUT
            files:
              [{
                id:     Google Drive File ID to copy
                seq:    ArchiveFileId; used for Request ID for batch request
                dst:    (OPTIONAL) Google Drive Folder ID to which the file will be copied
              }]

        OUTPUT
            All the responses for each batch request
        """
        if not self.client:
            self.errors.append('BATCH_COPY was called without Initialization')
            return None
        if not files:
            self.errors.append('BATCH_COPY: Files Not Provided')
            return None
        if not dst_folder_id:
            self.errors.append('BATCH_COPY: Dest Folder ID Not Provided')
            return None
        self.responses = {}
        service = self.client
        batch = self.client.new_batch_http_request(callback=self._handle_response)
        for obj in files:
            body = { 'parents': [obj['dst'] if obj.get('dst') else dst_folder_id] }
            batch.add(service.files().copy(fileId=obj['id'], body=body), request_id=obj['seq'])
        batch.execute()
        return self.responses

    def batch_copy_and_rename(self, files, dst_folder_id = ''):
        """
        Copies the specified files from src folder to dest folder

        INPUT
            files:
              [{
                id:     Google Drive File ID to copy
                name:   new name
                seq:    ArchiveFileId; used for Request ID for batch request
                dst:    (OPTIONAL) Google Drive Folder ID to which the file will be copied
              }]

        OUTPUT
            All the responses for each batch request
        """
        if not self.client:
            self.errors.append('BATCH_COPY_AND_RENAME was called without Initialization')
            return None
        if not files:
            self.errors.append('BATCH_COPY_AND_RENAME: Files Not Provided')
            return None
        #if not dst_folder_id:
        #    self.errors.append('BATCH_COPY_AND_RENAME: Dest Folder ID Not Provided')
        #    return None
        self.responses = {}
        service = self.client
        batch = self.client.new_batch_http_request(callback=self._handle_response)
        for obj in files:
            body = {
                'name': obj['name'],
                'parents': [obj['dst'] if obj.get('dst') else dst_folder_id]
            }
            batch.add(service.files().copy(fileId=obj['id'], body=body), request_id=obj['seq'])
        batch.execute()
        return self.responses

    def batch_delete(self, files):
        """
        Deletes specified files

        INPUT
            files:
              [{
                id:     Google Drive File ID to copy
                seq:    ArchiveFileId; used for Request ID for batch request
              }]

        OUTPUT
            All the responses for each batch request
        """
        if not self.client:
            self.errors.append('BATCH_DELETE was called without Initialization')
            return None
        if not files:
            self.errors.append('BATCH_DELETE: Files Not Provided')
            return None
        self.responses = {}
        service = self.client
        batch = self.client.new_batch_http_request(callback=self._handle_response)
        for obj in files:
            batch.add(service.files().delete(fileId=obj['id']), request_id=obj['seq'])
        batch.execute()
        return self.responses

    def show_errors(self):
        """
        Displays errors
        """
        for err in self.errors:
            print(err)

    def show_conf(self):
        """
        Displays configuration
        """
        print(self.conf)

    @staticmethod
    def extract_id(data):
        """
        Converts list data to array of File IDs
        """
        return [ obj['id'] for obj in data['files'] ]

    @staticmethod
    def extract_id_and_folder(data):
        """
        Converts list data to array of file IDs and parent folder IDs

        OUTPUT
          [{
            id:    Google Drive File ID to move DELETE DIR
            src:   Google Dirve Folder ID where the file is curretnly located
          }]
        """
        return [
            {
                'id': obj['id'],
                'src': ','.join(obj['parents'])
            } for obj in data['files']
        ]
