"""
Generates sample test files on Google Drive
"""
#pylint: disable=invalid-name
import time
from src.drive import Drive
from src.db import DB

def get_files_to_populate(conf):
    """
    Returns UploadedFiles by using cursor
    """
    sql = """
            SELECT r.RequestId, CAST(FLOOR(@rownum:=@rownum+1) AS CHAR) AS ArchiveFileId, FilePath, FileType
              FROM UploadedFiles r, (SELECT @rownum:=0) seq
             ORDER BY r.RequestId
          """
    try:
        db = DB(conf)
        db.call_create_upload_files()
        limit = 1000
        offset = 0
        rslt = []
        while True:
            suffix = f'LIMIT {limit}  OFFSET {offset}'
            data = db.query(sql + suffix)
            rslt += data
            offset += limit
            if len(data) < limit:
                break
        db.close()
        return rslt
    except Exception as err:
        print(err)
        db.show_errors()
        return None

def get_files_to_populate_old(conf):
    """
    Returns ArchivedFiles that need detailed file information from Google Drive
    Run run_stored_procs before this function
    """
    try:
        rslt = []
        limit = 1000
        offset = 0
        db = DB(conf)
        db.connect()
        while True:
            data = db.get_files_to_populate_drive_info(limit, offset)
            if len(data) == 0:
                break
            rslt += data
            offset += limit
        db.close()
        return rslt
    except Exception as err:
        print(err)
        db.show_errors()
        return None

def get_file_names(conf):
    """
    Returns all the generated test data
    """
    SQL = """
            SELECT OriginalPath, ArchiveFileId
              FROM ArchivedFiles
             WHERE RequestId LIKE '!!%'
          """
    rslt = None
    try:
        db = DB(conf)
        rslt = db.query(SQL)
        db.close()
    except Exception as err:
        print(err)
        db.show_errors()
    return rslt

def folder_name_to_id(dirname, conf):
    """
    Converts ArchivedFile.OriginalPath dirname to Folder ID
    """
    if dirname == 'Travelers_Images':
        return conf['DRIVE_TRAVELER_IMAGES']
    if dirname == 'Travelers_Files_':
        return conf['DRIVE_TRAVELER_FILES']
    if dirname == 'Requests_Images':
        return conf['DRIVE_REQUEST_IMAGES']
    if dirname == 'Requests_Files_':
        return conf['DRIVE_REQUEST_FILES']
    if dirname == 'Documents_Images':
        return conf['DRIVE_DOCUMENT_IMAGES']
    return conf['DRIVE_DOCUMENT_FILES']

def get_copy_target(ext, conf):
    """
    Selects copy target from sample files by extension
    """
    if ext == 'jpg':
        return conf['SAMPLE_JPG']
    if ext == 'png':
        return conf['SAMPLE_PNG']
    if ext == 'docx':
        return conf['SAMPLE_DOCX']
    return conf['SAMPLE_PDF']

def extract_file_info(fpath, conf):
    """
    Extracts file info from ArchivedFile.OriginalPath
    """
    dirname, fname = fpath.split('/')
    rid, doctype, seq, ext = fname.split('.')
    folder_id = folder_name_to_id(dirname, conf)
    file_id = get_copy_target(ext, conf)
    return {
        'file_id': file_id,
        'folder_id': folder_id,
        'dirname': dirname,
        'fname': fname,
        'request_id': rid,
        'doc_type': doctype,
        'seq': seq,
        'ext': ext
    }

def convert_to_files(data, conf):
    """
    Converts the results from get_files_to_populate_drive_info into the format that
    Drive.batch_copy_and_rename accepts

    INPUT
      data: [(RequestId, ArchivedFileId, OriginalPath, OriginalType)]
      conf: configuration

    OUTPUT
      [{
        id:      Googld Drive File ID to copy
        name:    new name
        dst:     destination Folder ID
        seq:     ArchviedFileId; used for batch request ID
      }]
    """
    files = []
    for _, aid, fpath, _ in data:
        info = extract_file_info(fpath, conf)
        files.append({
            'id': info['file_id'],
            'name': info['fname'],
            'dst': info['folder_id'],
            'seq': str(aid)
        })
    return files

def generate_files(files, conf):
    """
    Generates test files by copying Sample files
    """
    try:
        client = Drive(conf)
        client.connect()
        limit = len(files)
        index = 0
        size = 30
        while index < limit:
            rslt = client.batch_copy_and_rename(files[index:index+size])
            index += size
            if rslt:
                print(rslt)
            else:
                client.show_errors()
            time.sleep(1)
        client.close()
        return True
    except Exception as err:
        print(err)
        return None

def generate(conf):
    """
    Generates files on Googld Drive for generated Requests, Travelers, and
    Documents data.
    Such data can be specified with the following conditions:
      ArchivedRequsts.Status = 1
      ArchivedFiles.Status = 0
    """
    data = get_files_to_populate(conf)
    files = convert_to_files(data, conf)
    return generate_files(files, conf)

def extract_data(data):
    """
    Extracts file name from ArchivedFiles.OriginalPath
    """
    names = []
    ids = {}
    for fpath, aid in data:
        name = fpath.split('/')[1]
        names.append(name)
        ids[name] = str(aid)
    return { 'names': names, 'archive_file_id': ids }

def delete_all(conf):
    """
    Deleted all the generated files on Googld Drive for test
    Such files can be specified with the following conditions:
      ArchivedRequsts.Status = 1
      ArchivedFiles.Status = 0
    """
    data = get_file_names(conf)
    data = extract_data(data)
    client = Drive(conf)
    client.connect()
    files = []
    limit = len(data['names'])
    index = 0
    size = 200
    while index < limit:
        files += client.get_files_by_name(data['names'][index:index+size])
        index += size
        time.sleep(1)
    if not files:
        print('No Files To Delete')
        client.close()
        return
    targets = []
    for obj in files:
        targets.append({
            'id': obj['id'],
            'seq': data['archive_file_id'][obj['name']]
        })
    index = 0
    size = 30
    while index < limit:
        rslt = client.batch_delete(targets[index:index+size])
        print(rslt)
        index += size
        time.sleep(1)
    client.close()
