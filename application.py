import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import urllib.request, requests
import json
from flask_cors import CORS, cross_origin
import base64
import time
import backoff

application = Flask(__name__)

cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'
load_dotenv()

data = {
        'username': f'' + os.getenv('USER'),
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1589682409:'+ os.getenv('PASSWORD'),
        'queryParams': '{}',
        'optIntoOneTap': 'false'
} 

headers = {
    'authority': 'www.instagram.com',
    'method': 'POST',
    "path": "/api/v1/web/accounts/login/ajax/",
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'content-length': '356',
    'content-type': 'application/x-www-form-urlencoded',
    "cookie" : 'fbm_124024574287414=base_domain=.instagram.com; mid=Ykx7ZgALAAEuA5ym-037fLHn17yE; ig_did=1878DCE3-1DD2-4E8A-AEBF-F030FB4E39C5; ig_nrcb=1; datr=QDcAY3K6EgsSgRBNdwVvBkB-; shbid="2028\0542237186360\0541711574683:01f7885efc0cdd6a9c2af3a750d21dbb7bda580dabe9c87be3df6532cef209006ae2ad0c"; shbts="1680038683\0542237186360\0541711574683:01f7ca084f07ce34887509e1495aa2843428a9a281cfbf2dbeefb65569e26ef66f56d67b"; dpr=2; ds_user_id=58604319986; csrftoken=omem4YL9qqhfhHh8Xz0m7wsgBA4hYxIp; fbsr_124024574287414=G74oNgocuNbj2nyxoWufy7vi5JhOIz2IRTowj5LOiFc.eyJ1c2VyX2lkIjoiMTAwMDE0MjI4OTgzMDMzIiwiY29kZSI6IkFRRGNueTMxSWFnMWhOZEtqR2Jnbk1Ed2NJT24weGhJUHNzVXRWbGJZd2FMZTF1dElEdWF0cUFwTjVjOW9zWGlDMW1fMVBLY1NzQ0VQSlFuVC1uVURvTGFJMi1sSU9xYk5RX3Y2NTBldW5oeV9oZVU0VnFjWElrY3VqSVYtLWx1UUgwd2pjQWdHeTdCUGlySEp6UlJZaU5kVlFxdTBmYWVjOFdOQUxBRzYtMlJIUGt2M2VwNjY4aW9vSG1NU2s4ZGJrQ29MU04xYmR2eUlLYmFlTDBvSkt3SzRBaFZmVzNmQ3ZfNVBFMTVuTHBQSkJWSGxvYzNBakVYTDUzNkt0anN4bzFpdHNhUTlxa2lNUU5YclVIbzM3YUdJZnNuUlI3cUlqcVdsRTNpTDBzbHhVMGxCRC1IZllmNEJTZEpNa1pMZjYtU195eDFkWTh4Y3ZXRm1WTjI4SFJ6S3YxZ3E0S2xPa3IxSDdyR0hKcHlHZyIsIm9hdXRoX3Rva2VuIjoiRUFBQnd6TGl4bmpZQkFMbHBaQ1QweEtzaVJFZmpqRE1LRXN4UG91VnllTXpoUnhpZDBKWkJlblpDUEpXcjhZWU5zdmxScWZDamFtUEZDSldpeVVyUTNGanRRSHprUnBOUmxRejlwZUU3WDJFMXZ5bVUyTVpDWkFsc2cyakRkNElxbFJUb1pDcGd3bW5iYlh6WkJ0enpTRXphTlIwSXVUS2xPRTF2b3hvWkJmSEFjcGhocnhxZ2xsZmZSSk1aQlYwZlpDOFhnWkQiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY4MDM0MTA0OX0; fbsr_124024574287414=G74oNgocuNbj2nyxoWufy7vi5JhOIz2IRTowj5LOiFc.eyJ1c2VyX2lkIjoiMTAwMDE0MjI4OTgzMDMzIiwiY29kZSI6IkFRRGNueTMxSWFnMWhOZEtqR2Jnbk1Ed2NJT24weGhJUHNzVXRWbGJZd2FMZTF1dElEdWF0cUFwTjVjOW9zWGlDMW1fMVBLY1NzQ0VQSlFuVC1uVURvTGFJMi1sSU9xYk5RX3Y2NTBldW5oeV9oZVU0VnFjWElrY3VqSVYtLWx1UUgwd2pjQWdHeTdCUGlySEp6UlJZaU5kVlFxdTBmYWVjOFdOQUxBRzYtMlJIUGt2M2VwNjY4aW9vSG1NU2s4ZGJrQ29MU04xYmR2eUlLYmFlTDBvSkt3SzRBaFZmVzNmQ3ZfNVBFMTVuTHBQSkJWSGxvYzNBakVYTDUzNkt0anN4bzFpdHNhUTlxa2lNUU5YclVIbzM3YUdJZnNuUlI3cUlqcVdsRTNpTDBzbHhVMGxCRC1IZllmNEJTZEpNa1pMZjYtU195eDFkWTh4Y3ZXRm1WTjI4SFJ6S3YxZ3E0S2xPa3IxSDdyR0hKcHlHZyIsIm9hdXRoX3Rva2VuIjoiRUFBQnd6TGl4bmpZQkFMbHBaQ1QweEtzaVJFZmpqRE1LRXN4UG91VnllTXpoUnhpZDBKWkJlblpDUEpXcjhZWU5zdmxScWZDamFtUEZDSldpeVVyUTNGanRRSHprUnBOUmxRejlwZUU3WDJFMXZ5bVUyTVpDWkFsc2cyakRkNElxbFJUb1pDcGd3bW5iYlh6WkJ0enpTRXphTlIwSXVUS2xPRTF2b3hvWkJmSEFjcGhocnhxZ2xsZmZSSk1aQlYwZlpDOFhnWkQiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY4MDM0MTA0OX0; rur="NCG\05458604319986\0541711877078:01f77406d735de6fa360029deedef54ed6187554ba7a57f4ac921d29106480e51bfd3415"',
    "origin": 'https://www.instagram.com',
    "referer" : "https://www.instagram.com/",
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest' : 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
    'viewport-width': '425',
    'x-asbd-id': '198387',
    'x-csrftoken' : 'omem4YL9qqhfhHh8Xz0m7wsgBA4hYxIp',
    'x-ig-app-id': '1217981644879628',
    'x-ig-www-claim': 'hmac.AR2YJUm4-djg30GSAO7GeOXGzk0BpGjoy1p98_o1I58hs-K3',
    'x-instagram-ajax': '1007228779',
    'x-requested-with' : 'XMLHttpRequest',
}

