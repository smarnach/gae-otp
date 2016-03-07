OTP generator for Google App Engine
-----------------------------------

Usage:

1. Create a new project in the Google developer console, say "opencraft-otp".
   Update app.yaml with the name of the project.

2. Upload to GAE:

       appcfg.py update app.yaml

3. Navigate to https://opencraft-otp.appspot.com/seed to create the tables in
   the Datastore.

4. Navigate to https://console.cloud.google.com/datastore?project=opencraft-otp
   and add SSH public keys and 2FA secrets.  Use custom names as key identifiers.

5. To receive a key for $APP encrypted with the key for user $SSH_KEY_USER, run

       curl -s https://opencraft-otp.appspot.com/$APP/$SSH_KEY_USER |
           openssl pkeyutl -decrypt -inkey ~/.ssh/id_rsa -pkeyopt rsa_padding_mode:oaep
