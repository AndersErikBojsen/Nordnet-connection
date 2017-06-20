import socket
import ssl
import time
import base64
from M2Crypto import RSA
import httplib, urllib
import json
import Feed

class Login(object):

    def print_json(j, prefix=''):
        for key, value in j.items():
            if isinstance(value, dict):
                print '%s%s' % (prefix, key)
            else:
                print '%s%s:%s' % (prefix, key, value)

    username = 'sebc5325'
    password = 'qweasd123'
    service = 'NEXTAPI'
    URL = 'api.test.nordnet.se'
    API_VERSION = '2'

    timestamp = int(round(time.time() * 1000))
    timestamp = str(timestamp)
    buf = base64.b64encode(username) + ':' + base64.b64encode(password) + ':' + base64.b64encode(timestamp)
    rsa = RSA.load_pub_key('NEXTAPI_TEST_public.pem')
    encrypted_hash = rsa.public_encrypt(buf, RSA.pkcs1_padding)
    hash = base64.b64encode(encrypted_hash)

    headers = {"Accept": "application/json"}
    conn = httplib.HTTPSConnection(URL)



    # GET server status
    conn.request('GET', '/next/' + API_VERSION + '/', '', headers)
    r = conn.getresponse()
    response = r.read()
    j = json.loads(response)
    print_json(j)

    # POST login
    params = urllib.urlencode({'service': 'NEXTAPI', 'auth': hash})
    conn.request('POST', '/next/' + API_VERSION + '/login', params, headers)
    r = conn.getresponse()
    response = r.read()
    j = json.loads(response)
    print_json(j)
    session_key = j["session_key"]
    Feed.GetRequests().create_market_list(session_key, headers)
    Feed.GetRequests().instrument_name(session_key, headers, 'FINGerprint')


#################################################################################
    # Create SSL-wrapped socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_socket = ssl.wrap_socket(s)
    # Connect to socket
    ssl_socket.connect(("pub.api.test.nordnet.se", 443))
    print repr(ssl_socket.getpeername)
    print ssl_socket.cipher()
    # Send session key
    cmd = {"cmd": "login", "args": {"session_key": session_key, "service": "NEXTAPI"}}
    num_bytes = ssl_socket.write(json.dumps(cmd) + "\n")
    print "Session key sent (%d bytes)" % num_bytes
    # Get account information

    # Subscribe to a stock
    market = 11
    instruments = ["101", "4870"]  # ERIC B and FING B

    for i in range(0, len(instruments)):
        instrument = instruments[i]
        cmd = {"cmd": "subscribe", "args": {"t": "price", "m": 11, "i": instrument}}
        numBytes = ssl_socket.send(json.dumps(cmd) + "\n")
        print("Subscription request sent for market = %d and instrument = %s (%d bytes)" % (11, instrument, numBytes))
    # Read stream
    print "Reading stream"
    for i in range(10):
        output = ssl_socket.read(1024)
        print (output)

    time.sleep(1)
    print ("-")
    output = ssl_socket.recv()
    print (output)

    # print "Closing socket connection..."
    del ssl_socket
    s.close()


