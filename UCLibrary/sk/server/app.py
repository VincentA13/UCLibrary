from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import mysql.connector


app = Flask(__name__)
CORS(app, resources={r"/book_data": {"origins": "*"}})

db_connection = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'Wolves081314',
    database= 'uclibrary'
)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT')
    return response

@app.route('/book_data/', methods=['GET'])
def get_book_data():
    cursor = db_connection.cursor(dictionary=True)  # Use a dictionary cursor for easier data handling
    try:
        query =  query = 'SELECT BookID, BookName, CASE WHEN BookStatus = "B" THEN "Borrowed" ELSE "Available" END AS BookStatus FROM book_data'
        cursor.execute(query)
        books = cursor.fetchall()

        if books:
            return jsonify(books), 200
        else:
            return jsonify({'status': 'NOT_FOUND'}), 404
    except Exception as e:
        return jsonify({'status': str(e)}), 400
    finally:
        cursor.close()

@app.route('/book_return/', methods=['GET'])
def return_book():
    cursor = db_connection.cursor(dictionary=True)  # Use a dictionary cursor for easier data handling
    try:
        query = 'SELECT Borrow_ID, BName, DATE_FORMAT(RDate, "%d/%m/%Y") AS FormattedRDate FROM book_borrow WHERE Returned IS NULL'
        cursor.execute(query)
        books = cursor.fetchall()

        if books:
            return jsonify(books), 200
        else:
            return jsonify({'status': 'NOT_FOUND'}), 404
    except Exception as e:
        return jsonify({'status': str(e)}), 400
    finally:
        cursor.close()

@app.route('/trans_in_out/<string:trans_id>', methods=['PUT', 'GET'])
def get_trans(trans_id):
    cursor = db_connection.cursor()
    if request.method == 'GET':
        try:
            query = 'SELECT * FROM trans_in_out WHERE trans_item_id = %s'
            cursor.execute(query, (trans_id,))
            trans_in_out = cursor.fetchone()

            if trans_in_out\
                    :
                dict = {
                    'trans_id': trans_in_out[0],
                    'trans_date': trans_in_out[1],
                    'trans_item_id': trans_in_out[2],
                    'trans_type': trans_in_out[3],
                    'trans_qty': trans_in_out[4]
                }

                return jsonify(dict2), 200
            else:
                return jsonify({'status': 'NOT_FOUND'}), 404
        except Exception as e:
            return jsonify({'status': str(e)}), 400
        finally:
            cursor.close()
    elif request.method == "PUT":
            cursor.close()

@app.route('/borrow', methods=['POST'])
def add_borrow():
    if request.method == 'POST':
        data = request.get_json()
        cursor = db_connection.cursor()
        try:
            BBook_ID = data.get('BBook_ID')
            BName = data.get('BName')

            # INSERT query
            insert_query = 'INSERT INTO book_borrow (BBook_ID, BName) VALUES (%s, %s)'
            cursor.execute(insert_query, (BBook_ID, BName))

            # UPDATE query
            update_query = 'UPDATE book_data SET BookStatus = %s WHERE BookID = %s'
            cursor.execute(update_query, ('B', BBook_ID))

            db_connection.commit()

            return jsonify({'status': 'OK'}), 201
        except Exception as e:
            db_connection.rollback()
            return jsonify({'status': str(e)}), 400
        finally:
            cursor.close()

    return 'EMPTY'

@app.route('/return', methods=['PUT'])
def returnbook():
    if request.method == 'PUT':
        data = request.get_json()
        cursor = db_connection.cursor()
        try:
            Borrow_ID = data.get('Borrow_ID')


            update_borrow_query = 'UPDATE book_borrow SET Returned = CURDATE() WHERE Borrow_ID = %s'
            cursor.execute(update_borrow_query, (Borrow_ID,))

            update_book_data_query = 'UPDATE Book_Data SET BookStatus = "A" WHERE BookID = (SELECT BBook_ID FROM book_borrow WHERE Borrow_ID = %s)'
            cursor.execute(update_book_data_query, (Borrow_ID,))

            db_connection.commit()

            return jsonify({'status': 'OK'}), 201
        except Exception as e:
            db_connection.rollback()
            return jsonify({'status': str(e)}), 400
        finally:
            cursor.close()
    return 'EMPTY'

