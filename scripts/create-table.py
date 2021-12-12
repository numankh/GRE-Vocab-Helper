import psycopg2
from decouple import config

RDS_AWS_INSTANCE_ENDPOINT = config('RDS_AWS_INSTANCE_ENDPOINT')
PORT = config('PORT')
USERNAME = config('USERNAME')
PASSWORD = config('PASSWORD')
DATABASE_NAME = config('DATABASE_NAME')

connection = psycopg2.connect(
    host = RDS_AWS_INSTANCE_ENDPOINT,
    port = PORT,
    user = USERNAME,
    password = PASSWORD,
    database= DATABASE_NAME
)
cursor=connection.cursor()

#creating table vocab
cursor.execute("""CREATE TABLE vocab(
id SERIAL PRIMARY KEY,
word text)""")

connection.commit()