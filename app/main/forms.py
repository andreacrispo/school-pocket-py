from flask import g
from flask.ext.login import current_user
from flask.ext.babel import lazy_gettext as lazy_gt, gettext
from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, DateField, DateTimeField, SelectField, SubmitField 
from wtforms.validators import Required, Length
from wtforms import ValidationError
from ..models import Subject, Priority
from datetime import datetime 




class DateFieldLocale(DateTimeField):
    def __init__(self, label=None, validators=None, format='%Y-%m-%d', **kwargs):
        super(DateFieldLocale, self).__init__(label, validators, format, **kwargs)

    def process_formdata(self, valuelist):
    	if valuelist:
    		date_str = ''.join(valuelist)
    		print date_str
    		try:
    			format = '%Y-%m-%d'
    			self.data = datetime.strptime(date_str, format).date()
    		except ValueError:
    			raise ValueError(lazy_gt('Not a valid date value'))


class SubjectForm(Form):

	subject 	= StringField( lazy_gt('Subject') , validators=[Required()])
	description = TextAreaField( lazy_gt('Description') )
	submit 	    = SubmitField( lazy_gt('Insert') )
 

class GradeForm(Form) :

	grade 		= IntegerField( lazy_gt('Grade') , validators=[Required()])
	description = TextAreaField( lazy_gt('Description') )
	date        = DateFieldLocale( lazy_gt('Date') ) 
	subject 	= SelectField( lazy_gt('Subject') , coerce=int) 
	submit 	    = SubmitField( lazy_gt('Insert') )

	def __init__(self, *args, **kwargs):
		super(GradeForm, self).__init__(*args, **kwargs)
		self.subject.choices = [ (s.id,s.subject)
								  for s in Subject.query.filter_by(user_id= current_user.id)]

class HomeworkForm(Form) :

	homework    = StringField( lazy_gt('Homework') , validators=[Required()])
	description = TextAreaField( lazy_gt('Description') )
	date    	= DateFieldLocale( lazy_gt('Deadline') )   
	subject 	= SelectField( lazy_gt('Subject'), coerce=int)
	priority	= SelectField( lazy_gt('Priority'), coerce=int) 
	submit 	    = SubmitField( lazy_gt('Insert') )

	def __init__(self, *args, **kwargs):
		super(HomeworkForm, self).__init__(*args, **kwargs)
		self.subject.choices = [ (s.id,s.subject)
								  for s in Subject.query.filter_by(user_id= current_user.id)]

		self.priority.choices = [ (Priority.HIGH, lazy_gt('High') ) , (Priority.NORMAL,lazy_gt('Normal') ), (Priority.LOW, lazy_gt('Low') )] 