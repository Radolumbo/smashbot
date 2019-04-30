from mysql.connector import errors as sqlerr
from mysql.connector import errorcode as sqlerrcode
from mysql.connector import pooling
from enum import Enum
import time
import sb_db.errors as dberr

class DBAccessor:
    StatusCode = Enum("StatusCode", "SUCCESS DUPLICATE")

    def __init__(self, host, name, user, password):
        self.pool = pooling.MySQLConnectionPool(pool_name = "smash_pool",
                                                    pool_size = pooling.CNX_POOL_MAXSIZE,
                                                    database = name,
                                                    host = host,
                                                    user = user,
                                                    passwd = password)

    def execute(self, query, params, is_update=False):
        # Try once, if DB fails, will sleep + try again
        try:
            return self.__execute_impl(query, params, is_update)
        except dberr.DuplicateKeyError:
            raise
        except dberr.Error:
            time.sleep(.250)
            return self.__execute_impl(query, params, is_update)

    def execute_update(self, query, params):
        return self.execute(query, params, True)
        
    def __execute_impl(self, query, params, is_update):
        conn = None
        cursor = None
        try: 
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            if is_update:
                conn.commit()
            else:
                return cursor.fetchall()
        except sqlerr.PoolError as e:
            raise dberr.PoolBusyError from e
        except sqlerr.IntegrityError as e:
            if is_update:
                conn.rollback()
            if(e.errno == sqlerrcode.ER_DUP_ENTRY):
                raise dberr.DuplicateKeyError from e
            else:
                raise dberr.Error("Executing {} failed for unknown reasons.".format(query)) from e
        except Exception as e:
            if is_update:
                conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            # returns connection back to pool
            if conn is not None:
                conn.close()