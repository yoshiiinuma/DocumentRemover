"""
Archive Manager
"""
#pylint: disable=invalid-name
import re
import time
from datetime import datetime
from datetime import timedelta
from datetime import date
import src.config as Config
from src.drive import Drive
from src.db import DB

class Archive:
    """
    Archive Manager
    """
    def __init__(self, envpath = '.env'):
        """
        Constructor
        """
        self.conf = Config.load(envpath)
        self.db = DB(self.conf)
        self.drive = Drive(self.conf)

    def _open(self):
        self.db.connect()
        self.drive.connect()

    def _close(self):
        self.db.close()
        self.drive.close()

    def populate_file_info(self, limit = 1000):
        """
        Updates ArchivedFiles with information from Google Drive

        Sets 1 to ArchivedFiles.Status
        Sets 2 to ArchivedRequests.Status when all the dependent files Status = 1
        """
        try:
            self._open()
            requests = self.db.get_files_to_populate_drive_info(limit)
            if not requests:
                self._close()
                return 0
            #cnt = len(requests)
            fmap = DB.conv_requests_to_map(requests)
            names = fmap.keys()
            files = self.drive.get_files_by_name(names)
            cnt_files = self.db.populate_archive_file_info(files, fmap)
            print(f'ARCHIVE.POPULATE_FILE_INFO: {cnt_files} ArchivedFile Populated')
            cnt_reqs = self.db.complete_file_info_population()
            print(f'ARCHIVE.POPULATE_FILE_INFO: {cnt_reqs} ArchivedRequest Updated')
            self._close()
            return cnt_files if cnt_files else 0
        except Exception as err:
            print(err)
            self._close()
            return 0

    def set_deleted_file_to_requests(self):
        """
        Replaces file paths of deleted files with FileDeleted.png

        Call stored proc SetDeletedFileImage
        Sets 3 to ArchivedRequests.Status
        """
        try:
            self.db.connect()
            rslt = self.db.set_deleted_file_to_requests()
            self.db.close()
            return rslt
        except Exception as err:
            print(err)
            return err

    def set_archive_flag_to_requests(self):
        """
        Replaces deleted file path with FileDeleted.png

        Call stored proc SetDeletedFileImage
        Sets 1 to Requests.Archived
        Sets 4 to ArchivedRequests.Status
        """
        try:
            self.db.connect()
            rslt = self.db.set_archive_flag_to_requests()
            self.db.close()
            return rslt
        except Exception as err:
            print(err)
            return err

    @staticmethod
    def conv_to_moving_files(data, dst_folder_id = None):
        """
        Converts the results of DB.gets_requests_to_achive into array of object

        INPUT
            data: [(FileId, ArchvieFileId, SrcFolder)]

        OUTPUT
            [{
              id:   Google Drive File ID to move DELETE DIR
              src:  Google Dirve Folder ID where the file is curretnly located
              seq:  ArchiveFileId; used for Request ID for batch request
              dst:  (OPTIONAL) Google Drive Folder ID to which the file will be moved
            }]
        """
        files = []
        for [fid, aid, parent] in data:
            obj = { 'id': fid, 'src': parent, 'seq': str(aid) }
            if dst_folder_id:
                obj['dst'] = dst_folder_id
            files.append(obj)
        return files

    def move_files_to_archive_dir(self, archive_date):
        """
        Moves files to Archive folder
        Sets 2 to ArchivedFiles.Status
        Sets 5 to ArchivedRequests.Status if all the dependent files have Status 2

        INPUT
            archive_date (String): the date that the files are archived; yyyymmdd
        """
        print(f'ARCHIVE.MOVE_FILES_TO_ARCHIVE_DIR: {archive_date}')
        if not archive_date:
            archive_date = date.today().strftime('%Y%m%d')
        if not re.match(r'^20\d{2}\d{2}\d{2}$', archive_date):
            print('ARCHIVE.MOVE_FILES_TO_ARCHIVE_DIR: Invalid Date ' + archive_date)
            return 0
        #try:
        cnt = 0
        self._open()
        rslt = self.drive.create_folder(archive_date, self.conf['DRIVE_DELETED_FILES'])
        dst_folder_id = rslt['id']
        while True:
            rslt = self.db.get_requests_to_archive()
            if not rslt:
                print('ARCHIVE.MOVE_FILES_TO_ARCHIVE_DIR: NO MORE DATA')
                break
            files = Archive.conv_to_moving_files(rslt)
            limit = len(files)
            print(f'ARCHIVE.MOVE_FILES_TO_ARCHIVE_DIR: PROCESSING ({limit})')
            index = 0
            size = 50
            while index < limit:
                batch_rslt = self.drive.batch_move(files[index:index+size], dst_folder_id)
                rslt = self.db.set_archived_flag_to_files(batch_rslt, archive_date)
                cnt += rslt
                index += size
                print(f'ARCHIVE.MOVE_FILES_TO_ARCHIVE_DIR: CUR {rslt} / TOTAL {cnt} Processed')
                time.sleep(1)
        rslt = self.db.complete_file_archive(dst_folder_id, archive_date)
        print(f'ARCHIVE.MOVE_FILES_TO_ARCHIVE_DIR: {rslt} Requests Processed')
        print(f'ARCHIVE.MOVE_FILES_TO_ARCHIVE_DIR: {cnt} Files Moved')
        self._close()
        return cnt
        #except Exception as err:
        #    print(err)
        #    return 0

    def delete_folder_by_current_date(self, current_date = None, retention_period = 30):
        """
        Delete folder archived on the specified date under DELETE folder
        Sets 6 to ArchivedRequests.Status

        INPUT
            current_date (String): the date on which folder is deleted; yyyymmdd
        """
        if not current_date:
            print('ARCHIVE.DELETE_FOLDER_BY_CURRENT_DATE: No Current Date Provided')
            return None
        if not re.match(r'^20\d{2}\d{2}\d{2}$', current_date):
            print('ARCHIVE.DELETE_FOLDER_BY_CURRENT_DATE: Invalid Date ' + current_date)
            return None
        archive_date = (
            datetime.strptime(current_date, '%Y%m%d') - timedelta(retention_period)
        ).strftime('%Y%m%d') 
        return self.delete_folder(archive_date, current_date)

    def delete_folder(self, archive_date, delete_date = None):
        """
        Delete folder archived on the specified date under DELETE folder
        Sets 6 to ArchivedRequests.Status

        INPUT
            archive_date (String): the date that the files are archived; yyyymmdd
            delete_date (String): the date that the files are deleted; yyyymmdd
        """
        print(f'ARCHIVE.DELETE_FOLDER: DATE ARCHIVE {archive_date}, DELETE {delete_date}')
        if not archive_date:
            print('ARCHIVE.DELETE_FOLDER: No Archive Date Provided')
            return None
        if not re.match(r'^20\d{2}\d{2}\d{2}$', archive_date):
            print('ARCHIVE.DELETE_FOLDER: Invalid Archive Date ' + archive_date)
            return None
        if delete_date and not re.match(r'^20\d{2}\d{2}\d{2}$', delete_date):
            print('ARCHIVE.DELETE_FOLDER: Invalid Delete Date ' + delete_date)
            return None
        try:
            self._open()
            rslt = self.drive.find_folder(archive_date, self.conf['DRIVE_DELETED_FILES'])
            if not rslt:
                print('ARCHIVE.DELETE_FOLDER: No Folder Found ' + archive_date)
                return None
            folder_id = rslt['id']
            rslt = self.drive.delete_folder(folder_id)
            print(f'ARCHIVE.DELETE_FOLDER: Folder {archive_date} Deleted on {delete_date}')
            rslt = self.db.complete_file_delete(archive_date, delete_date)
            print('ARCHIVE.DELETE_FOLDER: Completed Set 6 to ArchivedRequests.Status')
            print(f'{rslt} Requests Processed')
            self._close()
            return True
        except Exception as err:
            print(err)
            return err

    def restore_files_by_archive_date(self, archive_date):
        """
        Move files in delete folder specified by the given date to the original location

        INPUT
            archive_date (String): the date that the files are archived; yyyymmdd
        """
        if not re.match(r'^20\d{2}\d{2}\d{2}$', archive_date):
            print('RESTORE_FILES_BY_DELETE_FOLDER: Invalid Date ' + archive_date)
            return None
        self._open()
        files = self.db.get_file_info_by_archive_date(archive_date)
        rslt = self.restore_files(files)

        delete_rslt = self.drive.find_folder(archive_date, self.conf['DRIVE_DELETED_FILES'])
        if not delete_rslt:
            print('RESTORE_FILES_BY_DELETE_FOLDER: No Folder Found ' + archive_date)
            return None
        folder_id = delete_rslt['id']
        rslt = self.drive.delete_folder(folder_id)
        print('RESTORE_FILES_BY_DELETE_FOLDER: Folder Deleted ' + archive_date)

        self._close()
        return rslt

    def restore_files_by_request_id(self, request_id):
        """
        Move files in delete folder of specified request to the original location
        """
        if not request_id:
            print('RESTORE_FILES_BY_REQUEST_ID: No RequestId Provided')
            return None
        #try:
        self._open()
        files = self.db.get_file_info_by_request_id(request_id)
        rslt = self.restore_files(files)
        self._close()
        return rslt

    def restore_files(self, files):
        """
        Move files in delete folder of specified request to the original location

        INPUT
            files: [(RequestId, ArchiveFileId, OriginalId, ArchiveFolder, srcFolder,
                   FileId, OriginalPath, OriginalType, ArchiveDate, MoveDate)]
        """
        if not files:
            print('RESTORE_REQUEST_FILES: No Files Provided')
            return None
        index = 0
        size = 50
        cnt = 0
        data = DB.conv_data_for_restore(files)
        limit = len(files)
        print(f'ARCHIVE.RESTORE_REQUEST_FILES: PROCESSING ({limit})')

        try:
            while index < limit:
                batch_rslt = self.drive.batch_move(data['all_files'][index:index+size])
                print(batch_rslt)
                if not batch_rslt:
                    print('ARCHIVE.RESTORE_REQUEST_FILES: BATCH_MOVE Failed')
                    return None
                rslt = len(batch_rslt)
                cnt += rslt
                index += size
                print(f'ARCHIVE.RESTORE_REQUEST_FILES: CUR {rslt} / TOTAL {cnt} Files Processed')
                time.sleep(1)
            rslt = self.db.undone_file_archive(data['request_ids'])
            print(f'{rslt} ArcvhiedRequests and ArchivedFiles Restored')
            rslt = self.db.undone_document_file_path(data['document_files'])
            print(f'{rslt} Documents Restored')
            rslt = self.db.undone_traveler_file_path(data['traveler_files'])
            print(f'{rslt} Travelers Restored')
            rslt = self.db.undone_request_file_path(data['request_files'])
            print(f'{rslt} Requests Restored')
            return True
        except Exception as err:
            print(err)
            return err

    def check_db_status(self, target_date):
        """
        Checks if the DB archive status at the given date is valid

        INPUT
            target_date (String): assumed to be the current date in YYYYMMDD
        """
        if not target_date:
            target_date = date.today().strftime('%Y%m%d')
        elif not re.match(r'^20\d{2}\d{2}\d{2}$', target_date):
            print('CHECK_DB_STATUS: Invalid Date ' + target_date)
            return None
        target_date = re.sub(r'^(20\d{2})(\d{2})(\d{2})$', r'\1-\2-\3', target_date)
        try:
            self._open()
            self._close()
            return True
        except Exception as err:
            print(err)
            return err
