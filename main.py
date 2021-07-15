
import base64
import re
from datetime import date
from datetime import timedelta
from src.archive import Archive

def log_event(context, caller):
    """
    Logs Pub/Sub event
    """
    print(f'{caller}: EventID {context.event_id} {context.resource["name"]} {context.timestamp}')

def populate_files(message, context):
    """
    Updates ArchivedFiles with information from Google Drive

    Sets 1 to ArchivedFiles.Status
    Sets 2 to ArchivedRequests.Status when all the dependent files Status = 1
    """
    log_event(context, 'POPULATE_FILES')
    archive = Archive()
    total = 0
    limit = 200
    while True:
        cnt = archive.populate_file_info(limit)
        if cnt == 0:
            break
        total += cnt
        print(f'POPULATE_FILE_INFO: CUR {cnt} / TOTAL {total} ArchivedFiles Populated')
    print(f'POPULATE_FILE_INFO: {total} ArchivedFiles Populated')

def set_deleted_file_path(message, context):
    """
    Replaces file paths of deleted files with FileDeleted.png

    Call stored proc SetDeletedFileImage 
    Sets 3 to ArchivedRequests.Status
    """
    log_event(context, 'SET_DELETED_FILE_PATH')
    archive = Archive()
    rslt = archive.set_deleted_file_to_requests()
    #print(f'{rslt} records are updated') not work
    print('SetDeletedFilePath Completed')

def set_archive_flag(message, context):
    """
    Replaces deleted file path with FileDeleted.png

    Call stored proc SetDeletedFileImage 
    Sets 1 to Requests.Archived
    Sets 4 to ArchivedRequests.Status
    """
    log_event(context, 'SET_ARCHIVE_FLAG')
    archive = Archive()
    rslt = archive.set_archive_flag_to_requests()
    print(f'{int(rslt/2)} Requests Archived')
    print(f'{int(rslt/2)} ArchivedRequests Updated')

def move_files(message, context):
    """
    Moves files to Archive folder

    Sets 2 to ArchivedFiles.Status
    Sets 4 to ArchivedRequests.Status if all the dependent files have Status 2
    """
    log_event(context, 'MOVE_FILES')
    archive = Archive()
    archive_date = date.today().strftime('%Y%m%d')
    if 'data' in message:
        raw_data = base64.b64decode(message['data']).decode('utf-8')
        matched = re.search(r'DATE=(20\d{6})', raw_data)
        if matched:
            archive_date = matched[1]
    print(f'MOVE_FILES: archive_date {archive_date}')
    cnt = archive.move_files_to_archive_dir(archive_date)

def delete_files(message, context):
    """
    Deletes folder archived 30 days ago

    Sets 6 to ArchivedRequests.Status
    """
    log_event(context, 'DELETE_FILES')
    retention_period = 30
    current_date = date.today().strftime('%Y%m%d')
    archive = Archive()
    #archive_date = (date.today() - timedelta(retention_period)).strftime('%y%m%d')
    print(message['data'])
    if 'data' in message:
        raw_data = base64.b64decode(message['data']).decode('utf-8')
        matched = re.search(r'DATE=(20\d{6})', raw_data)
        if matched:
            current_date = matched[1]
        matched = re.search(r'RETENTION=(\d{1,3})', raw_data)
        if matched:
            retention_period = int(matched[1])
    print(f'DELETE_FILES: current_date {current_date}, retention_period {retention_period}')
    archive.delete_folder_by_current_date(current_date, retention_period)
