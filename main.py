
from datetime import date
from datetime import timedelta
from src.archive import Archive

def log_event(context, caller):
    """
    Logs Pub/Sub event
    """
    print(f'{caller}: EventID {contet.event_id} {context.resource["name"]} {context.timestamp}')

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
    cnt = archive.move_files_to_archive_dir(archive_date)

def delete_files(message, context):
    """
    Deletes folder archived 30 days ago

    Sets 6 to ArchivedRequests.Status
    """
    log_event(context, 'DELETE_FILES')
    print(message)
    #RETENTION_PERIOD = 31
    RETENTION_PERIOD = 6
    archive = Archive()
    archive_date = (date.today() - timedelta(RETENTION_PERIOD)).strftime('%Y%m%d')
    rslt = archive.delete_folder(archive_date)
