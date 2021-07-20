"""
Test Suite Runner
"""
#pylint: disable=invalid-name
import re
from datetime import datetime
from datetime import timedelta
from src.archive import Archive

#class ExtendedArchive(Archive):
#    """
#    Archive Manager class extended for test suite
#    """
#    def run_stored_procs(self, retention1, retention2, current_date=None):
#        """
#        Runs the following stored procedure:
#            CreateArchiveRequests
#            CreateArchiveRequestsWithInvalidDate
#            CreateArchiveFiles
#        
#        INPUT
#
#            retention1: retention period for regular requests until archive
#            retention2: retention period for irregular requests until archive
#            current_date: YYYYMMDD
#        """
#        if not current_date:
#            current_date = 'NULL'
#        elif re.match(r'^20\d{2}\d{2}\d{2}$', current_date):
#            current_date = re.sub(r'^(20\d{2})(\d{2})(\d{2})$', r'\1-\2-\3', current_date)
#        else:
#            print('RunSuiteRunner#run_suite: Invalid Date ' + current_date)
#            return
#        self.db.connect()
#        print(f'CALL CreateArchiveRequests({retention1}, {current_date})')
#        rslt = self.db.exec(f"CALL CreateArchiveRequests({retention1}, '{current_date}')")
#        print('CreateArchiveRequests Called')
#        print(f'{rslt} ArchivedRequests Created')
#        print(f'CALL CreateArchiveRequestsWithInvalidDate({retention2}, {current_date})')
#        rslt = self.db.exec(f"CALL CreateArchiveRequestsWithInvalidDate({retention2}, '{current_date}')")
#        print('CreateArchiveRequestsWithInvalidDate Called')
#        print(f'{rslt} ArchivedRequests With Invalid Date Created')
#        rslt = self.db.exec('CALL CreateArchiveFiles()')
#        print(f'{rslt} ArchivedFiles Created')
#        self.db.close()

class TestSuiteRunner:
    """
    Archive Manager
    """
    def __init__(self, envpath='.env', retention1=60, retention2=240, retention3=30):
        """
        Constructor

        envpath: path to file containing environment variables
        retention_period1: days to move files of regular requests
        retention_period2: days to move files of irregular requests
        retention_period3: days to move files of regular requests
        """
        #self.archive = ExtendedArchive(envpath)
        self.archive = Archive(envpath)
        self.retention_period1 = retention1
        self.retention_period2 = retention2
        self.retention_period3 = retention3
        self.LIMIT = 200

    def run_suite(self, current_date):
        """
        Runs Test Suite with current date

        INPUT
            current_date: YYYYMMDD
        """
        if not current_date:
            print('RunSuiteRunner#run_suite: No Current Date Provided')
            return
        if not re.match(r'^20\d{2}\d{2}\d{2}$', current_date):
            print('RunSuiteRunner#run_suite: Invalid Date ' + current_date)
            return
        self.archive.prepare_for_archive(self.retention_period1, self.retention_period2, current_date)
        cnt = self.archive.populate_file_info(self.LIMIT)
        print(f'POPULATE_FILE_INFO: {cnt} ArchivedFiles Populated')
        self.archive.set_deleted_file_to_requests()
        print('SetDeletedFileImage Completed')
        rslt = self.archive.set_archive_flag_to_requests()
        print(f'{int(rslt/2)} Requests Archived')
        print(f'{int(rslt/2)} ArchivedRequests Updated')
        self.archive.move_files_to_archive_dir(current_date)
        self.archive.delete_folder_by_current_date(current_date, self.retention_period3)

    def run(self, start_date, days):
        """
        Runs Test suite days time from start_date

        INPUT
            start_date: date to start the test (YYYYMMDD)
            days:       the number of days to run test 
        """
        if not start_date:
            print('RunSuiteRunner#run: No Star Date Provided')
            return
        if not re.match(r'^20\d{2}\d{2}\d{2}$', start_date):
            print('RunSuiteRunner#run: Invalid Date ' + start_date)
            return
        start_date = datetime.strptime(start_date, '%Y%m%d')
        for offset in range(days):
            current = (start_date + timedelta(offset)).strftime('%Y%m%d')
            print(f'====< {current} >==========================================')
            self.run_suite(current)
