import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import helpers

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'a46a5277cdc5482795f7881abd6b9894',
}

params = urllib.parse.urlencode({
    # Request parameters
    'handwriting': 'true',
})

def post_ocr(img_path):
    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        
        helpers.image_resize(img_path)
        resized_img_file = 'handwritten/resized/resized_file_2.jpg'
        img = open(resized_img_file, 'rb').read()
    
        conn.request("POST", "/vision/v1.0/recognizeText?%s" % params, img, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return response.headers