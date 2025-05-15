from flask import Flask,render_template,session,request,redirect,flash,url_for,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.secret_key = "ammoeka"
adminpass = "Ammoeka"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

#admins department will be 0
# admin userlevel is 0 
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
    user_level = db.Column(db.Integer, nullable = False)##Lectures are 1 and admin is 0 
    department_id = db.Column(db.Integer,db.ForeignKey('department.id'),nullable = False)

class Department(db.Model):
   id=db.Column(db.Integer,primary_key=True)
   department_name=db.Column(db.String(50),nullable=False,unique = True)
   users = db.relationship('User',backref='department',lazy=True)
   years = db.relationship('Year',backref='dm_year',lazy=True )

class Year(db.Model):
   id = db.Column(db.Integer,primary_key=True)
   year = db.Column(db.Integer,nullable=False,unique=True)
   department_id = db.Column(db.Integer,db.ForeignKey('department.id'),nullable = False)

   __table_args__ = (db.UniqueConstraint('department_id', 'year', name='_department_year_uc'),)

class Hall(db.Model):
   id = db.Column(db.Integer,primary_key = True)
   hallName = db.Column(db.String(5),nullable = False,unique=True)
   hallType = db.Column(db.String(10),nullable=False)
   status = db.Column(db.Boolean,default=False,nullable=False)

class Booking(db.Model):
   booking_session = db.Column(db.String(100),primary_key=True)
   user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
   hall_id = db.Column(db.Integer,db.ForeignKey('hall.id'),nullable=False)
   year_id = db.Column(db.Integer,db.ForeignKey('year.id'),nullable=False)
   start_time = db.Column(db.DateTime,nullable=False)
   end_time = db.Column(db.DateTime,nullable=False)
     

@app.route('/',methods = ['GET', 'POST'])
def root():
   if 'user' in session and session.get('user_level') == 1:
      return render_template('index.html',lec_user=True)
   return render_template("index.html")

@app.route('/login',methods = ['GET', 'POST'])
def login():
   if 'user' in session and session.get('user_level') == 0:
      return redirect(url_for('admin'))
   if 'user' in session and session.get('user_level') == 1:
      return redirect(url_for('root'))   
   if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    qurrey  = User.query.filter_by(username = username).one_or_none()

    if qurrey:
        if password == qurrey.password:
            if qurrey.user_level == 0:
                session['user'] = qurrey.username
                session['user_level'] = qurrey.user_level
                session['department'] = qurrey.department.department_name
                return redirect(url_for("admin"))
            if qurrey.user_level == 1:
                session['user'] = qurrey.username
                session ['user_level'] = qurrey.user_level
                session['department'] = qurrey.department.department_name
                return redirect(url_for('root'))
        flash("wrong password")
        return redirect(url_for('login'))
    flash("worng username")
    return redirect(url_for('login'))
   return render_template("login.html")

@app.route('/admin',methods = ['GET', 'POST'])
def admin():
   if 'user' not in session and session.get('user') is None:
      return redirect(url_for('login'))
   elif session.get('user_level',1) != 0:
      abort(401)
   else:
      users = User.query.all()
      departments = Department.query.all()
      halls = Hall.query.all()
      
      if request.method == "POST":
         value = request.form.get('action')
         if value == "add_department":
            department_name = request.form["name"]
            if Department.query.filter_by(department_name = department_name).one_or_none() is None:
               add = Department(department_name = department_name)
               db.session.add(add)
               db.session.commit()
               flash("The department has been added",category="message")
               return redirect(url_for('admin'))
            flash("The Department is allrady exsist!",category="warning")
            return redirect(url_for("admin"))
         if value == "delete_department":
            delValue= db.session.get(Department,int(request.form.get("department")))
            db.session.delete(delValue)
            db.session.commit()
            flash("Departmet deleted sucsessfully!",category="message")
            return redirect(url_for('admin'))

         if value == "add_hall":
            hallName = request.form["name"]
            hallType = request.form.get('hallType')
            if Hall.query.filter_by(hallName = hallName).one_or_none() is None:
               add = Hall(hallName = hallName,hallType=hallType,status = 0)
               db.session.add(add)
               db.session.commit()
               return redirect(url_for('admin'))
            flash("Hall alrady exsist")
            return redirect(url_for('admin'))         
         if value == "delete_hall":
            deleteHall = request.form.get("faculty")
      return render_template("admin.html",users=users,departments=departments[1:],halls=halls)
   return redirect(url_for('root'))
   
   
@app.route('/logout')
def logout():
   session.pop('user',None)
   session.pop('user_level',None)
   session.pop('department',None)
   return redirect(url_for("root"))  


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
         with app.app_context():
            db.drop_all(bind_key=None)
            db.create_all()
         username = request.form['username']
         password = request.form['password']

         add_department = Department(department_name = 'admin')
         db.session.add(add_department)  
         db.session.commit()
         adduser = User(name = 'admin',username = username,
                        password = password,user_level = 0,
                        department_id = add_department.id)
         db.session.add(adduser)
         db.session.commit()


 

        return redirect(url_for("login"))
    return render_template("install.html")


         

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        

    app.run(debug=True)
