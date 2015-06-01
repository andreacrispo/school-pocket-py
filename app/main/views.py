from flask import g, render_template, session, abort, redirect, flash, url_for, current_app
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext
from .. import db, babel
from ..models import User, Subject, Grade, Homework, Priority
from ..email import send_email
from . import main
from .forms import SubjectForm, GradeForm, HomeworkForm


@main.route('/')
def index(): 
	if current_user.is_authenticated() :
		models = {
			'grades':Grade.query.filter_by( user_id= current_user.id).count(),
			'subjects':Subject.query.filter_by( user_id= current_user.id).count(),
			'homeworks':Homework.query.filter_by( user_id= current_user.id).count() 
		}
		return render_template('index.html', models=models )
	return redirect( url_for('auth.login') )


@main.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('profile.html',user=user)


@main.route('/subjects')
@login_required
def subjects():
	subjects = Subject.query.filter_by(user_id= current_user.id).order_by(Subject.subject)
	return render_template('subjects.html',subjects=subjects)


@main.route('/subject/insert', defaults={'id':None}, methods=['GET', 'POST'])
@main.route('/subject/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def action_subject(id):
	subject = Subject.query.get_or_404(id) if id else None			#Return the subject if id is given else None - use to fill the form for edit porpuse
	form = SubjectForm( obj = subject )
	if form.validate_on_submit() :		
		if id is None:					# insert new grade
			subject_to_add = Subject( subject= form.subject.data,
								  	  description = form.description.data,
								  	  user_id= current_user.id)
			db.session.add( subject_to_add )
			flash( gettext('The subject has been inserted.') , 'success')

		else:		# edit grade
			subject.subject 	 = form.subject.data
			subject.description  = form.description.data
			flash( gettext('The subject has been update.') , 'success')
		db.session.commit()
		return redirect( url_for('main.subjects') )
	return render_template('forms.html',form=form)



@main.route('/subject/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    flash( gettext('Subject was deleted successfully'), 'success')
    return redirect( url_for('main.subjects') )


@main.route('/grades')
@login_required
def grades():
	grades   = Grade.query.filter_by(user_id= current_user.id).order_by(Grade.subject_id,Grade.grade)
	subjects = Subject.query.join(Grade).filter_by(user_id= current_user.id).order_by(Subject.subject)
	return render_template('grades.html', grades=grades, subjects=subjects)


@main.route('/grade/insert', defaults={'id':None}, methods=['GET', 'POST'])
@main.route('/grade/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def action_grade(id):
	grade = Grade.query.get_or_404(id) if id else None
	form = GradeForm( obj = grade )
	if form.validate_on_submit() :		
		if id is None:					# insert new grade
			grade_to_add = Grade( grade = form.grade.data,
								  date  = form.date.data,
								  description = form.description.data,
								  subject_id = form.subject.data,  
								  user_id= current_user.id)
			db.session.add( grade_to_add )
			flash( gettext('The grade has been inserted.') , 'success')

		else:		# edit grade
			grade.grade 	  = form.grade.data
			grade.description = form.description.data
			grade.date		  = form.date.data
			grade.subject_id  = form.subject.data
			flash( gettext('The grade has been update.') , 'success')
		db.session.commit()
		return redirect( url_for('main.grades') )
	return render_template('forms.html',form=form)


@main.route('/grade/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_grade(id) :
	grade = Grade.query.get_or_404(id)
	db.session.delete( grade )
	db.session.commit()
	flash( gettext('Grade was deleted successfully'), 'success')
	return redirect( url_for('main.grades') ) 


@main.route('/homeworks')
@login_required
def homeworks():
	priority = Priority()
	homeworks = Homework.query.filter_by(user_id= current_user.id)
	return render_template('homeworks.html', homeworks=homeworks, priority=priority)


@main.route('/homework/insert', defaults={'id':None}, methods=['GET', 'POST'])
@main.route('/homework/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def action_homework(id):
	homework = Homework.query.get_or_404(id) if id else None 
	form = HomeworkForm( obj = homework )

	if form.validate_on_submit() :		
		if id is None:					# insert new 
			homework_to_add = Homework( homework  = form.homework.data,
								        deadline  = form.date.data,
								  		description = form.description.data,
								  		priority    = form.priority.data,
								  		subject_id = form.subject.data,  
								  		user_id= current_user.id)
			db.session.add( homework_to_add )
			flash( gettext('The homework has been inserted.'), 'success')

		else:		# edit 
			homework.homework 	 = form.homework.data
			homework.description = form.description.data
			homework.deadline    = form.date.data
			homework.priority 	 = form.priority.data
			homework.subject_id  = form.subject.data
			flash( gettext('The homework has been update.'), 'success')
		db.session.commit()
		return redirect( url_for('main.homeworks') )
	return render_template('forms.html',form=form)


@main.route('/homework/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_homework(id) :
	homework = Homework.query.get_or_404(id)
	db.session.delete( homework )
	db.session.commit()
	flash( gettext('Homework was deleted successfully'), 'success')
	return redirect( url_for('main.homeworks') ) 


@main.route('/homework/update/<int:id>', methods=['GET','POST'])
@login_required
def update_homework(id) :
	homework = Homework.query.get_or_404(id)
	homework.completed = False if homework.completed else True
	db.session.commit()
	flash( gettext('Homework was update successfully'), 'success')
	return redirect( url_for('main.homeworks') ) 




@main.route('/chart', methods=['GET','POST'])
@login_required
def chart() :
	grades   = Grade.query.filter_by(user_id= current_user.id).order_by(Grade.subject_id,Grade.grade)
	subjects = Subject.query.join(Grade).filter_by(user_id= current_user.id).order_by(Subject.subject)
	return render_template('chart.html', grades=grades, subjects=subjects)