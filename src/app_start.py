from flask import Flask, render_template, request

from call_api import *

def create_application():
	application = Flask (__name__, template_folder='templates')

	@application.route('/')
	def home():
		
		return render_template('index.html', payment_method=paymentMethods(), client_key=returnKey(), session_id=returnSessionId())


	@application.route('/api/sessions', methods=['POST'])
	def sessions():
		host_url = request.host_url 

		return createSession(host_url)

	@application.route('/redirect', methods=['POST', 'GET'])
	def redirect():
		payload = request.get_json()
		# print (payload)
		return paymentDetails(payload)

	@application.route('/payment', methods=['POST', 'GET'])
	def payment():
		host_url = request.host_url
		payload = request.get_json()
		print ("Payment Payload")
		print (payload)
		return makePayment(host_url, payload)

	@application.route('/success')
	def success():
		
		return render_template('thanks.html', client_key=returnKey())


	return application


if __name__ == '__main__':
    web_app = create_application()
    web_app.run(debug=True, port=5000, host='0.0.0.0')