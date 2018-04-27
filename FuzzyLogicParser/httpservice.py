import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import helpers
import json

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '',
}

params = urllib.parse.urlencode({
    # Request parameters
    'Printed': 'true',
})

regionapiaddress = 'westeurope.api.cognitive.microsoft.com'

def post_ocr(img_path):
    try:
        conn = http.client.HTTPSConnection(regionapiaddress)
        
        resized_img_path = helpers.image_resize(img_path)
        img = open(resized_img_path, 'rb').read()
    
        conn.request("POST", "/vision/v2.0/recognizeText?mode=Printed", img, headers)
        response = conn.getresponse()

        operationlocationaddress = response.getheader('operation-location')
        conn.close()

        return operationlocationaddress
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def get_ocr(operationlocationaddress):
    operationId = helpers.path_leaf(operationlocationaddress)
    try:
        conn = http.client.HTTPSConnection(regionapiaddress)
        conn.request("GET", "/vision/v2.0/textOperations/" + operationId, "{body}", headers)
        jsonresult, fail_condition = check_response_status(conn)
        while not fail_condition:
            conn = http.client.HTTPSConnection(regionapiaddress)
            conn.request("GET", "/vision/v2.0/textOperations/" + operationId, "{body}", headers)
            jsonresult, fail_condition = check_response_status(conn)

        conn.close()

        return jsonresult
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def check_response_status(conn):
    response = conn.getresponse()
    responsestatus = response.status
    resultsview = response.read()
    resultdecoded = resultsview.decode('utf-8')
    jsonresult = json.loads(resultdecoded)
    resultstatus = jsonresult['status']

    if resultstatus == 'Succeeded':
        return jsonresult, True
    else:
        return jsonresult, False