# # from pypaystack import Transaction, Customer, Plan

# # """
# # All Response objects are a tuple containing status_code, status, message and data
# # """

# # #Instantiate the transaction object to handle transactions.  
# # #Pass in your authorization key - if not set as environment variable PAYSTACK_AUTHORIZATION_KEY

# # transaction = Transaction(authorization_key="sk_myauthorizationkeyfromthepaystackguys")
# # response = transaction.charge("customer@domain.com", "CustomerAUTHcode", 10000) #Charge a customer N100.
# # response  = transaction.verify(refcode) #Verify a transaction given a reference code "refcode".


# # #Instantiate the customer class to manage customers

# # customer = Customer(authorization_key="sk_myauthorizationkeyfromthepaystackguys")
# # response = customer.create("customer2@gmail.com", "John", "Doe", phone="080123456789") #Add new customer
# # response = customer.getone("CUS_xxxxyy") #Get customer with customer code of  CUS_xxxxyy
# # response = customer.getall() #Get all customers


# # #Instantiate the plan class to manage plans

# # plan = Plan(authorization_key="sk_myauthorizationkeyfromthepaystackguys")
# # response = plan.create("Test Plan", 150000, 'Weekly') #Add new plan
# # response = plan.getone(240) #Get plan with id of 240
# # response = plan.getall() #Get all plans
# import requests

# # Set up the API endpoint and headers
# url = 'https://api.paystack.co/transaction/initialize'
# headers = {
#     'Authorization': 'Bearer sk_test_8f1d2a9288296f690d843434b760a147a8353bb2',
#     'Content-Type': 'application/json'
# }

# # Set up the request payload
# payload = {
#     'amount': 500000,  # Amount in kobo (e.g., 5000 Naira)
#     'email': 'customer@example.com',
#     'callback_url': 'https://example.com/payment-callback'
# }

# # Send the API request
# response = requests.post(url, json=payload, headers=headers)

# # Handle the API response
# if response.status_code == 200:
#     data = response.json()
#     # Process the data returned from Paystack
#     print(data)
# else:
#     # Handle the error response
#     print(response.text)


# import requests
# from django.shortcuts import redirect

# def initiate_payment(request):
#     # Set up the API endpoint and headers
#     url = 'https://api.paystack.co/transaction/initialize'
#     headers = {
#         'Authorization': 'Bearer YOUR_SECRET_KEY',
#         'Content-Type': 'application/json'
#     }

#     # Set up the request payload
#     payload = {
#         'amount': 500000,  # Amount in kobo (e.g., 5000 Naira)
#         'email': 'customer@example.com',
#         'callback_url': request.build_absolute_uri('/payment-callback/')
#     }

#     # Send the API request
#     response = requests.post(url, json=payload, headers=headers)

#     # Handle the API response
#     if response.status_code == 200:
#         data = response.json()
#         authorization_url = data['data']['authorization_url']
#         return redirect(authorization_url)
#     else:
#         # Handle the error response
#         return HttpResponse(response.text, status=response.status_code)

print(365*24*3600*2)