from flask import *
import sqlite3 # salite3

app = Flask(__name__)
#db
conn = sqlite3.connect("database.db")   # splite3 db 연결
print("Opened database successfully")
conn.execute("DROP TABLE IF EXISTS Board")  # Board 테이블이 기존에 있다면 삭제 (매번, 동일한 파일에서 실행하면, 내용이 겹쳐서 만듦)
conn.execute('CREATE TABLE IF NOT EXISTS Board (name TEXT, context TEXT)')  # Board 테이블이 기존에 없다면 생성
print ("Table created successfully")
name = [['Elice', 15], ['Dodo', 16], ['Checher', 17], ['Queen', 18]]

for i in range(len(name)):
    conn.execute(f"INSERT INTO Board(name,context) VALUES('{name[i][0]}', '{name[i][1]}')")  # Board DB에 데이터 삽입
conn.commit()   # 지금껏 작성한 SQL, DB에 반영 commit
conn.close()    # 작성 다한 DB는 닫아줘야함 close

#로그인
app.secret_key='super secret key'
app.config['SESSION_TYPE']='filesystem'
userinfo={'rawfish':'rjsghl'}

#메소드
@app.route('/')
def index():
    if session.get('logged_in'):
        return render_template('loggedin.html')
    return render_template('index.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        name=request.form['username']
        password=request.form['password']
        try:
            if(name in userinfo):
                session['logged_in']=True
                return render_template('loggedin.html')
            else:
                return '없는 비밀번호입니다'
        except:
            return '로그인이 불가합니다'
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        name=request.form['username']
        password=request.form['password']
        userinfo[name]=password
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route("/logout")
def logout():
    session['logged_in']=False
    return render_template('index.html')

#board
@app.route('/board')
def board():
    con=sqlite3.connect('database.db')
    cur=con.cursor()
    cur.execute("SELECT * FROM Board")
    rows = cur.fetchall()

    print("DB: ")
    for i in range(len(rows)):
        print(rows[i][0] + ':' + rows[i][1])
    return render_template('board1.html',rows=rows)
#search
@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        name = request.form["name"]
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM Board WHERE name='{name}'")
        rows = cur.fetchall()
        print("DB : ")
        for i in range(len(rows)):
            print(rows[i][0] + ':' + rows[i][1])
        return render_template("search.html", rows=rows)
    else:
        return render_template("search.html")

#add
# 게시물 생성 (Create)
@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            name = request.form['name']
            context = request.form['context']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO Board (name, context) VALUES ('{name}', '{context}')")
                con.commit()
        except:
            con.rollback()
        finally : 
            con.close()
            return redirect(url_for('board'))
    else:
        return render_template('add.html')

# 게시물 내용 갱신(Update)
@app.route("/update/<uid>", methods=["GET","POST"])
def update(uid):
    if request.method == "POST":
        name = request.form["name"]
        context = request.form["context"]
        
        # 내용 갱신하고
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()  # connection한 db에 접근하기 위해, cursor 객체 만들기
            cur.execute(f"UPDATE Board SET name='{name}', context='{context}' WHERE name='{uid}'")
            con.commit()
 
        return redirect(url_for("board"))   # 갱신되었는지, board함수 리다이렉트해서, / 페이지 렌더링
    else:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM Board WHERE name='{uid}'")
        row = cur.fetchall()
        return render_template("update.html",row=row)

@app.route("/delete/<uid>")
def delete(uid):
    # 들어온 uid 값이랑 name이랑 delete 연산하고 반영
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM Board WHERE name='{uid}'")
        con.commit()
 
    return redirect(url_for('board'))  # 삭제 반영하고, 반영됬는지, board함수 리다이렉트, / 페이지 렌더링

if __name__ == '__main__':
    app.run(debug=True)