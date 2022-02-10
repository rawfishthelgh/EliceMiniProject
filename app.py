from flask import *
app = Flask(__name__)
boardlist=[]
app.secret_key='super secret key'
app.config['SESSION_TYPE']='filesystem'
userinfo={'rawfish':'rjsghl'}

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

# @app.route("/post",methods = ['GET','POST'])
# def post():
#     if request.method=="POST":
#         value = request.form["input"]
#         return f"{value} 님 환영합니다."
#     if request.method=="GET":
#         return render_template('post.html')

#read
@app.route('/board')
def board():
    return render_template('board.html',rows=boardlist)

#create
@app.route('/create',methods=['POST'])
def create():
    if request.method=="POST":
        name = request.form["name"]
        context = request.form["context"]
        boardlist.append([name,context])
        return redirect(url_for('board'))
    else:
        return render_template('board.html',rows=boardlist)

#update

@app.route('/update/<int:uid>', methods=["GET","POST"])
def update(uid):
    if request.method == "POST":
        index = uid - 1
        name = request.form["name"]
        context = request.form["context"]
        
        boardlist[index] = [name,context]   # 기존의 board내용에 덮어쓰기
        return redirect(url_for("board"))
    else:
        return render_template("update.html",index=uid,rows=boardlist)

#delete

@app.route('/delete/<int:uid>')
def delete(uid):
    index = uid - 1
    del boardlist[index]
    return redirect(url_for("board"))


# # login 주소에서 POST 방식의 요청을 받았을 때
# @app.route('/login',methods = ['POST'])  
# def loginrequest():  
#     id = request.form['id']  
#     password = request.form['pass'] 
 
#     if id=="rawfishthelgh" and password=="rjsghl": 
#         return "Welcome %s" % id  

if __name__ == '__main__':
    app.run(debug=True)