import psycopg2
from decouple import config
import pandas as pd
import dbconnect

cursor, connection = dbconnect.connect_to_db()
sql = """
SELECT "table_name","column_name", "data_type", "table_schema"
FROM INFORMATION_SCHEMA.COLUMNS
WHERE "table_schema" = 'public'
ORDER BY table_name  
"""
df = pd.read_sql(sql, con=connection)
print(df.to_string())