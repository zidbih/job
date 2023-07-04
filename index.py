import datetime
from flask import Flask,render_template,redirect,url_for,request,flash,session,jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///job.db'
app.config['SECRET_KEY']='my secret key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

db=SQLAlchemy(app)

#decorator to block the entry with out login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id=session.get('user_id')
        if  user_id is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

#signup page
@app.route('/',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            my_data=UsersInfo(email=email,password=password)
            db.session.add(my_data)
            db.session.commit()
            flash(f"Welcomme  {email[:email.index('@')]} Login Here Please")
            return redirect(url_for('login'))
        except:
            flash("The Email Alreaddy Exists Try Onther One!")
            return render_template('signup.html')
    return render_template('signup.html',title='Find Job')


#login page
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=UsersInfo.query.filter(UsersInfo.email==email,UsersInfo.password==password).first()
        if user:
            flash(f"Welcome  {user.email[:user.email.index('@')]} in FindJob")
            user_id =  user.id
            session['user_id'] =  user_id
            return redirect(url_for('home_page'))
        else:
            flash("Sorry The Email OR Password Not Correct")
    return render_template('login.html',title='login')

#home page
@app.route('/home',methods=['GET','POST'])
@login_required
def home_page():
    user_id=session['user_id']
    image=UsersInfo.query.get(user_id)
    sender=Sender.query.filter_by(reciver_id=user_id).all()
    return render_template('index.html',title='home',
                           background=image.background_picture,
                           profile=image.profile_picture,
                           email=image.email,
                           name=image.name,
                           phone=image.phone,
                           adress=image.adress,
                           profession=image.profession,
                           notification=image.notification,
                           sender=sender,
                           nbr_sender=len(sender))
                          

@app.route('/upload_profile', methods=['POST','GET'])
def upload_profile():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            user_id = session['user_id']
            user = UsersInfo.query.get(user_id)
            user.profile_picture = filename
            db.session.commit()
            return redirect(url_for('home_page'))
    flash("Please Choose The Image First!")
    return redirect(url_for('home_page'))


@app.route('/upload', methods=['POST','GET'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            user_id = session['user_id']
            user = UsersInfo.query.get(user_id)
            user.background_picture = filename
            db.session.commit()
            return redirect(url_for('home_page'))
    flash("Please Chooose The Image First")
    return redirect(url_for('home_page'))

#complete information
@app.route('/complete',methods=['GET','POST'])
def complete_info():
    if request.method=='POST':
        name=request.form['name']
        phone=request.form['phone']
        adress=request.form['adress']
        profession=request.form['profession']
        
        user_id=session['user_id']
        user=UsersInfo.query.get(user_id)
        try:
            user.name=name
            user.phone=phone
            user.adress=adress
            user.profession=profession
            
            db.session.commit()
            return redirect(url_for('home_page'))
        except:
            flash("Some Thing Wrong Please Try Again!")
    return redirect(url_for('home_page'))

#result for the search of someone
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        name = request.form['search']
        if name!='':
            data=UsersInfo.query.filter_by(name=name).all()
            return render_template('search.html', users=data,length=len(data))
    return redirect(url_for('home_page'))

@app.route('/demande_job',methods=['POST','GET'])
def demande_job():
    if request.method=='POST':
        id=request.form['id']
        user_recive=UsersInfo.query.get(id)
        user_id=session['user_id']
        user_sender=UsersInfo.query.get(user_id)
        if user_sender.id !=user_recive.id:
            if user_recive:
                user_recive.notification+=1
                sender=Sender(reciver_id=user_recive.id,sender_name=user_sender.name,sender_phone=user_sender.phone)
                db.session.add(sender)
                db.session.commit()
                flash(f"The Demande Was Send Successfuly")
            else:
                flash(f"The Demande Was wrong")
        else:
            flash('You can\'t send demande job to your self')
    return redirect(url_for('home_page'))

@app.route('/chat',methods=['POST','GET'])
def chat():
    if request.method=='POST':
        sender_id=request.form['accept']
        sender=UsersInfo.query.get(sender_id)
        sender_image=sender.profile_picture
        sender_name=sender.name
        my_id=session['user_id']
        me=UsersInfo.query.get(my_id)
        my_image=me.profile_picture
        my_name=me.name
        return render_template('chat.html',sender_id=sender_id,sender_image=sender_image,sender_name=sender_name,my_image=my_image,my_name=my_name)
    return redirect(url_for('home_page'))

@app.route('/send_msg',methods=['POST'])
def send_msg():
    message=request.form['message']
    sender=session['user_id']
    reciver=request.form['reciver']
    
    message_info=Message(sender=sender,recive=reciver,message=message)
    db.session.add(message_info)
    db.session.commit()
    success=[{"success":"success"}]
    
    return success
    
@app.route('/get_send_msg',methods=['GET','POST'])
def get_send_msg():
    reciver=request.form['reciver']
    sender=session['user_id']
    
    data=Message.query.filter(Message.sender==sender,Message.recive==reciver).all()
    
    result=[]
    for msg in data:
        result.append({"send_msg":msg.message})
    return result
    
@app.route('/get_recived_msg',methods=['GET','POST'])
def get_recived_msg():
    reciver=request.form['reciver']
    sender=session['user_id']
    
    data=Message.query.filter(Message.sender==reciver,Message.recive==sender).all()
    
    result=[]
    for msg in data:
        result.append({"recived_msg":msg.message})
    return result  
    
    
#cration of the tables(classes)

class UsersInfo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(125),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    background_picture=db.Column(db.String(255),default='default.jpg')
    profile_picture=db.Column(db.String(255),default='default-user.png')
    name=db.Column(db.String(100))
    phone=db.Column(db.Integer,unique=True)
    adress=db.Column(db.String(50))
    profession=db.Column(db.String(100))
    notification=db.Column(db.Integer,default=0)

class Sender(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    reciver_id=db.Column(db.Integer)
    sender_name=db.Column(db.String(125))
    sender_phone=db.Column(db.Integer)
    send_date=db.Column(db.String(100),default=datetime.datetime.now())
    
    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    sender = db.Column(db.Integer)
    recive = db.Column(db.Integer)



if __name__=='__main__':
    app.run(debug=True)