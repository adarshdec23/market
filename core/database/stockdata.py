from config import database as dbconfig
import pymysql.cursors


class StockData:

    def __init__(self):
        self.con = pymysql.connect(
            host=dbconfig.host,
            user=dbconfig.username,
            password=dbconfig.password,
            db=dbconfig.database
        )
        self.fromDate = ""
        self.toDate = ""
        self.symbol = None
        self.selectFields = ""

    def sfrom(self, fdate):
        self.fromDate = fdate

    def sto(self, tdate):
        self.toDate = tdate

    def ssymbol(self, symbol):
        self.symbol = symbol

    def get_sdata(self, symbol=None):
        if symbol is None:
            symbol = self.symbol
        with self.con.cursor() as cursor:
            sql = '''
                    SELECT s.sopen, s.high, s.low, s.sclose, s.quantity, TRUNCATE(s.turnover*100000/s.quantity, 2) AS average
                    FROM stockData s, companies c
                    WHERE c.symbol = %s
                    AND DATE(sdate) BETWEEN %s AND %s
                    ORDER BY sdate
                    '''
            cursor.execute(sql, (symbol, self.fromDate, self.toDate))
            results = cursor.fetchall()
            return results
