"""
MySql Client Base Class
"""
#pylint: disable=invalid-name
import MySQLdb

class MysqlBaseClient:
    """
    Handles basic DB access
    """
    def __init__(self, conf):
        """
        Constructor
        """
        self.conf = conf
        self.db = None
        self.errors = []

    def connect(self):
        """
        Opens the connection to the database
        """
        if self.db:
            return True
        try:
            socket_path = self.conf.get('DOCRMV_DB_SOCKET')
            if socket_path:
                self.db = MySQLdb.connect(
                    unix_socket=socket_path,
                    user=self.conf['DOCRMV_DB_USER'],
                    passwd=self.conf['DOCRMV_DB_PASS'],
                    db=self.conf['DOCRMV_DB_DATABASE'])
            else:
                ssl_set = {
                    'key': self.conf['DOCRMV_DB_SSL_KEY'],
                    'cert': self.conf['DOCRMV_DB_SSL_CERT'],
                    'ca': self.conf['DOCRMV_DB_SSL_CA']}
                self.db = MySQLdb.connect(
                    host=self.conf['DOCRMV_DB_HOST'],
                    port=int(self.conf['DOCRMV_DB_PORT']),
                    user=self.conf['DOCRMV_DB_USER'],
                    passwd=self.conf['DOCRMV_DB_PASS'],
                    db=self.conf['DOCRMV_DB_DATABASE'],
                    ssl=ssl_set)
        except Exception as err:
            print(err)
            self.errors.append(err)
            return False
        return True

    def close(self):
        """
        Closes the connection
        """
        if not self.db:
            return False
        try:
            self.db.close()
            self.db = None
            return True
        except Exception as e:
            self.errors.append(e)
            return False

    def query(self, sql):
        """
        Executes the given SELECT sql query
        """
        rslt = []
        try:
            self.connect()
            cur = self.db.cursor()
            cur.execute(sql)
            while True:
                rows = cur.fetchmany(1000)
                if not rows:
                    break
                rslt += rows
            cur.close()
        except Exception as e:
            print(e)
            self.errors.append(e)
            return None
        return rslt

    def fetch(self, sql, limit = 1000):
        """
        Executes the given SELECT sql query
        """
        rslt = []
        offset = 0
        try:
            self.connect()
            while True:
                suffix = f'LIMIT {limit}  OFFSET {offset}'
                self.db.query(sql + suffix)
                result = self.db.store_result()
                rows = result.fetch_row(maxrows=0)
                if not rows:
                    break
                rslt += rows
                offset += len(rows)
        except Exception as e:
            print(e)
            self.errors.append(e)
            return None
        return rslt

    def exec(self, sql):
        """
        Executes the given INSERT/UPDATE/DELETE sql statement
        """
        rslt = None
        try:
            self.connect()
            cur = self.db.cursor()
            rslt = cur.execute(sql)
            self.db.commit()
            cur.close()
        except Exception as e:
            self.db.rollback()
            print(e)
            self.errors.append(e)
            return None
        return rslt

    def exec_many(self, sql, values):
        """
        Execute given sql statement with multiple values
        """
        rslt = None
        try:
            self.connect()
            cur = self.db.cursor()
            rslt = cur.executemany(sql, values)
            self.db.commit()
            cur.close()
        except Exception as e:
            self.db.rollback()
            print(e)
            self.errors.append(e)
            return None
        return rslt

    def callproc(self, proc, args = None):
        """
        Calls the given stored procedure
        """
        if args is None:
            args = []
        rslt = None
        try:
            self.connect()
            cur = self.db.cursor()
            rslt = cur.callproc(proc, args)
            cur.close()
        except Exception as e:
            self.db.rollback()
            print(e)
            self.errors.append(e)
            return None
        return rslt

    def ping(self):
        """
        Checks whether the connection to the server is working.  If the connection
        has gone down and auto-reconnect is enabled an attempt to reconnect is made.
        If the connection is down and auto-reconnect is disabled, mysql_ping()
        returns an error.
        """
        rslt = None
        try:
            self.connect()
            rslt = self.db.ping()
        except Exception as e:
            self.db.rollback()
            print(e)
            self.errors.append(e)
            return None
        return rslt

    def show_errors(self):
        """
        Displays errors
        """
        for e in self.errors:
            print(e)

    def show_conf(self):
        """
        Displays configuration
        """
        print(self.conf)