s = requests.Session()
r = s.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', data=data, headers=headers)
print(r.content)

@backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError)
def getJSON(url):
    r = s.get(url)
    return r

@application.route('/', methods = ['POST', 'GET'])
@cross_origin()
def index():

    all_links = []

    if(request.method == 'POST'):

        req = request.json
        download_url = req['url']

        #If link is reel or mobile version
        if 'reel' in download_url:
            download_url = download_url[0:43]
        else:
            download_url = download_url[0:40]

        r = getJSON(download_url + '?__a=1&__d=dis')

        media = r.json()
        mediaArray = []

        try:
            #Checks to see if post is a reel
            responseImg = requests.get(media['items'][0]['image_versions2']['candidates'][0]['url'])
            responseVid = requests.get(media['items'][0]['video_versions'][0]['url'])
            all_links.append({'url': media['items'][0]['video_versions'][0]['url'], 'base64': "data:" + responseImg.headers['Content-Type'] + ";" + "base64," + base64.b64encode(responseImg.content).decode("utf-8"), 'base64Vid': "data:" + responseVid.headers['Content-Type'] + ";" + "base64," + base64.b64encode(responseVid.content).decode("utf-8")})
        except:
            mediaArray = media['items'][0]

        if len(mediaArray):
            try:
                for items in mediaArray['carousel_media']:  
                    response = requests.get(items['image_versions2']['candidates'][0]['url'])
                    try:
                        #Checks to see if carousel media is a video
                        all_links.append({'url': items['video_versions'][0]['url'], 'base64': "data:" + response.headers['Content-Type'] + ";" + "base64," + base64.b64encode(response.content).decode("utf-8")})
                    except:
                        #If not video, carousel media is an image
                        all_links.append({'url': items['image_versions2']['candidates'][0]['url'], 'base64' : "data:" + response.headers['Content-Type'] + ";" + "base64," + base64.b64encode(response.content).decode("utf-8")})
            except:
                #If the post is only a single image
                response = requests.get(mediaArray['image_versions2']['candidates'][0]['url'])
                all_links.append({'url': mediaArray['image_versions2']['candidates'][0]['url'], 'base64': "data:" + response.headers['Content-Type'] + ";" + "base64," + base64.b64encode(response.content).decode("utf-8")})
        
        return {'links' : all_links}
    
    else:
        return {'links' : all_links}

if __name__ == "__main__":
    application.run()