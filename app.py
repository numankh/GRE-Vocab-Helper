from flask import Flask, request, jsonify
import os
import time
from scripts.dbconnect import connect_to_db
import pandas as pd

"""
Basic app setup
"""
app = Flask(__name__)
cursor, connection = connect_to_db()

"""
Flask test routes
"""
@app.route('/')
def hello():
    return "Hello World!"

@app.route('/name/<name>')
def hello_name(name):
    return {'name': "numan"}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/getTableSchema')
def get_table_schema():
    sql = """
    SELECT "table_name","column_name", "data_type", "table_schema"
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE "table_schema" = 'public'
    ORDER BY table_name  
    """
    df = pd.read_sql(sql, con=connection)
    return jsonify(df.to_string())

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/word', methods=['POST', 'GET'])
def db_word():
    # if not request.json or not 'word' in request.json:
    #     abort(400)

    if request.method == 'POST':
        print("word:POST")
        connection = None
        try:
            sql = """INSERT INTO vocab(word) VALUES(%s) RETURNING id;"""
            request_word = request.args.get("word")
            print(f"WORD: <{request_word}>")

            cursor, connection = connect_to_db()
            cursor.execute(sql, (request_word,))
            id = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
            return f"Successfully added <{request_word}> with id:<{id}>into the vocab table"
        except Exception as error:
            return f"Error: <{error}>"
        finally:
            if connection is not None:
                connection.close()
    elif request.method == 'GET':
        print("word:GET")
        """ query data from the vendors table """
        connection = None
        try:
            cursor, connection = connect_to_db()
            cursor.execute("SELECT word FROM vocab ORDER BY word")
            print("The number of parts: ", cursor.rowcount)
            row = cursor.fetchone()

            while row is not None:
                print(row)
                row = cursor.fetchone()

            cursor.close()
            return f"Successfully fetched words"
        except Exception as error:
            return f"Error: <{error}>"
        finally:
            if connection is not None:
                connection.close()
        

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)