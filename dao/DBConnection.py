from singleton.Singleton import Database


class Dao:
    def dbcall(filename,tablename):
        db = Database().connect()
        fileprocessed = False
        iscontentmatched = False
        sql = 'SELECT * FROM {} WHERE Filename = ? '.format(tablename)
        db.execute(sql, filename)
        result = db.fetchall()
        if (len(result) != 0):
            if (result[0][0] == filename):
                fileprocessed = True
                iscontentmatched = result[0][2]
        return fileprocessed, iscontentmatched

    def insertrecord(filename, text, isContentMatched, listToStr,tablename):
        db = Database().connect()
        query = "INSERT INTO {}(Filename,Content,isContentMatched,ContentDifference) " \
            "VALUES(?,?,?,?)".format(tablename)
        args = (filename, text, isContentMatched, listToStr)
        db.execute(query, args)
        db.commit()
        print("Record inserted successfully into table")
    def insertFailRecords(filename,apiname,exception):
        db = Database().connect()
        query = "INSERT INTO {} (Filename,ApiName,Error) " \
            "VALUES(?,?,?)".format('mscdissertation.dbo.FailedRecords')
        args = (filename, apiname, exception)
        db.execute(query, args)
        db.commit()
        print("Error inserted into table")

    def dbcallForFailedRecord(filename,ApiName, tablename):
        db = Database().connect()
        fileprocessed = False
        sql = 'SELECT * FROM {} WHERE Filename = ? and ApiName = ? '.format(tablename)
        db.execute(sql, filename,ApiName)
        result = db.fetchall()
        if (len(result) != 0):
            if (result[0][0] == filename):
                fileprocessed = True
        return fileprocessed