@app.route('/trans', methods=['POST', 'GET'])
def transaction():
    if request.method == 'POST':
        data = request.get_json()
        cursor = db_connection.cursor()
        try:
            trans_item_id = data.get('trans_item_id')
            trans_type = data.get('trans_type')
            trans_qty = data.get('trans_qty')

            query = 'INSERT INTO trans_in_out (trans_item_id, trans_type, trans_qty) VALUES ( %s, %s, %s)'
            cursor.execute(query, (trans_item_id, trans_type, trans_qty))
            db_connection.commit()

            return jsonify({'status': 'OK'}), 201
        except Exception as e:
            db_connection.rollback()
            return jsonify({'status': str(e)}), 400
        finally:
            cursor.close()

    elif request.method == 'GET':
        cursor = db_connection.cursor()
        try:
            query = 'SELECT trans_date, trans_type, trans_qty FROM trans_in_out WHERE trans_item_id = %s'
            cursor.execute(query)
            results = cursor.fetchall()

            list = []

            for trans_in_out in results:
                dict2 = {
                    'trans_date' : trans_date [0],
                    'trans_item_id': trans_in_out[1],
                    'trans_type': trans_in_out[2],
                    'trans_qty': trans_in_out[3]
                }
                list.append(dict2)

            return jsonify(list), 200
        except Exception as e:
            return jsonify({'status': str(e)}), 400
        finally:
            cursor.close()
    return 'EMPTY'

@app.route('/book_data/<string:BookID>', methods=['GET'])
def get_book(BookID):
    cursor = db_connection.cursor()
    if request.method == 'GET':
        try:
            query = 'SELECT * FROM book_data WHERE BookID = %s'
            cursor.execute(query, (BookID,))
            book = cursor.fetchone()

            if book:
                booklist = {
                    'BookID': book[0],
                    'BookName': book[1],
                    'BookStatus': book[2]
                }
                return jsonify(booklist), 200
            else:
                return jsonify({'status': 'NOT_FOUND'}), 404
        except Exception as e:
            return jsonify({'status': str(e)}), 400
        finally:
            cursor.close()

@app.route('/borrow/<string:Borrow_ID>', methods=['GET'])
def getreturn(Borrow_ID):
    cursor = db_connection.cursor()
    if request.method == 'GET':
        try:
            query = 'SELECT Borrow_ID, BName, DATE_FORMAT(RDate, "%Y-%m-%d") AS RDate FROM book_borrow WHERE Borrow_ID = %s'
            cursor.execute(query, (Borrow_ID,))
            book = cursor.fetchone()

            if book:
                booklist = {
                    'Borrow_ID': book[0],
                    'BName': book[1],
                    'RDate': book[2]
                }
                return jsonify(booklist), 200
            else:
                return jsonify({'status': 'NOT_FOUND'}), 404
        except Exception as e:
            return jsonify({'status': str(e)}), 400
        finally:
            cursor.close()

@app.route('/sales', methods=['GET'])
def sales():
    if request.method == 'GET':
        data = request.get_json()
        cursor = db_connection.cursor()
        try:
            trans_item_id = data.get('item_id')
            query = 'SELECT DATE_FORMAT(trans_date, "%Y-%m-%d") AS trans_date, trans_type, trans_qty FROM trans_in_out WHERE trans_item_id = %s'
            cursor.execute(query, (trans_item_id,))
            trans_in_out = cursor.fetchone()

            if trans_in_out\
                    :
                dict = {
                    'trans_id': trans_in_out[0],
                    'trans_date': trans_in_out[1],
                    'trans_item_id': trans_in_out[2],
                    'trans_type': trans_in_out[3],
                    'trans_qty': trans_in_out[4]
                }

                return jsonify(dict2), 200
            else:
                return jsonify({'status': 'NOT_FOUND'}), 404
        except Exception as e:
            return jsonify({'status': str(e)}), 400
        finally:
            cursor.close()
    elif request.method == "PUT":
            cursor.close()


if __name__ == '__main__':
    app.run(debug=True)

