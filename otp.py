import base64
import hashlib
import hmac
import time

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from google.appengine.ext import ndb
import webapp2

def get_otp(key):
    key = base64.b32decode(key)
    counter = format(int(time.time()) // 30, '016x').decode('hex')
    raw_otp = hmac.new(key, counter, hashlib.sha1).hexdigest()
    offset = int(raw_otp[-1], 16) * 2
    truncated = int(raw_otp[offset:offset + 8], 16) & 0x7fffffff
    return str(truncated)[-6:].zfill(6)

class Account(ndb.Model):
    totp_secret = ndb.StringProperty(indexed=False)

class User(ndb.Model):
    public_key = ndb.StringProperty(indexed=False)

class OTP(webapp2.RequestHandler):
    def get(self, account, user):
        otp = get_otp(Account.get_by_id(account).totp_secret)
        public_key = RSA.importKey(User.get_by_id(user).public_key)
        cipher = PKCS1_OAEP.new(public_key)
        self.response.write(cipher.encrypt(otp + "\n"))

class Seed(webapp2.RequestHandler):
    def get(self):
        Account(id='test', totp_secret='test').put()
        User(id='test', public_key='test').put()

app = webapp2.WSGIApplication([
    (r'/([-A-Za-z]+)/([-A-Za-z]+)', OTP),
    (r'/seed', Seed),
], debug=True)
