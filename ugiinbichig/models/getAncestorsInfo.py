from django.db import connection

def get_ancestors_info(human_id, max_level):
    with connection.cursor() as cursor:
        cursor.execute("SELECT getAncestorsInfo(%s, %s)", [human_id, max_level])
        return cursor.fetchall()
