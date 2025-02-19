class CategoryQueries:
    GET_ALL = "SELECT category_id, name FROM category"
    GET_NAME_BY_ID = "SELECT name FROM category WHERE category_id = %s"
    