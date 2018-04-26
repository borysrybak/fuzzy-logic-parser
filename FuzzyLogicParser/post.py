import http.client, urllib.request, urllib.parse, urllib.error, base64
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

try:
    conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
    img_file = 'handwritten/handwritten_sample_1.jpg'
    img = open(img_file, 'rb').read()
    resized_img = helpers.image_resize(img)
    
    conn.request("POST", "/vision/v1.0/recognizeText?%s" % params, resized_img, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))