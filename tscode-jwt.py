def get_token(phone_number, xid = None):
  response = Response(status=200, content_type='text/plain')
  response.headers['Allow'] = 'GET'

  try:
    # Set token claims
    # Define the token time stamp validity range in seconds
    iss = 'your_telesign_customer_id'
    iat = int(time()) - 10
    exp = iat + 90

    # Unique identifier to verify status of transaction completion from
    # TeleSign's GET status by XID service

    xid = xid or str(uuid4())

    payload = {
        'iss' : iss,
        'iat' : iat,
        'exp' : exp,
        'phn' : phone_number,
        'xid' : xid
    }

    # Base64 decode your API key
    key = b64decode("your secret API key")

    # Base64 encode everything
    token = jwt.encode(payload, key)

    # Store the token in your DB (for use with MongoDB)
    result = jwt_db.tokens.insert_one(
        {
            'xid' : xid,
            'phone_number' : phone_number,
            'token' : token
        }
    )

  except Exception:
      # Add logging as required here
      token = ""
      response.status = 500

  return token

#FOR DEBUGGING (You can go to `0.0.0.0:5000/v1/token/<phone_number>/<xid>`)
if __name__ == "__main__": app.run(host = '0.0.0.0')
