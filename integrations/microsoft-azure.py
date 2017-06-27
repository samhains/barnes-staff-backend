import time 
import json
import os
import requests
import operator
import numpy as np
# Import library to display results
import matplotlib.pyplot as plt
# Variables

_url = 'https://eastus2.api.cognitive.microsoft.com/vision/v1.0/analyze'
_key = '6a239c99a5b74c33a5579b5c3e6276b7'
_dirname = './barnes-image-original'
_dirname_cropped = './barnes-images-cropped'
_maxNumRetries = 10

def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json()['error']['message'] ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )

        break
        
    return result

def analyse_image(url):
    pathToFileInDisk = url

    with open( pathToFileInDisk, 'rb' ) as f:
        data = f.read()

    # Computer Vision parameters
    params = { 'visualFeatures' : 'Tags,Description,Categories,Faces'} 

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'

    json = None

    result = processRequest( json, data, headers, params )
    return result


filenames = [os.path.join(_dirname, fname)
             for fname in os.listdir(_dirname) if fname.endswith('.jpg')]

filenames_cropped = [os.path.join(_dirname_cropped, fname)
             for fname in os.listdir(_dirname_cropped) if fname.endswith('.jpg')]


i = 0
# data = {}
with open('./result.json') as data_file:    
    data = json.load(data_file)

for filename in filenames:
    i = i + 1
    img_id = filename.split('/')[-1].split('_')[0]
    print(img_id)
    if img_id not in data.keys():
        statinfo = os.stat(filename)
        file_size = float(statinfo.st_size)
        for j in range(2):
            file_size = file_size / 1024
        if file_size > 4:
            print('swapping out:', filename)
            filenames = [filename for filename in filenames_cropped if filename.split('/')[-1].startswith(img_id)]
            filename = filenames[0]
            print('for:', filename)

        result = analyse_image(filename)
        data[img_id] = { "result": result, "url": filename }
        print(result['tags'])
        # if (i % 50 == 0):
        with open('result.json', 'w') as fp:
            json.dump(data, fp)


with open('microsoft-azure-results.json', 'w') as fp:
    print('final saving')
    json.dump(data, fp)

#analyse_image("./5330_2de9b175db4b1580_b.jpg")
