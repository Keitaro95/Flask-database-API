"""データベースを利用する処理"""
import sqlite3
from flask import Flask
from flask import render_template
from flask import g
from flask import request

app = Flask(__name__)


@app.route('/') #'/'だったらこれ
def toppage():
    return 'top'


@app.route('/hello')
@app.route('/hello/<username>')
def hello_world(username=None):
    return render_template('index.html', username=username) #jinjaで再現される


"""データベースに接続する処理"""
def get_db():
    db = getattr(g, '_database', None) #gはグローバルな値を格納する場所,お決まり表現
    if db is None:
        db = g._database = sqlite3.connect('customers.db') #dbを作成
    return db

"""データベースへの接続を閉じる処理"""
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/customer', methods=['POST', 'PUT', 'DELETE'])
@app.route('/customer/<name>', methods=['GET'])
def customer(name=None):
    """データベースへの接続とテーブルの作成"""
    db = get_db()
    curs = db.cursor() 
    curs.execute(
        'CREATE TABLE IF NOT EXISTS persons( '
        'id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)'
    )
    db.commit()

    name = request.values.get('name', name)

    """GET時の処理"""
    if request.method == 'GET':
        curs.execute(f'SELECT * FROM persons WHERE name = "{name}"')
        person = curs.fetchone() #1つだけ取り出す
        if not person:
            return "No", 404
        user_id, name = person
        return f'{user_id}:{name}', 200

    """POST時の処理=挿入"""
    if request.method == 'POST':
        curs.execute(f'INSERT INTO persons(name) values("{name}")')
        db.commit()
        return f'created {name}', 201

    """PUT時の処理=更新"""
    if request.method == 'PUT':
        new_name = request.values['new_name']
        curs.execute(f'UPDATE persons set name = "{new_name}" '
                     f'WHERE name = "{name}"')
        db.commit()
        return f'updated {name}: {new_name}', 200

    """DELETE時の処理"""
    if request.method == 'DELETE':
        curs.execute(f'DELETE from persons WHERE name = "{name}"')
        db.commit()
        return f'deleted {name}', 200

    curs.close()


@app.route('/post', methods=['POST', 'PUT', 'DELETE'])
def show_post():
    return str(request.values['username']) #response_test.pyで返ってくる値

def main():
    app.debug = True
    app.run()

if __name__ == '__main__':
    main()