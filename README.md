## Motivation
While working as a face to face fundraiser, I have noticed that many people donate to a lot of charity and they forget what charities they are doing and they lose track of it. 
I manually add these charities to my notepad, just so that I don't forgtet. 

Many of the potential donors that I speak, could not able to donate, becuase they have lost the track of number of charities they are doing inclduing amount and date the dontation goes through. 
I wanted to create a web app that allows these payments to get synced in the google calender to give the person a quick overview about their donations and analyse their sitution. 
This idea can also be applied for any automatic payments that are linked with paypal. 

## Code workflow
Want to create a web app, that allows you to link your paypal and google calender API, once it's authorised with necessary permissions. 
After, it pulls the automating payments from the paypal api, and then adds them to the google calender.

## Code break in a live app
### PayPal does not allow to access `/v1/billing/plans` Not sure why!!!
```error
raise Exception(f"Failed to get PayPal subscriptions: {response.text}")
Exception: Failed to get PayPal subscriptions: {"name":"NOT_AUTHORIZED","message":"Authorization failed due to insufficient permissions.",
"debug_id":"","details":[{"issue":"PERMISSION_DENIED","description":"You do not have permission to access or perform operations on this resource."}],
"links":[{"href":"https://developer.paypal.com/docs/api/v1/billing/subscriptions#NOT_AUTHORIZED","rel":"information_link",
"method":"n":"You do not have permission to access or perform operations on this resource."}],
"links":[{"href":"https://developer.paypal.com/docs/api/v1/billing/subscriptions#NOT_AUTHORIZED","rel":"information_link","method":"GET"}]}
```

### Accessing invoices needs extra permission endpoint "/v1/reporting/transactions"
```error
Failed to retrieve transactions: 403
{"name":"PERMISSION_DENIED","message":"You are not authorized to perform 3rd party calls for this API.
 You need to be part of the PayPal Partner Program for the same.
 Please reach out to your Partner Manager for more information.","debug_id":"","details":[],"links":[]}
```
The error suggests that access to the Transaction Search API is restricted to those in the PayPal Partner Program. 
You will need to enroll in this program if you plan to make API calls on behalf of other PayPal accounts.
