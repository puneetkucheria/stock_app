import pymysql.cursors
import pymysql
import dbconfig


def runquery(query):
    connection = pymysql.connect(host=dbconfig.mysql['host'],
                                 user=dbconfig.mysql['user'],
                                 password=dbconfig.mysql['passwd'],
                                 db=dbconfig.mysql['db'],
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    finally:
        connection.close()

def runinsert(query):
    connection = pymysql.connect(host=dbconfig.mysql['host'],
                                 user=dbconfig.mysql['user'],
                                 password=dbconfig.mysql['passwd'],
                                 db=dbconfig.mysql['db'],
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
        #    result = cursor.fetchall()
        #return result
    finally:
        connection.commit()
        connection.close()

def data_status():
    connection = pymysql.connect(host=dbconfig.mysql['host'],
                                 user=dbconfig.mysql['user'],
                                 password=dbconfig.mysql['passwd'],
                                 db=dbconfig.mysql['db'],
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT distinct DATE_FORMAT(bhav_data.date, '%Y-%m-%d') as date FROM bhav_data left outer join bhav_data_status ON bhav_data.date = bhav_data_status.date where bhav_data_status.date is null" # WHERE `email`=%s"
            #sql = "SELECT 'ONE'"
            #cursor.execute(sql, ('webmaster',))
            cursor.execute(sql)
            result = cursor.fetchall()
                #print(result)
        return result

    finally:
        connection.close()



def get():
    # Connect to the database
    connection = pymysql.connect(host=dbconfig.mysql['host'],
                                 user=dbconfig.mysql['user'],
                                 password=dbconfig.mysql['passwd'],
                                 db=dbconfig.mysql['db'],
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        #with connection.cursor() as cursor:
            # Create a new record
        #    sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        #    cursor.execute(sql, ('webmaster', 'verysecret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        #connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT sc_code, sc_name, no_of_shrs, open FROM `bhav_data` WHERE last < 2.0 and no_of_shrs > 2000 order by no_of_shrs desc" # WHERE `email`=%s"
            #cursor.execute(sql, ('webmaster',))
            cursor.execute(sql)
            result = cursor.fetchall()
                #print(result)
        return result

    finally:
        connection.close()
