import requests
import json

CLIENT_KEY = "test_7ZCG2HRVQ5DYDG54CTVFVXKYFIKWXTBF"

URL= "https://checkout-test.adyen.com/v68"
HEADERS = {
	"x-API-KEY": "AQEyhmfxKonIYxZGw0m/n3Q5qf3VaY9UCJ14XWZE03G/k2NFikzVGEiYj+4vtN01BchqAcwQwV1bDb7kfNy1WIxIIkxgBw==-JtQ5H0iXtu8rqQMD6iAb33gf2qZeGKGhrMpyQAt9zsw=-3wAkV)*$kP%bCcSf",
	"content-type": "application/json"
}
SESSION_ID = "abc"

def returnSessionId():
	return SESSION_ID

def returnKey():
	return CLIENT_KEY

def paymentMethods():
	DATA = json.dumps({
		"merchantAccount": "AdyenRecruitmentCOM",
		"countryCode": "NL",
	  	"amount": {
	        "value": 1000,
	        "currency": "EUR"
	  	},
	    "channel": "Web",
  		"shopperLocale": "nl-NL"
	})
	try:
		response = requests.post(URL+"/paymentMethods",
			headers= HEADERS,
			data= DATA)
	except requests.exceptions.RequestException as e:
		raise SystemExit(e)

	# print(response)
	return response.json()


def createSession(host_url):
	DATA  = json.dumps({
		"merchantAccount": "AdyenRecruitmentCOM",
	  	"amount": {
	        "value": 1000,
	        "currency": "EUR"
	  	},
	    "returnUrl": host_url,
	    "reference": "Gary_checkoutChallenge",
	    "countryCode": "NL"
	})
	try:
		response = requests.post(URL+"/sessions",
			headers= HEADERS,
			data= DATA)
	except requests.exceptions.RequestException as e:
		raise SystemExit(e)

	# Setting SESSION_ID for Redirection
	global SESSION_ID 
	SESSION_ID = response.json()["id"]

	# formatting response
	formatted_response = dict( {'id': response.json()["id"], "sessionData": response.json()["sessionData"]} )
	response = json.dumps(formatted_response)
	print(response)

	# print(type(response))
	return response

def makePayment(host_url, data):
	if data.get("paymentMethod").get("type") == "scheme":
		DATA  = json.dumps({
		"merchantAccount": "AdyenRecruitmentCOM",
	  	"amount": {
	        "value": 1000,
	        "currency": "EUR"
	  	},
	    "returnUrl": host_url,
	    "reference": "Gary_checkoutChallenge",
	    "countryCode": "NL",

	    # 3DS2 Specific
	    "paymentMethod": data.get("paymentMethod"),
	    "browserInfo": data.get("browserInfo"),
	    "channel": "web",
	    "origin": data.get("origin"),
	    "billingAddress": data.get("billingAddress"),
	    "shopperEmail": "hamsterdam@hamster.com",
	    "shopperIP": "192.168.0.1"
	})

	if data.get("paymentMethod").get("type") == "ideal":
		DATA  = json.dumps({
		"merchantAccount": "AdyenRecruitmentCOM",
	  	"amount": {
	        "value": 1000,
	        "currency": "EUR"
	  	},
	    "returnUrl": host_url,
	    "reference": "Gary_checkoutChallenge",
	    "countryCode": "NL",
	    "paymentMethod": data.get("paymentMethod")
	})
	
	try:
		response = requests.post(URL+"/payments",
			headers= HEADERS,
			data= DATA)
	except requests.exceptions.RequestException as e:
		raise SystemExit(e)

	print("paymentResponse: ")
	print(response.json())

	return response.json()

# def makePaymentTest():
# 	DATA  = json.dumps({
# 		"merchantAccount": "AdyenRecruitmentCOM",
# 	  	"amount": {
# 	        "value": 1000,
# 	        "currency": "EUR"
# 	  	},
# 	    "returnUrl": "localhost:5000",
# 	    "reference": "Gary_checkoutChallenge",
# 	    "countryCode": "NL",
# 	    "paymentMethod": {
# 	        "type": "ideal",
# 	        "issuer": "1154"
#     	}
# 	})
# 	try:
# 		response = requests.post(URL+"/payments",
# 			headers= HEADERS,
# 			data= DATA)
# 	except requests.exceptions.RequestException as e:
# 		raise SystemExit(e)

# 	print("paymentResponse: ")
# 	print(response.json())

# 	return response


def paymentDetails(reference):
	DATA = json.dumps(reference)
	# formatted_reference = str(reference)
	# formatted_reference = formatted_reference.strip()
	try:
		response = requests.post(URL+"/payments/details",
			headers= HEADERS,
			data= DATA)
	except requests.exceptions.RequestException as e:
		raise SystemExit(e)

	print(response.json())
	return response.json()

def main():
	# makePaymentTest()
	# paymentMethods()
	createSession("https://localhost:5000")
	print(returnSessionId())
	# paymentDetails()
if __name__ == '__main__':
	main()