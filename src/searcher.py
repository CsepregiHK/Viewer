"""
 Copyright (c) 2025 free

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """

import src.date_checker as date_checker
import streamlit as st
from sqlalchemy import text

class searcher:
    def __init__(self, database):
        """
        Docstring for __init__  
        :param self: class self reference.
        :param database: path to the sqlite database.
        """
        self.data_source = database
        self.data_loaded = False
        self.query = (''' SELECT chrono.id, chrono.date,  chrono.title, chrono.text, -1, -1'''
        ''' FROM chrono WHERE chrono.date =:main_date'''
        ''' UNION ALL'''
        ''' SELECT chrono.id, chrono.date, chrono.title, chrono.text, spos, epos'''
        ''' FROM chrono'''
        ''' LEFT JOIN internal ON internal.cid = chrono.id WHERE internal.cid IS NOT NULL AND internal.date =:i_date ''')
        self.query_next = "SELECT date, title, text, -1, -1 FROM chrono WHERE date >:next_date ORDER BY date"
   
    def load_data(self):
        """This does nothing but loading the earliest and the latest date in the databases.
        """
        self.conn = st.connection('raxx_sl3', type='sql')
        sql = text("SELECT MIN(date) FROM chrono")
        result = self.conn.session.execute(sql)
        rows = result.fetchone()
        if rows:
            self.FDATE = rows[0]
        sql = text("SELECT MAX(date) FROM chrono")
        result = self.conn.session.execute(sql)
        rows = result.fetchone()
        if rows:
            self.LDATE = rows[0]

    def run_search(self, input_date):
        if(not self.data_loaded):
            self.load_data()
        date_to_search = self.get_valid_date(input_date)
        sql = text(self.query)
        result = self.conn.session.execute(sql, {"main_date": date_to_search, "i_date": date_to_search})
        rows = result.fetchmany(5)
        if rows:
            for row in rows:
                yield(row[1], row[2], row[3], row[4], row[5])    

        else:
            sql = text(self.query_next)
            result = self.conn.session.execute(sql, {"next_date": date_to_search})
            row = result.first()
            if row:
                yield(row[0], row[1], row[2], -1, -1)    
    

    def get_valid_date(self, input):
        if(date_checker.date_checker(input)):
            date2search = input[:10]
            if(date2search < self.FDATE):
                date2search =self.FDATE
            if(date2search > self.LDATE):
                date2search = self.LDATE
        else:
            date2search = self.FDATE
        return date2search