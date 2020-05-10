from flask_wtf import FlaskForm, RecaptchaField
from wtforms import TextField, StringField, PasswordField, validators
from wtforms.validators import DataRequired
from flask import Flask, render_template
from flask import request
from flask import jsonify

import boto3
import sys

# by Rafael Klock

ec2 = boto3.client('ec2')
security_group_id = 'sg-080ce2a7c35e04bca'

app = Flask(__name__)

app.config['SECRET_KEY'] = 'as&gbnXnUGg8777bsxX'
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']='6LeA1-kUAAAAAOR8MIJ0alYZIKVe2i3Otg1elzL8'
app.config['RECAPTCHA_PRIVATE_KEY']='6LeA1-kUAAAAAC_LIqK1gsWpDUgMTnvIhYFucGcu'
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}


class SignupForm(FlaskForm):
    username = TextField('Username')
    recaptcha = RecaptchaField()


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('passwd', [validators.DataRequired(),validators.Length(min=8)])



@app.route('/allowmeplease', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)


@app.route("/allow_my_ip_please", methods=["POST"])
def get_my_ip():
    passwd = request.form['password']
    name = request.form['name']
    ip_allow = str(request.remote_addr) + '/32'
    if passwd == 'XhiCo3vIdsYdHy9x':
        try:
            retorno = ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {'IpProtocol': '-1',
                     'IpRanges': [
                        {'CidrIp': ip_allow,
                         'Description': 'Allowed by web - ' + str(name)
                        }]
                    }
                ])
            print(retorno)
            return jsonify({ 'Sucesso, liberado': {'ip': ip_allow} }), 200
        except Exception as err: 
            return jsonify({'Erro': str(err)}), 200
    else:
        return jsonify({'access': 'denied'}), 200



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8007)
