import mysql.connector as mysql
from enum import Enum
import time

class DBAccessor:
    StatusCode = Enum("StatusCode", "SUCCESS DUPLICATE")

    def __init__(self, host, name, user, password):
        self.pool = mysql.pooling.MySQLConnectionPool(pool_name = "smash_pool",
                                                pool_size = pooling.CNX_POOL_MAXSIZE,
                                                database = name,
                                                host = host,
                                                user = user,
                                                passwd = password)

    # Delete once confirming pool will open a new connection if one times out
    #def connect_to_db(self):
    #    self.connection = mysql.connector.connect(
    #        host=self.host,
    #        user=self.user,
    #        passwd=self.password,
    #        database=self.name
    #    )
    #    cursor = self.connection.cursor()
    #   # Timeout = 2 days
    #    cursor.execute("SET SESSION wait_timeout = 172800")
    #    # not sure if necessary but
    #    self.connection.commit()

    def execute(self, query, params, is_update):
        # Try once, if DB fails, will sleep + try again
        try:
            return self.__execute_impl(query, params, is_update)
        except mysql.errors.Error:
            time.sleep(.200):
            return self.__execute_impl(query, params, is_update)

        
    def __execute_impl(self, query, params, is_update):
        try: 
            conn = pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            if is_update:
                conn.commit()
            else:
                return cursor.fetchall()
        except mysql.errors.IntegrityError as e:
            if is_update:
                conn.rollback()
            if(e.errno == mysql.errorcode.ER_DUP_ENTRY):
                return self.StatusCode.DUPLICATE
            else:
                raise
        except Exception as e:
            if is_update:
                conn.rollback()
            raise
        finally:
            cursor.close()
            # returns connection back to pool
            conn.close()
        
        return self.StatusCode.SUCCESS


    def is_registered(db, discord_id):
        cursor = db.cursor()
        query = '''
            SELECT 
                COUNT(1) 
            FROM 
                player 
            WHERE 
                discord_id = %(discord_id)s'''
        cursor.execute(query, {"discord_id": discord_id})
        return (cursor.fetchone()[0] > 0)

    def get_fighter_names(db):
        cursor = db.cursor()
        query = '''
            SELECT 
                name
            FROM 
                fighter'''
        cursor.execute(query)
        data = cursor.fetchall()
        fighter_names = [data[i][0] for i in range(0,len(data))]
        
        return fighter_names