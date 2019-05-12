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


class LoginAPI(Resource):

    def post(self):
      f = open("/home/ec2-user/python_codes/output.txt","w")
      try:
        some_json = request.get_json()
        f.write("type of some_json: " + str(type(some_json)))
        user = some_json['country_code'] + '_' + some_json['phone_number']
        mob_no = some_json['country_code'] + some_json['phone_number']
        l_otpFromUser = some_json['otp']
        l_key = 'otp_' + mob_no
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
            h_key = 'details_' + user
            details = r.hgetall(h_key)
            if len(details) == 0:
                status = r.incr('user_id_counter')
                user_id = status
                del some_json['otp']
                r.hset(h_key, str(user_id), str(some_json))
                f.close()
                return ({'user_id': user_id}, 201)
            for x in details:
                l_id = x.decode('utf-8')
                l_json = details[x].decode('utf-8')
            f.close()
            return ({'user_id': l_id, 'user_details': l_json}, 200)

      except:
        f.close()
        return ({'error': 'exception'}, 400)

class sendOtpAPI(Resource):

    def post(self):
      try:
        some_json = request.get_json()
        user = some_json['country_code'] + some_json['phone_number']
        otpobj =  sendotp.sendotp('30349Af2uB99a7996063bc8','Your OTP is {{otp}}.')
        l_otp = random.randint(1000,9999)
        l_key = 'otp_' + user
        status = r.setex(l_key,150,l_otp)
        otpobj.send(user,'msgind',l_otp)
        return ({'result': 'OK'}, 200)
      except:
        return ({'error': 'exception'}, 400)


api.add_resource(HelloWorld, '/')
api.add_resource(LoginAPI, '/login')
api.add_resource(sendOtpAPI, '/sendOTP')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)

