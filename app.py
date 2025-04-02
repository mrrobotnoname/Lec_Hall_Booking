from flask import Flask,render_template,session,request,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.secret_key = "ammoeka"
adminpass = "Ammoeka"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

#admins department will be 0 
#department will be represent in numbers
#it-1
#pm-2
#eng-3
# acount-4
 
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable = False)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(100), unique = True, nullable = False)
    department = db.Column(db.Integer, nullable = False)
    user_level = db.Column(db.Integer, nullable = False)

class Hall(db.Model):
   id = db.Column(db.Integer,primary_key = True)
   hallName = db.Column(db.String(5),nullable = False,unique=True)
   hallType = db.Column(db.String(10),nullable=False)
   status = db.Column(db.Boolean,nullable=False)#boked = True
   startTime = db.Column(db.DateTime)
   endTime = db.Column(db.DateTime)

     

@app.route('/',methods = ['GET', 'POST'])
def root():
    if request.method == "POST":
        if request.form['value'] == "admin" :
            return redirect(url_for('admin'))

        if request.form['value'] == "lecture":
           return redirect(url_for('lecture'))
    
        if request.form['value'] == "student":
           return redirect(url_for("student"))

    return render_template("index.html")

@app.route('/login',methods = ['GET', 'POST'])
def login():   
   if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    qurrey  = User.query.filter_by(username = username).one_or_none()

    if qurrey:
        if password == qurrey.password:
            if qurrey.user_level == 0:
                session['user'] = qurrey.username
                session['user_level'] = qurrey.user_level
                session['department'] = qurrey.department
                return redirect(url_for("admin"))
            if qurrey.user_level == 1:
                session['user'] = qurrey.username
                session ['user_level'] = qurrey.user_level
                session['department'] = qurrey.department
                return redirect(url_for('lecture'))
        flash("wrong password")
        return redirect(url_for('login'))
    flash("worng username")
    return redirect(url_for('login'))
   return render_template("login.html")

@app.route('/admin')
def admin():
   if 'user' not in session or session.get('user_level',0) != 0:
      return redirect(url_for('login'))
   return render_template("admin.html")

@app.route('/lecture_edit',methods = ['GET','POST'])
def lecture_edit():
   if request.method == 'POST':
      name = request.form['name']
      username = request.form['username']
      password = request.form['password']
      department = int(request.form.get('depatment'))
      qurry = User.query.filter_by(username=username).one_or_none() or User.query.filter_by(password=password).one_or_none()
      print(qurry)
      if qurry is not None:
         flash('username or password allredy exsist')
         return redirect(url_for('lecture_edit'))
      add = User(name= name,username= username,password= password,department= department,user_level=1)
      db.session.add(add)
      db.session.commit()
      flash('Lecture Added')

   return render_template('lec_add.html')
   
@app.route('/hall_edit',methods = ['GET','POST'])
def hall_edit():
   if request.method == 'POST':
      hallName = request.form['hname']
      hallType = request.form.get('htype')
      qurrey = Hall.query.filter_by(hallName=hallName).one_or_none()
      if qurrey is not None:
         flash("Hallname allredy exsist",category='message')
         return redirect(url_for('hall_edit'))
      add = Hall(hallName = hallName,hallType = hallType,status = False)
      db.session.add(add)
      db.session.commit()
      flash("Hall been added!",category="message")
      return redirect(url_for('hall_edit'))
   return render_template('hall_edit.html')  


@app.route('/lecture',methods=['GET','POST'])
def lecture():
   if 'user' not in session and session.get('user') is None:
      return redirect(url_for('login'))
   
   datas = Hall.query.filter_by(status = False).all()
   users = User.query.filter_by(username = session['user'])
   print(users)
   return render_template("lecture.html",datas=datas)

@app.route('/install',methods = ['GET', 'POST'])
def install():
    if request.method == "POST":
        if request.form["adminpass"] != 'Ammoeka':
            flash("Wrong admin password")
            return redirect(url_for("install"))
        else:
         username = request.form['username']
         password = request.form['password']

         add = User(name = 'admin',username = username,password = password, department = 0, user_level = 0)

         with app.app_context():
            db.drop_all(bind_key=None)
            db.create_all()
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("install.html")


         

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        

    app.run(debug=True)
