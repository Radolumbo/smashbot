import psycopg2
import psycopg2.extras
import psycopg2.pool

from enum import Enum
import time
import sb_db.errors as dberr

class DBAccessor:
    StatusCode = Enum("StatusCode", "SUCCESS DUPLICATE")

    def __init__(self, host, name, port, user, password):
        # Disabling sql access for now
        raise dberr.DatabaseError("SQL access is disabled")
        # self.pool = psycopg2.pool.SimpleConnectionPool(1, 10, database=name, user=user, password=password, host=host, port=port)

    def execute(self, query, params, is_update=False):
        # Try once, if DB fails, will sleep + try again
        try:
            return self.__execute_impl(query, params, is_update)
        except dberr.UniqueViolation:
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
            conn = self.pool.getconn()
            conn.set_client_encoding('UTF8')
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query, params)
            if is_update:
                conn.commit()
            else:
                return cursor.fetchall()
        except psycopg2.errors.UniqueViolation as e:
            if is_update:
                conn.rollback()
            raise dberr.UniqueViolation
        except psycopg2.DatabaseError as e:
            raise dberr.DatabaseError from e
        except Exception as e:
            if is_update:
                conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            # returns connection back to pool
            if conn is not None:
                self.pool.putconn(conn)