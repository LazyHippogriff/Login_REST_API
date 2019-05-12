# Login_REST_API
Implementation of a login REST API in Python3.6 using Flask-RESTful(https://flask-restful.readthedocs.io/en/latest/), redis-py(https://github.com/andymccurdy/redis-py) and Redis(https://redis.io/) 

The api.py code implements 2 REST APIs: 
1. http://13.127.225.85:5010/sendOTP
2. http://13.127.225.85:5010/login

Both APIs accept POST requests and accept data in JSON format. The details of the customer(JSON) are stored in Redis database.

# Description
The first API will accept country code and mobile number of the user and send him a 4 digit OTP using msg91 API(https://github.com/MSG91/sendotp-python).

Given below is a sample curl command and its output.
Command: curl -sS -H "content-type: application/json" -d '{"country_code":"91", "phone_number":"1122334455"}' -X POST http://13.127.225.85:5010/sendOTP
Output: {"result": "OK"}

When successful, this API will send a 4 digit code to the mobile number and also will save this OTP in Redis for a time duration of 150 seconds. This OTP has to be used by the user in the input data for the 2nd API.

The second API will accept, along with the country code and mobile number of the user, the OTP and any other details the user want to send. The API will match the OTP with the OTP stored in Redis and if matched, the API will store the details of the user in the database against a unique User ID(if the user had not existed). On success, the API will return the user ID and if the user had existed before then it will also return the saved details in JSON. 

Given below is a sample curl command and its output.

Command: curl -sS -H "content-type: application/json" -d '{"country_code":"91", "phone_number":"1122334455","otp":"4932","age":"25"}' -X POST http://13.127.225.85:5010/login
Output: Output: {"user_id": "2", "user_details": "{'country_code': '91', 'phone_number': '1122334455', 'age': '25'}"}
