from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
from flask.ext.login   import UserMixin
from . import db,login_manager

#The user loader callback function receives a user identifier as a Unicode string. The
#return value of the function must be the user object if available or None otherwise.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get( int(user_id) )

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(64), unique=True, index=True)
    username      = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed     = db.Column(db.Boolean, default=False)
    img_profile   = db.Column(db.String(128), nullable=True)

    subjects      = db.relationship('Subject', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @property
    def imgsrc(self):
        if self.img_profile :
            return url_for('static',filename='uploads/'+self.img_profile)

        return url_for('static',filename='uploads/placeholder_img_profile.png')
       
    
    def __repr__(self):
        return '<User %r>' % self.username


class Subject(db.Model):
    __tablename__ = 'subjects'
    id            = db.Column(db.Integer, primary_key=True)
    subject       = db.Column(db.String(255), index=True)
    description   = db.Column(db.String(255), nullable=True)

    user_id       = db.Column(db.Integer, db.ForeignKey('users.id')) 
    
    """
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    """

    def __repr__(self):
        return '<Subject %r>' % self.subject

class Grade(db.Model):
    __tablename__ = 'grades'
    id            = db.Column(db.Integer, primary_key=True)
    grade         = db.Column( db.Integer )
    date          = db.Column(db.Date, index=True)
    description   = db.Column(db.String(255), nullable=True)
    
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id')) 
    #user          = db.relationship('User', backref=db.backref('users') ) 
    subject_id    = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    #subject       = db.relationship('Subject', backref=db.backref('subjects') )
    
    def __repr__(self):
        return '<Grade %r>' % self.grade



class Homework(db.Model):
    __tablename__ = 'homeworks'
    id            = db.Column(db.Integer, primary_key=True)
    homework      = db.Column(db.String(255) )
    description   = db.Column(db.String(255), nullable=True)
    deadline      = db.Column(db.Date)
    completed     = db.Column(db.Boolean, default=False)
    priority      = db.Column(db.Integer)

    user_id       = db.Column(db.Integer, db.ForeignKey('users.id')) 
    subject_id    = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    subject       = db.relationship('Subject')

    def __repr__(self):
        return '<Homework %r>' % self.homework

class Priority :
    LOW    =  0x01
    NORMAL =  0x02
    HIGH   =  0x04