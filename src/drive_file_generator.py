"""
Generates sample test files on Google Drive
"""
#pylint: disable=invalid-name
import traceback
import time
from src.drive import Drive
from src.db import DB

def call_create_upload_files(conf):
    """
    Calls CreateUploadFiles Stored Proc, which creates UploadedFiles TBL
    """
    try:
        db = DB(conf)
        rslt = db.call_create_upload_files()
        db.close()
        return rslt
    except Exception as err:
        traceback.print_exc()
        print(err)
        db.show_errors()
        return None

def get_files_to_populate(conf, limit = 1000, offset = 0, total_max = 10000):
    """
    Returns UploadedFiles by using cursor

    NOTE: Use call_craete_upload_files before this
    """
    try:
        db = DB(conf)
        #db.call_create_upload_files()
        total = 0
        rslt = []
        while total < total_max:
            sql = f"""
                    SELECT r.RequestId, CAST(FLOOR(@rownum:=@rownum+1) AS CHAR) AS ArchiveFileId, FilePath, FileType
                      FROM UploadedFiles r, (SELECT @rownum:={offset}) seq
                     ORDER BY r.RequestId
                     LIMIT {limit}  OFFSET {offset}
                  """
            data = db.query(sql)
            size = len(data)
            total += size
            rslt += data
            offset += limit
            if size < limit:
                break
        db.close()
        return rslt
    except Exception as err:
        traceback.print_exc()
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
        traceback.print_exc()
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
        traceback.print_exc()
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

    Ignore invalid file paths

    Invalid File Path:
        Empty string (907)
        No '/' (1168)
               e.g. "The selected image could not be found.#filename=Lilian%20ID.jpg"
                    "data:#filename=Covid-19%20Exception.pdf "
        With '/' (6)
                    "data:application/pdf;base64,#filename=COVID%20EXEMPTION%20LETTER.pdf"
                    "data:image/png;base64,iVBORw0KGgoAAAA......"
    """
    if '/' not in fpath:
        return None
    if fpath.startswith('data:'):
        return None
    dirname, fname = fpath.split('/')
    extra = ''
    ext = ''
    rid, doctype, seq, *rest = fname.split('.')
    ext = rest.pop()
    if len(rest) == 1:
        extra = rest.pop()
    elif len(rest) > 1:
        print(f'UNEXPECTED FILE NAME: {rid} {fname}')
        extra = '.'.join(rest)

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
        'extra': extra,
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
        if info:
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
                print(f'DriveFileGenerator#generate_files: limit {limit}, index {index}, rslt {len(rslt)}')
                #print(rslt)
            else:
                client.show_errors()
            time.sleep(1)
        client.close()
        return True
    except Exception as err:
        traceback.print_exc()
        print(err)
        return None

def generate(conf, limit = 1000, offset = 0, total_max = 10000):
    """
    Generates files on Googld Drive for generated Requests, Travelers, and
    Documents data.
    Such data can be specified with the following conditions:
      ArchivedRequsts.Status = 1
      ArchivedFiles.Status = 0
    """
    data = get_files_to_populate(conf, limit, offset, total_max)
    files = convert_to_files(data, conf)
    return generate_files(files, conf)

def get_files_by_request_ids(conf, request_ids):
    """
    Returns UploadedFiles by using cursor

    NOTE: Use call_craete_upload_files before this
    """
    sql = f"""
            SELECT RequestId, ArchiveFileId, OriginalPath, OriginalType
              FROM ArchivedFiles
             WHERE RequestId IN ({request_ids})
               AND Status = 0
             ORDER BY RequestId
          """
    try:
        db = DB(conf)
        rslt = db.query(sql)
        db.close()
        return rslt
    except Exception as err:
        traceback.print_exc()
        print(err)
        db.show_errors()
        return None

def generate_by_request_ids(conf, request_ids):
    """
    Generates files on Googld Drive for generated Requests, Travelers, and
    Documents data.
    Such data can be specified with the following conditions:
      ArchivedRequsts.Status = 1
      ArchivedFiles.Status = 0
    """
    data = get_files_by_request_ids(conf, request_ids)
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
