import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote

connection = sqlite3.connect('beer.db')
cursor = connection.cursor()


cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS beer_user (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT,
        UNIQUE(name)
    );
    '''
)

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS beer_review (
        id INTEGER PRIMARY KEY,
        user_id INT NOT NULL,
        shop_id INT NOT NULL,
        beer_name TEXT NOT NULL,
        review TEXT,
        datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES beer_user(id),
        FOREIGN KEY(shop_id) REFERENCES beer_shop(id)
    );
    '''
)
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS beer_shop (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    '''
)


class MyFancyServer(BaseHTTPRequestHandler):
    """Server for beer lovers"""

    def do_GET(self):
        print(self.path)
        request_data = self.path.split('/')
        result = '<h1>Hello world</h1>'

        if request_data[1] == 'register':
            cursor.execute(
                "INSERT INTO beer_user (name, password) VALUES (:name, :password)",
                {'name': request_data[2], 'password': request_data[3]},
            )
            connection.commit()
            result = f'<h1>User {request_data[2]} successfully created</h1>'
        elif request_data[1] == 'auth':
            cursor.execute(
                f"SELECT * FROM beer_user WHERE name='{unquote(request_data[2])}' AND password='{unquote(request_data[3])}'")
            user = cursor.fetchone()
            if user:
                result = (
                    f'<h1>User {user[1]} authorized successfully</h1></br></br>'
                    f'<b>SECRET INFORMATION</b>'
                )
            else:
                result = f'<h1>Access denied</h1>'
        elif request_data[1] == 'post_review':
            cursor.execute(
                "INSERT INTO beer_review (user_id, shop_id, beer_name, review) "
                "VALUES (:user_id, :shop_id, :beer_name, :review)",
                {
                    'user_id': request_data[2],
                    'shop_id': request_data[3],
                    'beer_name': request_data[4],
                    'review': request_data[5],
                },
            )
            connection.commit()
            result = f'<h1>Review {request_data[4]} created</h1>'
        elif request_data[1] == 'get':
            cursor.execute(
                'SELECT * FROM beer_user WHERE name=:name',
                {'name': request_data[2]}
            )
            user = cursor.fetchone()

            if user:
                cursor.execute(
                    f"SELECT * FROM beer_review WHERE user_id='{user[0]}'",
                )
                reviews = cursor.fetchall()
                rev_html = ''
                for review in reviews:
                    rev_html += f'{review[3]} - {review[4]}</br>'
                result = f'<h1>User {user[1]} exists with id {user[0]}</h1> {rev_html}'
            else:
                result = f'<h1>User not found</h1>'

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(result.encode())


def run(server_class=HTTPServer, handler_class=MyFancyServer):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
