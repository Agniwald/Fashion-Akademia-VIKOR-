from flask import Flask, render_template, request, make_response
from flask_mail import Mail, Message
from config import config_mail, config_mail_password, config_recipients

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = config_mail
app.config['MAIL_PASSWORD'] = config_mail_password
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = config_mail
mail = Mail(app)


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/basic")
def basic():
	return render_template("basic.html")


@app.route("/underwear")
def underwear():
	return render_template("underwear.html")


@app.route("/pro")
def pro():
	return render_template("pro.html")


@app.route("/pc")
def pc():
	return render_template("pc.html")


@app.route("/sitemap")
def sitemap():
	template = render_template('sitemap.xml')
	response = make_response(template)
	response.headers['Content-Type'] = 'application/xml'
	return response


@app.route("/robots.txt")
def robots():
	template = render_template('robots.txt')
	response = make_response(template)
	response.headers['Content-Type'] = 'application/txt'
	return response


@app.route("/send", methods=["POST"])
def send():
	body_message = f"Запрос на связь:" \
					f"\nИмя: {request.form['name']}" \
					f"\nE-mail: {request.form['email']}" \
					f"\nТелефон: {request.form['phone']}" \
					f"\nВид связи: {request.form['options']}"
	if "course" in request.form.keys():
		body_message += f"\nКурс: {request.form['course']}"
	
	msg = Message("VIKOR", body=body_message, recipients=config_recipients)
	mail.send(msg)
	
	return render_template('success.html')


@app.errorhandler(404)
def not_found(e):
	return render_template('404.html'), 404


if __name__ == '__main__':
	app.run(threaded=True, port=5000)
