import os
from flask import current_app, render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.babel import gettext
from werkzeug import secure_filename
from ..models import User
from ..email import send_email
from .. import db
from . import auth
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ChangeEmailForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated():
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit() : 
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data) : 
			login_user(user,form.remember_me.data)
			return redirect( request.args.get('next') or  url_for('main.index'))
		flash( gettext('Invalid email or password'), 'error')
	return render_template('auth/login.html',form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User( email=form.email.data,
					 username=form.username.data,
					 password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm Your Account',
						'auth/email/confirm', user=user, token=token)
		flash( gettext('A confirmation email has been sent to you by email.'), 'success' )
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash( gettext('You have confirmed your account. Thanks!'), 'success' )
	else:
		flash( gettext('The confirmation link is invalid or has expired.'), 'error' )
	return redirect(url_for('main.index'))

	
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash( gettext('A new confirmation email has been sent to you by email.'), 'success' )
    return redirect(url_for('main.index'))


@auth.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form_email    = ChangeEmailForm()
	form_password = ChangePasswordForm()
	
	if form_password.validate_on_submit() :
		if current_user.verify_password( form_password.old_password.data) :
			current_user.password = form_password.new_password.data
			db.session.add(current_user)
			flash('Password update', 'success')
			return redirect( url_for('auth.edit_profile') )
		else:
			flash('Invalid password', 'error')
	if form_email.validate_on_submit() : 
		if current_user.verify_password(form_email.password.data) :
			current_user.email = form_email.email.data
			db.session.add(current_user)
			flash('Email update', 'success')
			return redirect( url_for('auth.edit_profile') )
		else:
			flash('Invalid password', 'error')
	return render_template('auth/edit_profile.html', form_password=form_password, form_email=form_email)

 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


@auth.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image_file = request.files['photo']
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
            image_file.save( file_path )
            current_user.img_profile = filename
            db.session.commit()
            flash('Immagine Profilo aggiornata', 'success')
            return redirect( url_for('auth.edit_profile') )

    return redirect( url_for('main.index') )

 

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))