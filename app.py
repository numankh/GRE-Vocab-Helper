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

@app.route('/login', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/bulkWords', methods = ['POST', 'GET'])
def bulk_words():
    if request.method == 'POST':
        print("bulkWords:POST")
        connection = None
        try:
            cursor, connection = connect_to_db()

            wordList = request.form.getlist('word')
            for word in wordList:
                print(f"WORD: <{word}>")
                cursor.execute("""INSERT into vocab(word) VALUES(%s) RETURNING id;""", (word,))
            
            connection.commit()
            cursor.close()
            return f"SUCCESS: added <{wordList}>"
        except Exception as error:
            return f"ERROR: <{error}>"
        finally:
            if connection is not None:
                connection.close()

    elif request.method == 'GET':
        print("word:GET")
        """ query data from the vendors table """
        connection = None
        try:
            cursor, connection = connect_to_db()
            cursor.execute("SELECT id, word FROM vocab ORDER BY word")
            print("The number of parts: ", cursor.rowcount)
            row = cursor.fetchone()

            res_ids = []
            res_words = []
            while row is not None:
                res_ids.append(row[0])
                res_words.append(row[1])
                row = cursor.fetchone()

            cursor.close()
            return f"SUCCESS: fetched all words: <{res_words}> with these ids: <{res_ids}>"
        except Exception as error:
            return f"Error: <{error}>"
        finally:
            if connection is not None:
                connection.close()

@app.route('/word', methods=['POST', 'GET'])
def add_word():
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
            return f"SUCCESS: added <{request_word}> with id:<{id}> into the vocab table"
        except Exception as error:
            return f"Error: <{error}>"
        finally:
            if connection is not None:
                connection.close()

@app.route('/word/<id>', methods=['GET'])
def get_word_by_id(id):
    if request.method == 'GET':
        print("word:GET")
        """ query data from the vendors table """
        connection = None
        try:
            cursor, connection = connect_to_db()
            cursor.execute("""SELECT word FROM vocab WHERE id = (%s)""", (id,))
            print("The number of parts: ", cursor.rowcount)
            row = cursor.fetchone()
            print(row)
            cursor.close()
            return f"SUCCESS: fetched <{row[0]}> with this id:<{id}>"
        except Exception as error:
            return f"Error: <{error}>"
        finally:
            if connection is not None:
                connection.close()
        

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)