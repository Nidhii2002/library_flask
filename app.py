from flask import Flask,render_template, request ,redirect, url_for

from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        pwd = request.form['pass']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,pwd))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/addBooks')
def addBooks():
    return render_template('addBooks.html')

@app.route('/addBook', methods = ['POST'])
def addBook():
    call = request.form['call']
    name = request.form['name']
    author = request.form['author']
    publisher = request.form['publisher']
    quant = request.form['quant']
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO add_books VALUES (%s, %s, %s,%s,%s, curdate())''',(call,name,author,publisher,quant))
    mysql.connection.commit()
    return "Book Added!"

@app.route('/viewBooks')
def viewBooks():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM add_books''')
    books = cursor.fetchall()
    return render_template('viewBooks.html', books=books)

@app.route('/issueBooks')
def issueBooks():
    return render_template('issueBooks.html')

@app.route('/issueBook', methods= ['POST'])
def issueBook():
    call = request.form['call']
    s_id = request.form['id']
    name = request.form['name']
    contact = request.form['contact']
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO issue_books (`call_no`, `id`, `name`, `contact`, `issue_date`) VALUES (%s, %s, %s,%s, curdate())''',(call,s_id,name,contact))
    mysql.connection.commit()
    return "Issue Added!"

@app.route('/viewIBooks')
def viewIBooks():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM issue_books''')
    ibooks = cursor.fetchall()
    return render_template('viewIBooks.html', ibooks = ibooks)

@app.route('/returnBook')
def returnBook():
    return render_template('returnBook.html')

@app.route('/bookReturn', methods=['POST'])
def bookReturn():
    call = request.form['call']
    s_id = request.form['id']
    cursor = mysql.connection.cursor()
    cursor.execute(''' DELETE FROM issue_books WHERE `call_no` = %s and `id` = %s''',(call,s_id))
    mysql.connection.commit()
    return "Book Returned"

@app.route('/logout')
def logout():
    return render_template('index.html')

app.run(host='localhost', port=5000, debug=True)