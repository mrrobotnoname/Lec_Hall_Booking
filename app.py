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

class Year(db.Model):
   id = db.Column(db.Integer,primary_key=True)
   department_id = db.Column(db.Integer,db.ForeignKey('department.id'),nullable = False)
   year = db.Column(db.Integer,nullable=False)



class Hall(db.Model):
   id = db.Column(db.Integer,primary_key = True)
   hallName = db.Column(db.String(5),nullable = False,unique=True)
   hallType = db.Column(db.String(10),nullable=False)

class Booking(db.Model):
   booking_session = db.Column(db.String(100),primary_key=True)
   user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
   hall_id = db.Column(db.Integer,db.ForeignKey('hall.id'),nullable=False)
   year_id = db.Column(db.Integer,db.ForeignKey('year.id'),nullable=False)
   department_id = db.Column(db.Integer,db.ForeignKey('department.id'),nullable=False)
   startDatetime = db.Column(db.DateTime,nullable=False)
   endDatetime = db.Column(db.DateTime,nullable=False)
   pennding_delete = db.Column(db.Boolean,default=False)

   user = db.relationship('User', backref='bookings', lazy=True)
   hall = db.relationship('Hall', backref='bookings', lazy=True)
   year = db.relationship('Year', backref='bookings', lazy=True) 
   department = db.relationship('Department', backref='bookings', lazy=True)  

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
            delBookings = Booking.query.filter_by(year_id = int(year)).all()
            for delBooking in delBookings:
               db.session.delete(delBooking)
            for delete in deletes:   
               db.session.delete(delete)
            db.session.commit()
            flash("The year was deleted successfully!",category='success')
            return redirect(url_for("admin"))     
         if value == "add_hall":
            hallName = request.form["name"]
            hallType = request.form.get('hallType')
            if Hall.query.filter_by(hallName = hallName).one_or_none() is None:
               add = Hall(hallName = hallName,hallType=hallType)
               db.session.add(add)
               db.session.commit()
               flash("Hall been Added!",category="success")
               return redirect(url_for('admin'))
            flash("Hall alrady exsist",category="warning")
            return redirect(url_for('admin'))         
         if value == "delete_hall":
            delValue = db.session.get(Hall,request.form.get("deleteHall"))
            delBookings = Booking.query.filter_by(hall_id = int(request.form.get('deleteHall'))).all()
            for delBooking in delBookings:
               db.session.delete(delBooking)
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
         if value == "delete_lecture":
            delValue = db.session.get(User,request.form.get("deleteLecture"))
            delBookings = Booking.query.filter_by(user_id = int(request.form.get('deleteLecture'))).all()
            
            if delValue is not None:
               for delBooking in delBookings:
                  db.session.delete(delBooking)
               db.session.delete(delValue)
               db.session.commit()
               flash("The lecture was deleted successfully!",category="success")
               return redirect(url_for('admin'))
            flash("The lecture does not exist!",category="warning")
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
         return redirect(url_for('view_bookings'))
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
      getid = User.query.filter_by(username=session['user']).one_or_none()
      new_booking = Booking(booking_session=booking_session,user_id=getid.id,hall_id=hall_id,
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

#Keep in mind this was genarated by Ai that means you sucked and need to be better.
@app.route('/view-bookings',methods=['GET', 'POST'])
def view_bookings():
    
   if request.method == 'POST':
    pass




    current_datetime = datetime.now()
    if 'user' in session:
       user_id = User.query.filter_by(username=session.get('user')).one_or_none().id
    else:
         user_id = None
    if user_id:
        current_user = User.query.get(user_id)
        
        if not current_user:
            session.pop('user', None)
            return redirect(url_for('login'))
        
        user_bookings = Booking.query.options(
            db.joinedload(Booking.hall),
            db.joinedload(Booking.year),
            db.joinedload(Booking.department),
            db.joinedload(Booking.user)
        ).filter(Booking.user_id == user_id,Booking.endDatetime > current_datetime)\
         .order_by(Booking.startDatetime).all()
        other_bookings = Booking.query.options(
            db.joinedload(Booking.hall),
            db.joinedload(Booking.year),
            db.joinedload(Booking.department),
            db.joinedload(Booking.user)
        ).filter(Booking.user_id != user_id,Booking.endDatetime > current_datetime)\
         .order_by(Booking.startDatetime).all()
        
        return render_template('view_bookings.html', 
                             user_bookings=user_bookings,
                             other_bookings=other_bookings,
                             current_user=current_user,
                             is_logged_in=True)
    
    else:
        selected_department_id = session.get('selected_department')
        selected_year_id = session.get('selected_year')
        
        if selected_department_id and selected_year_id:
            filtered_bookings = Booking.query.options(
                db.joinedload(Booking.hall),
                db.joinedload(Booking.year),
                db.joinedload(Booking.department),
                db.joinedload(Booking.user)
            ).filter(
                Booking.department_id == selected_department_id,
                Booking.year_id == selected_year_id,Booking.endDatetime > current_datetime
            ).order_by(Booking.startDatetime).all()
            
            selected_department = Department.query.get(selected_department_id)
            selected_year = Year.query.get(selected_year_id)
            
            return render_template('view_bookings.html',
                                 filtered_bookings=filtered_bookings,
                                 selected_department=selected_department,
                                 selected_year=selected_year,
                                 is_logged_in=False)
        else:
            return render_template('view_bookings.html',
                                 message="Please select a department and year first.",
                                 is_logged_in=False)

@app.route('/clear-selection')
def clear_selection():
    """Clear department and year selection from session"""
    session.pop('selected_department', None)
    session.pop('selected_year', None)
    return redirect(url_for('view_bookings'))

# Additional Flask-SQLAlchemy helper functions
def get_safe_bookings_query():
    """
    Helper function to get bookings with safe joins to avoid None errors
    Uses Flask-SQLAlchemy's query builder with proper error handling
    """
    return Booking.query.options(
        db.joinedload(Booking.hall),
        db.joinedload(Booking.year),
        db.joinedload(Booking.department),
        db.joinedload(Booking.user)
    ).join(User, Booking.user_id == User.id)\
     .join(Hall, Booking.hall_id == Hall.id)\
     .join(Year, Booking.year_id == Year.id)\
     .join(Department, Booking.department_id == Department.id)

def validate_booking_relationships():
    """
    Helper function to check for orphaned bookings (useful for debugging)
    """
    orphaned_bookings = db.session.query(Booking.booking_session).outerjoin(
        User, Booking.user_id == User.id
    ).filter(User.id.is_(None)).all()
    
    if orphaned_bookings:
        print(f"Warning: Found {len(orphaned_bookings)} bookings with invalid user references")
    
    return len(orphaned_bookings) == 0



      
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
