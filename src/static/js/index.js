const clientKey = JSON.parse(document.getElementById('client-key').innerHTML);
const paymentMethod = JSON.parse(document.getElementById('payment-method').innerHTML);
const sessionId = JSON.parse(document.getElementById('session-id').innerHTML);

const urlParams = new URLSearchParams(window.location.search);
const redirectResult = urlParams.get('redirectResult');


async function startCheckout() {

	//createSession
	// window.alert("create Session");
	const sessionResponse = await callServer("/api/sessions");
	// console.log(sessionResponse);

	// window.alert("create Checkout");
	const checkout = await createCheckout(sessionResponse);

	// window.alert("mounting Checkout");
	const dropin = checkout
	.create('dropin')
	.mount('#dropin-container');
}

async function finishCheckout(sessionId) {
    try {
    	// window.alert("check checkout");
    	// console.log(sessionId);
        const checkout = await createCheckout({id: sessionId});
        // window.alert("submit Checkout");
        checkout.submitDetails({details: {redirectResult}});
    } 
    catch (error) {
        console.error(error);
        alert("Error occurred. Look at console for details");
    }
}

async function createCheckout(session){
	const configuration = {
		paymentMethodsResponse: paymentMethod,
		clientKey: clientKey,
		locale: "en-US",
		environment: "test",
		session: session,
		showPayButton: true,
		analytics: {
			enabled: false // Set to false to not send analytics data to Adyen.
		},
		paymentMethodsConfiguration: {
			ideal: {
                showImage: true
            },
			card: {
                hasHolderName: true,
                holderNameRequired: true,
                name: "Credit or debit card w/ 3DS2",
                billingAddressRequired: true,
                enableStoreDetails: true,
                amount: {
                    value: 1000,
                    currency: "EUR"
                }
            },
            threeDS2: {
            	challengeWindowSize: '05'
            }
		},
		onPaymentCompleted: (result, component) => {
			// console.info(result);
			// console.error(component);
			callServer("/redirect", {details: {redirectResult}});
			resultPage(result);
		},
		onError: (error, component) => {
            console.error(error.name, error.message, error.stack, component);
        },
        onSubmit: (state, dropin) => {
        	// console.log(state.data);
        	callServer("/payment", state.data)
        	.then((response) => {
        		// console.log(response.action);
        		if (response.action){
        			// window.alert("action from response");
        			dropin.handleAction(response.action);
        		}
        		else if (response.resultCode === "Authorised") {
        			dropin.setStatus("success");
        			resultPage(response);
        		}
        	})
        	.catch((error) =>{
        		throw Error(error);
        	});
        }
	};

	return new AdyenCheckout(configuration);
}

function resultPage(res) {
	if (res.resultCode == "Authorised") {
		window.location.href = "/success";
	} 
	else {
		window.location.href = "/failure";
	}
}

async function callServer(url, data) {
	const res = await fetch(url, {
		method: "POST",
		body: data ? JSON.stringify(data) : "",
		headers: {
			"Content-Type": "application/json"
		}
	});



	return await res.json();
}

if (!redirectResult) {
	// window.alert("starting Checkout");
	startCheckout();
}
else{
	// window.alert("finishing Checkout");
    finishCheckout(sessionId);
}
