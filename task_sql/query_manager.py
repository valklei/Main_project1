from db_connection import DBConnection
from sql_queries import CategoryQueries

class QueryHandler(DBConnection):
    def __init__(self, dbconfig):
        super().__init__(dbconfig)

    def get_all_category(self):
        cursor = self.get_cursor()
        cursor.execute(CategoryQueries.GET_ALL)
        records = cursor.fetchall()
        return records

    def get_categoryname_by_id(self, category_id: int):
        cursor = self.get_cursor()
        cursor.execute(CategoryQueries.GET_NAME_BY_ID, (category_id,))
        records = cursor.fetchone()
        if records:
            return records.get('name')
        return None