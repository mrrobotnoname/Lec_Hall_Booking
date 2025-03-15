from flask import Flask,render_template,session,request,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy



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
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(100), unique = True, nullable = False)
    department = db.Column(db.Integer, nullable = False)
    user_level = db.Column(db.Integer, nullable = False)

     

@app.route('/')
def root():
    if request.method == "POST":
        if request.form['value'] is "admin" :
            return redirect(url_for('admin'))

        if request.form['value'] is "lecture":
           return redirect(url_for('lecture'))
    
        if request.form['value'] is "student":
           return redirect(url_for("student"))

    return render_template("index.html")

app.route('/login')
def login():
   if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    qurrey  = User.query.filter_by(username = username, password = password).one_or_none()

    if qurrey:
       if password == qurrey.password:
          if qurrey.user_level:
       
       

   

@app.route('/admin')
def admin():
   if 

@app.route('/install')
def install():
    if request.method == "POST":
        if request.form["adminpass"] != 'Ammoeka':
         flash("Wrong admin password")
         return redirect(url_for("install"))
        else:
         username = request.form['username']
         password = request.form['password']

         add = User(username = username,password = password, depatment = 0, userlevel = 1)

         with app.app_context():
            db.drop_all(bind_key=None)
            db.create_all()
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("root"))
    return render_template("install.html")


         




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        

    app.run(debug=True)
