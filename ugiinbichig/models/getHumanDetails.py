from django.db import connection

def get_human_details(human_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT getHumanDetails(%s)", [human_id])
        return cursor.fetchall()
