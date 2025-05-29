from flask import Flask,render_template,session,request,redirect,flash,url_for,abort
from flask_sqlalchemy import SQLAlchemy      
from datetime import datetime
from hashlib import sha256



app = Flask(__name__)
app.secret_key = "ammoeka"
adminpass = "Ammoeka"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


 
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable = False)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(100), unique = True, nullable = False)
    user_level = db.Column(db.Integer, nullable = False)##Lectures are 1 and admin is 0 

class Department(db.Model):
   id=db.Column(db.Integer,primary_key=True)
   department_name=db.Column(db.String(50),nullable=False,unique = True)
   year = db.relationship('Year',backref='department',lazy=True )

class Year(db.Model):
   id = db.Column(db.Integer,primary_key=True)
   department_id = db.Column(db.Integer,db.ForeignKey('department.id'),nullable = False)
   year = db.Column(db.Integer,nullable=False)


class Hall(db.Model):
   id = db.Column(db.Integer,primary_key = True)
   hallName = db.Column(db.String(5),nullable = False,unique=True)
   hallType = db.Column(db.String(10),nullable=False)
   bookings = db.relationship('Booking',backref='hall',lazy=True)

class Booking(db.Model):
   booking_session = db.Column(db.String(100),primary_key=True)
   user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
   hall_id = db.Column(db.Integer,db.ForeignKey('hall.id'),nullable=False)
   year_id = db.Column(db.Integer,db.ForeignKey('year.id'),nullable=False)
   department_id = db.Column(db.Integer,db.ForeignKey('department.id'),nullable=False)
   startDatetime = db.Column(db.DateTime,nullable=False)
   endDatetime = db.Column(db.DateTime,nullable=False)
     

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
                return redirect(url_for("admin"))
            if qurrey.user_level == 1:
                session['user'] = qurrey.username
                session ['user_level'] = qurrey.user_level
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
               flash("The department has been added",category="success")
               return redirect(url_for('admin'))
            flash("The Department is allrady exsist!",category="warning")
            return redirect(url_for("admin"))
         
         if value == "delete_department":
            department = request.form.get("department")
            delValue= db.session.get(Department,int(department))
            delYears = Year.query.filter_by(department_id = int(department)).all()
            delBookings = Booking.query.filter_by(department_id = int(department)).all()
            for delYear in delYears:
               db.session.delete(delYear)
            for delBooking in delBookings:
               db.session.delete(delBooking)

            db.session.delete(delValue)
            db.session.commit()
            flash("Departmet deleted sucsessfully!",category="success")
            return redirect(url_for('admin'))
         
         if value == "add_year":
            year = int(request.form['year'])
            department = int(request.form.get("department"))

            if Year.query.filter_by(department_id = department,year = year ).one_or_none() is None:
               add = Year(department_id = department,year=year)
               db.session.add(add)
               db.session.commit()
               flash("The year was added succsefully!",category="success")
               return redirect(url_for("admin"))
            flash("The year is allredy added!",category="warning")
            return redirect(url_for("admin"))

         if value == 'delete_year':
            department = request.form.get('faculty')  
            year = request.form.get('year')
            deletes = Year.query.filter_by(department_id = int(department),year = int(year)).all()
            for delete in deletes:   
               db.session.delete(delete)
            db.session.commit()
            flash("The year was deleted successfully!",category='success')
            return redirect(url_for("admin"))     
         if value == "add_hall":
            hallName = request.form["name"]
            hallType = request.form.get('hallType')
            if Hall.query.filter_by(hallName = hallName).one_or_none() is None:
               add = Hall(hallName = hallName,hallType=hallType,status = 0)
               db.session.add(add)
               db.session.commit()
               flash("Hall been Added!",category="success")
               return redirect(url_for('admin'))
            flash("Hall alrady exsist",category="warning")
            return redirect(url_for('admin'))         
         if value == "delete_hall":
            delValue = db.session.get(Hall,request.form.get("deleteHall"))
            db.session.delete(delValue)
            db.session.commit()
            flash("The hall was deleted succsessfully!",category="success")
            return redirect(url_for('admin'))
         if value == "add_lecture":
            name = request.form["name"]
            username = request.form["username"]
            password = request.form["password"]
            if User.query.filter_by(username=username).one_or_none() is None:
               add = User(name = name,username=username,password = password,user_level=1)
               db.session.add(add)
               db.session.commit()
               flash("Lecture added successfully!",category="success")
               return redirect(url_for('admin'))
            flash("The lecture is already exsist!",category="warning")
            return redirect(url_for('admin'))
      return render_template("admin.html",users=users,departments=departments,halls=halls)
   return redirect(url_for('root'))
   
