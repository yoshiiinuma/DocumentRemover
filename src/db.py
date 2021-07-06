"""
Handles DB access

    ArchivedRequests:
        RequestId
        Status
        ArchvieDate
        DaleteDate

    ArchivedFiles:
        ArvhiveFileId
        RequestId
        Status
        SrcFolder
        FileId
        OriginalId
        OriginalType
        OriginalPath
        OriginalFileName
        FileExtension
        MoveDate
"""
#pylint: disable=invalid-name
import re
from datetime import date
from src.mysql_base_client import MysqlBaseClient

class DB(MysqlBaseClient):
    """
    Handles DB access
    """
    def get_files_to_populate_drive_info(self, limit=1000, offset=0):
        """
        Gets ArchivedFiles data which need to populate Google Drive file info
        """
        SQL = f"""
                SELECT r.RequestId, ArchiveFileId, OriginalPath, OriginalType
                  FROM ArchivedRequests r
                  JOIN ArchivedFiles f
                    ON f.RequestId = r.RequestId
                 WHERE r.Status = 1
                   AND f.Status = 0
                   LIMIT {limit}  OFFSET {offset}
              """
        return self.query(SQL)

    @staticmethod
    def conv_requests_to_map(data):
        """
        Converts the query results from ArchivedFiles (get_files_to_populate_drive_info)
        into Map<fname, { requestId, archiveFileId }>
        """
        fmap = {}
        for rid, aid, fpath, _ in data:
            folder, fname = fpath.split('/')
            fmap[fname] = {
                'requestId': rid,
                'archiveFileId': aid,
                'originalPath': fpath,
                'folderName': folder,
                'originalFilename': fname }
        return fmap

    @staticmethod
    def conv_data_for_update(file_info, fmap):
        """
        Converts the query results from Google Drive (Drive#get_files_by_name)
        into the form that update_file_info expects
        """
        return [(
            ','.join(obj['parents']),
             obj['id'],
             obj['name'],
             obj['fileExtension'],
             fmap[obj['name']]['archiveFileId']
         ) for obj in file_info]

    def populate_archive_file_info(self, file_info, fmap):
        """
        Updates ArchivedFiles with information from Google Drive
        Sets 1 to ArchivedFile.Status
        """
        values = DB.conv_data_for_update(file_info, fmap)
        return self.update_file_info(values)

    def update_file_info(self, values):
        """
        Updates ArchivedFiles with information from Google Drive

        values: [(SrcFolderId, FileId, Name, FileExtension, ArchiveFileId)]
        """
        SQL = """
               UPDATE ArchivedFiles
                  SET Status = 1,
                      SrcFolder = %s,
                      FileId = %s,
                      OriginalFileName = %s,
                      FileExtension= %s
                WHERE ArchiveFileId = %s
              """
        return self.exec_many(SQL, values)

    def complete_file_info_population(self):
        """
        Updates ArchivedRequests Status after all the dependent ArchiveFiles
        get populted with Google Drive info
        Set 2 to ArchivedRequests.Status
        """
        SQL = """
               UPDATE ArchivedRequests r
                  SET r.Status = 2
                WHERE r.Status = 1
                  AND NOT EXISTS (
                      SELECT 1 FROM ArchivedFiles f
                       WHERE f.RequestId = r.RequestId
                         AND f.Status = 0
                  )
              """
        return self.exec(SQL)

    def set_deleted_file_to_requests(self):
        """
        Replaces with FileDeleted.png all the file paths of Requests that are
        in Archived Status 2
        SetDeletedFileImage sets 3 to ArchivedRequests.Status
        """
        return self.exec('CALL SetDeletedFileImage')

    def set_archive_flag_to_requests(self):
        """
        Set 1 to Archived column of Requests that are in Archived Status 3
        SetArchiveFlagToRequests:
            Sets 1 to Requests.Archived
            Sets 4 to ArchivedRequests.Status
        """
        return self.exec('CALL SetArchiveFlagToRequests')

    def get_requests_to_archive(self, limit = 1000):
        """
        Gets ArchivedFiles data which need to move to Archive folder

        OUTPUT: [(FileId, ArchiveFileId, SrcFolder)]
        """
        #fields = 'r.RequestId, ArchiveFileId, SrcFolder, FileId'
        fields = 'FileId, ArchiveFileId, SrcFolder'
        SQL = f"""
               SELECT {fields}
                 FROM ArchivedRequests r
                 JOIN ArchivedFiles f
                   ON f.RequestId = r.RequestId
                WHERE r.Status = 4
                  AND f.Status = 1
                LIMIT {limit}
              """
        return self.query(SQL)

    @staticmethod
    def conv_response_to_values(batch_rslt, archive_date):
        """
        Coverts batch responses

        INPUT

            batch_rslt: {
                'ArchiveFileId', {
                    'response': {
                        'kind', 'id', 'name', 'mimeType'
                    }
                }
            }

        OUTPUT

            [(FileId,)]
        """
        return [
            (obj['response']['id'],) for obj in batch_rslt.values()
        ]

    def set_archived_flag_to_files(self, batch_rslt, archive_date):
        """
        Sets MoveDate to ArchivedFiles
        Sets 2 to ArchivedFiles.Status

        INPUT
            values: [(MoveDate, FileId)]
        """
        formatted_date = re.sub(r'^(\d{4})(\d{2})(\d{2})$', r'\1-\2-\3', archive_date)
        SQL = f"""
               UPDATE ArchivedFiles
                  SET Status = 2,
                      MoveDate = '{formatted_date}' 
                WHERE Status = 1
                  AND FileId = %s
              """
        values = DB.conv_response_to_values(batch_rslt, archive_date)
        return self.exec_many(SQL, values)

    def complete_file_archive(self, archive_folder, archive_date):
        """
        Updates ArchivedRequests Status after all the files are moved to Archive folder
        Sets 5 to ArchivedRequests.Status when all the dependent ArchivedFiles are
        in Status 2

        INPUT
            archive_folder:         Archvie Folder ID
            archive_date (String): the date that the files are archived; yyyymmdd
        """
        formatted_date = re.sub(r'^(\d{4})(\d{2})(\d{2})$', r'\1-\2-\3', archive_date)
        SQL = f"""
               UPDATE ArchivedRequests r
                  SET r.Status = 5,
                      r.ArchiveFolder = '{archive_folder}',
                      r.ArchiveDate = '{formatted_date}'
                WHERE r.Status = 4
                  AND NOT EXISTS (
                        SELECT 1 FROM ArchivedFiles f
                         WHERE f.RequestId = r.RequestId
                           AND f.Status = 1)
              """
        return self.exec(SQL)

    def complete_file_delete(self, archive_date, delete_date = None):
        """
        Updates ArchivedRequests Status after all the files are deleted
        Set 6 to ArchivedRequests.Status
        """
        if not delete_date:
            formatted_delete_date = date.today().strftime('%Y-%m-%d')
        else:
            formatted_delete_date = re.sub(r'^(\d{4})(\d{2})(\d{2})$', r'\1-\2-\3', delete_date)
        formatted_archive_date = re.sub(r'^(\d{4})(\d{2})(\d{2})$', r'\1-\2-\3', archive_date)
        SQL = f"""
               UPDATE ArchivedRequests r
                  SET r.Status = 6,
                      r.DeleteDate = '{formatted_delete_date}'
                WHERE r.Status = 5
                  AND r.ArchiveDate = '{formatted_archive_date}'
              """
        return self.exec(SQL)

    def insert_archive_files(self, values):
        """
        Insert given values into ArchiveFiles

        values: [(RequestId, Status, OriginalType, OrginalPath)]
        """
        SQL = """
               INSERT INTO ArchivedFiles
                      (RequestId, Status, OriginalType, OriginalPath)
               VALUES (%s, %s, %s, %s)
              """
        return self.exec_many(SQL, values)

    def insert_requests(self, values):
        """
        Insert given values into Requests

        INPUT
            values: [
              RequestId,
              UserId,
              Owner,
              Status,
              `Application Confirmation ID`,
              `Request Date`,
              `Approval Date`,
              `Approval ID`,
              `Arrival Date`,
              `Exemption Category`,
              `Project Document 1`,
              `Project Document 2`,
              `Proof of Port of Embarkation`,
              `PCS Orders`,
              `Letter From Medical Provider`,
              `Nucleic Acid Amplification Test`,
              CreatedAt,
              CreatedBy,
              UpdatedAt,
              UpdatedBy
            ]
        """
        SQL = """
           INSERT INTO Requests
              (RequestId, UserId, Owner, Status, `Application Confirmation ID`,
              `Request Date`, `Approval Date`, `Approval ID`, `Arrival Date`,
              `Exemption Category`,
              `Project Document 1`, `Project Document 2`,
              `Proof of Port of Embarkation`, `PCS Orders`,
              `Letter From Medical Provider`, `Nucleic Acid Amplification Test`,
              CreatedAt, UpdatedAt, UpdatedBy)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              """
        return self.exec_many(SQL, values)

    def insert_travelers(self, values):
        """
        Inserts given values into Requests

        values:
            [ RequestId, TravelerId, Owner, `First Name`, `Last Name`, `Arrival Date`,
              `Picture ID`, CreatedAt, UpdatedAt, UpdatedBy ]
        """
        SQL = """
               INSERT INTO Travelers
                   (RequestId, TravelerId, Owner, `First Name`,
                    `Last Name`, `Arrival Date`, `Picture ID`,
                    CreatedAt, UpdatedAt, UpdatedBy)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              """
        return self.exec_many(SQL, values)

    def insert_documents(self, values):
        """
        Inserts given values into Requests

        values:
            [ RequestId, DocumentId, Owner, File,
              CreatedAt, UpdatedAt, UpdatedBy]
        """
        SQL = """
               INSERT INTO Documents
                   (RequestId, DocumentId, Owner, File,
                    CreatedAt, UpdatedAt, UpdatedBy)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
              """
        return self.exec_many(SQL, values)

    def get_file_info_by_archive_date(self, archive_date):
        """
        Gets ArchivedFiles data of archived on the specified date

        INPUT
            archive_date (String): the date that the files are archived; yyyymmdd
        """
        if not re.match(r'^20\d{2}\d{2}\d{2}$', archive_date):
            print('GET_FILE_INFO_BY_ARCHIVE_DATE: Invalid Date ' + archive_date)
            return None
        formatted_date = re.sub(r'^(\d{4})(\d{2})(\d{2})$', r'\1-\2-\3', archive_date)
        SQL = f"""
                SELECT r.RequestId, ArchiveFileId, OriginalId, ArchiveFolder, srcFolder,
                       FileId, OriginalPath, OriginalType, ArchiveDate, MoveDate
                  FROM ArchivedRequests r
                  JOIN ArchivedFiles f
                    ON f.RequestId = r.RequestId
                 WHERE r.ArchiveDate = '{formatted_date}'
                 ORDER BY RequestId, OriginalId
              """
        return self.query(SQL)

    def get_file_info_by_request_id(self, request_id):
        """
        Gets ArchivedFiles data of specified Request
        """
        SQL = f"""
                SELECT r.RequestId, ArchiveFileId, OriginalId, ArchiveFolder, srcFolder,
                       FileId, OriginalPath, OriginalType, ArchiveDate, MoveDate
                  FROM ArchivedRequests r
                  JOIN ArchivedFiles f
                    ON f.RequestId = r.RequestId
                 WHERE r.RequestId = '{request_id}'
                 ORDER BY RequestId, OriginalId
              """
        return self.query(SQL)

    @staticmethod
    def conv_data_for_restore(data):
        """
        Converts the results of DB.gets_requests_to_achive into array of object

        INPUT
            data: [(RequestId, ArchiveFileId, OriginalId, ArchiveFolder, srcFolder,
                   FileId, OriginalPath, OriginalType, ArchiveDate, MoveDate)]

        OUTPUT
            {
                request_ids: [(RequestId)]
                all_files: [{
                  id:   Google Drive File ID to move DELETE DIR
                  src:  Google Dirve Folder ID where the file is curretnly located
                  seq:  ArchiveFileId; used for Request ID for batch request
                  dst:  (OPTIONAL) Google Drive Folder ID to which the file will be moved
                }]
                request_files: [[f1, f2, f3, f4, f5, f6, RequestId]]
                traveler_files: [(OriginalPath, OriginalId)]
                document_files: [(OriginalPath, OriginalId)]
            }
        """
        requests = {}
        all_files = []
        request_files = []
        traveler_files = []
        doc_files = []
        for [rid, aid, oid, dst, src, fid, opath, otype, _, _] in data:
            all_files.append({ 'id': fid, 'src': dst, 'dst': src, 'seq': str(aid) })
            if otype == 7:
                traveler_files.append((opath, oid))
            elif otype == 8:
                doc_files.append((opath, oid))
            else:
                if not requests.get(rid):
                    requests[rid] = {}
                requests[rid][otype] = opath
        #request_ids = [(rid,) for rid in requests.keys()]
        request_ids = list(requests.keys())
        request_files = DB.merge_request_files(requests)
        return { 'request_ids': request_ids,
                 'all_files': all_files,
                 'request_files': request_files,
                 'traveler_files': traveler_files,
                 'document_files': doc_files }

    @staticmethod
    def merge_request_files(data):
        """
        Converts the results of DB.gets_requests_to_achive into array of object

        INPUT
            data: (RequestId, OriginalId, ArchiveFolder, srcFolder, FileId,
                   OriginalPath, OriginalType, ArchiveDate, MoveDate)
        OUTPUT
            [{
              id:   Google Drive File ID to move DELETE DIR
              src:  Google Dirve Folder ID where the file is curretnly located
              seq:  ArchiveFileId; used for Request ID for batch request
              dst:  (OPTIONAL) Google Drive Folder ID to which the file will be moved
            }]
        """
        values = []
        for rid in data.keys():
            val = ['NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', rid]
            for otype in data[rid].keys():
                val[otype - 1] = data[rid][otype]
            values.append(val)
        return values

    def undone_file_archive(self, values):
        """
        Restore ArchivedRequests and ArchviedFiles to the status before moving files
        """
        SQL = """
                UPDATE ArchivedRequests r, ArchivedFiles f
                   SET r.Status = 2,
                       r.ArchiveFolder = NULL,
                       r.ArchiveDate = NULL,
                       f.Status = 1,
                       f.MoveDate = NULL
                 WHERE r.RequestId = %s
                   AND f.RequestId = r.RequestId
              """
        return self.exec_many(SQL, values)

    def undone_request_file_path(self, values):
        """
        Restore Requests file paths
        """
        SQL = """
                UPDATE Requests
                   SET `Project Document 1` = %s,
                       `Project Document 2` = %s,
                       `Proof of Port of Embarkation` =  %s,
                       `PCS Orders` =  %s,
                       `Letter From Medical Provider` =  %s,
                       `Nucleic Acid Amplification Test` =  %s,
                       Archived = 0,
                       UpdatedBy = 'SYSTEMUSER'
                 WHERE RequestId = %s
                """
        return self.exec_many(SQL, values)

    def undone_traveler_file_path(self, values):
        """
        Restore Travlers file paths
        """
        SQL = """
                UPDATE Travelers
                   SET `Picture ID` = %s,
                       UpdatedBy = 'SYSTEMUSER'
                 WHERE TravelerId = %s
                """
        return self.exec_many(SQL, values)

    def undone_document_file_path(self, values):
        """
        Restore Documents file paths
        """
        SQL = """
                UPDATE Documents
                   SET File = %s,
                       UpdatedBy = 'SYSTEMUSER'
                 WHERE DocumentId = %s
              """
        return self.exec_many(SQL, values)

    def call_create_archive_dates(self, days1, days2):
        """
        Call CreateArchiveDates Stored Proc, which creates ArchiveDates and ArchiveDateSummary
        tables

        INPUT
            days1: retention period for regular requests until archive
            days2: retention period for irregular requests until archive
        """
        return self.exec('CALL CreateArchiveDates({days1}, {days2})')

    def call_create_upload_files(self):
        """
        Call CreateUploadFiles Stored Proc, which creates UploadedFiles TBL
        """
        return self.callproc('CreateUploadFiles')
