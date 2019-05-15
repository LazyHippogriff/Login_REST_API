from flask import Flask, request
from flask_restful import Resource, Api
from redis import Redis
from sendotp import sendotp
import random

app = Flask(__name__)
api = Api(app)
r = Redis(host='localhost', port=6379, db=0)


class HelloWorld(Resource):

    def get(self):
        return {'about': 'World\'s Best Application!'}


class getUserDetailsAPI(Resource):

    def get(self):
      f = open("/home/ec2-user/python_codes/output.txt","w")
      try:
        some_json = request.get_json()
        uId = some_json['ID']
        if uId is None:
          f.close()
          return({'error':'Missing User ID in the Json.'},409)

        f.write("UID: "+str(uId))
        h_key = uId + "_profile"
        userDetails = r.get(h_key)
        if userDetails is None:
          f.close()
          return({'error':'User ID not found.'},404)

        f.write("User Details: "+ userDetails.decode('utf-8'))
        f.close()
        return ({'user_id': uId, 'user_details': userDetails.decode('utf-8')}, 200)

      except:
        f.close()
        return ({'error': 'exception'}, 400)


class putUserDetailsAPI(Resource):

    def put(self):
      f = open("/home/ec2-user/python_codes/output.txt","w")
      try:
        some_json = request.get_json()
        uId = some_json['ID']
        if uId is None:
          f.close()
          return({'error':'Missing User ID in the Json.'},409)

        f.write("UID: "+str(uId))
        del some_json['ID']

        h_key = uId + "_profile"
        r.set(h_key, str(some_json))
        f.close()
        return ({'result': 'OK'}, 200)

      except:
        f.close()
        return ({'error': 'exception'}, 400)


class verifyOtpAPI(Resource):

    def post(self):
      f = open("/home/ec2-user/python_codes/output.txt","w")
      try:
        some_json = request.get_json()
        f.write("type of some_json: " + str(type(some_json)))
        user = some_json['country_code'] + '_' + some_json['phone_number']
        l_otpFromUser = some_json['otp']
        l_key = user + "_OTP"
        l_otp = r.get(l_key)
        if l_otp is None:
            f.close()
            return({'error':'OTP expired. Get new OTP.'},400)
        else:
          l_otp = l_otp.decode('utf-8')
        f.write("l_otp: " + str(l_otp) + "\nl_otpFromUser: \
" + str(l_otpFromUser))
        if l_otp != l_otpFromUser:
            f.close()
            return({'error':'Wrong OTP.'},400)
        else:
            f.close()
            return ({'user_id': user}, 200)

      except:
        f.close()
        return ({'error': 'exception'}, 400)

class loginAPI(Resource):

    def post(self):
      try:
        some_json = request.get_json()
        user = some_json['country_code'] + "_" + some_json['phone_number']
        mob_no = some_json['country_code'] + some_json['phone_number']
        otpobj =  sendotp.sendotp('9Af2uB93ad8','Your OTP is {{otp}}.')
        l_otp = random.randint(1000,9999)
        l_key = user + "_OTP"
        r.setex(l_key,150,l_otp)
        otpobj.send(mob_no,'msgind',l_otp)
        return ({'result': 'OK'}, 200)
      except:
        return ({'error': 'exception'}, 400)


api.add_resource(HelloWorld, '/')
api.add_resource(verifyOtpAPI, '/verifyOTP')
api.add_resource(loginAPI, '/login')
api.add_resource(putUserDetailsAPI, '/putUserDetails')
api.add_resource(getUserDetailsAPI, '/getUserDetails')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