@app.route('/api')
def api():
   if request.args.get('action') is None:
      return 'No action specified', 400
   if request.args['action'] == 'getYears':
      years = Year.query.filter_by(department_id = int(request.args.get('faculty'))).all()
      return [year.year for year in years]     

@app.route('/department',methods = ['GET', 'POST'])
def department():
   departments = Department.query.all()
   if request.method == "POST":
      if 'user' not in session and session.get('user') is None:
         return redirect(url_for('viwewBookings'))
      session['selected_department'] = request.form.get('faculty')
      session['selected_year'] = request.form.get('year')
      return redirect(url_for('selectDatetime'))
   return render_template('department.html',departments=departments)

@app.route('/selectdatetime',methods = ['GET', 'POST'])
def selectDatetime():
   if request.method == "POST":
      session['date'] =  request.form['selectedDate']
      session['start_time'] = request.form['startTime']
      session['end_time'] = request.form['endTime']
      return redirect(url_for('selectHall'))
   else:
      if 'user' not in session and session.get('user') is None:
         return redirect(url_for('viwewBookings'))
      elif 'selected_department' not in session or 'selected_year' not in session:
         flash("Please select a department and year first",category="warning")
         return redirect(url_for('department'))
      return render_template('date.html')


@app.route('/selecthall',methods = ['GET', 'POST'])
def selectHall():
   all_halls = Hall.query.all()
   if request.method == "POST":
      session['selected_hall'] = request.form.get('selectedHallId')
      return redirect(url_for('book'))
   else:
      if 'selected_department' not in session or 'selected_year' not in session:
         flash("Please select a department and year first",category="warning")
         return redirect(url_for('department'))
      elif 'date' not in session or 'start_time' not in session or 'end_time' not in session:
         flash("Please select a date and time first",category="warning")
         return redirect(url_for('selectDatetime'))
      else:
            date = datetime.strptime(session['date'], '%Y-%m-%d')
            start_time = datetime.strptime(session['start_time'], '%H:%M')
            end_time = datetime.strptime(session['end_time'], '%H:%M')
            start_datetime = datetime.combine(date, start_time.time())
            end_datetime = datetime.combine(date, end_time.time())

            
            overlap_booking = Booking.query.filter(Booking.startDatetime < end_datetime,
                                                   Booking.endDatetime >start_datetime
                                                   ).with_entities(Booking.hall_id).all()
            booked_ids = [b.hall_id for b in overlap_booking]
            halls = Hall.query.filter(~Hall.id.in_(booked_ids)).all()
            return render_template('hall.html',halls=halls)

   
@app.route('/book',methods = ['GET', 'POST'])
def book():
   if 'user' not in session or session.get('user') is None:
      return redirect(url_for('login'))
   if request.method == "POST":
      hall_id = int(session['selected_hall'])
      department_id = int(session['selected_department'])
      year_id = int(session['selected_year'])
      start_datetime = datetime.strptime(session['date'] + ' ' + session['start_time'], '%Y-%m-%d %H:%M')
      end_datetime = datetime.strptime(session['date'] + ' ' + session['end_time'], '%Y-%m-%d %H:%M')
      booking_session = sha256(f"{session['date']}_{session['selected_hall']}_{session['end_time']}_{session['selected_department']}".encode('utf-8')).hexdigest()
      
      new_booking = Booking(booking_session=booking_session,user_id=session.get('user'),hall_id=hall_id,
                            year_id=year_id,department_id=department_id,startDatetime=start_datetime,endDatetime=end_datetime)
      db.session.add(new_booking)
      db.session.commit()
      session.pop('selected_department', None)
      session.pop('selected_year', None)
      session.pop('date', None)
      session.pop('start_time', None)
      session.pop('end_time', None)
      session.pop('selected_hall', None)
      flash("Booking successful!",category="success")
      return redirect(url_for('root'))
   data=[['selected_department'] ,['selected_year'] ]
   return render_template('book.html',datas =data)




@app.route('/viewbookings')
def viwewBookings():

   department = session['selected_department'] 
   year = session['selected_year']
      

   return render_template('viewbookings.html')
@app.route('/logout')
def logout():
   session.pop('user',None)
   session.pop('user_level',None)
   session.pop('department',None)
   return redirect(url_for("root"))  


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

         db.session.commit()
         adduser = User(name = 'admin',username = username,
                        password = password,user_level = 0)
         db.session.add(adduser)
         db.session.commit()


 

        return redirect(url_for("login"))
    return render_template("install.html")


         

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        

    app.run(debug=True)
