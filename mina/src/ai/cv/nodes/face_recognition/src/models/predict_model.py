import glob
from azure.cognitiveservices.vision.face import FaceClient
import os
from msrest.authentication import CognitiveServicesCredentials
import time
import  sys
import requests
import datetime
from loguru import logger



KEY = "d1c82aaaf4f145c39e4397ec83602c7e"
ENDPOINT = "https://madan.cognitiveservices.azure.com/"
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
# Request headers set Subscription key which provides access to this API. Found in your Cognitive Services accounts.
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'd1c82aaaf4f145c39e4397ec83602c7e',
}



def prediction1(PERSON_GROUP_ID,test_image_path):

    body = dict()
    body["url"] = test_image_path
    body = str(body)

    # Request URL 
    FaceApiDetect = f'{ENDPOINT}/face/v1.0/detect?returnFaceId=true' 

    try:
        # REST Call 
        response = requests.post(FaceApiDetect, data=body, headers=headers) 
        responseJson = response.json()
        faceId = responseJson[0]["faceId"]
        print("FACE ID: "+str(faceId))

    except Exception as e:
        print(e)


    faceIdsList = [faceId]
    # Request Body
    body = dict()
    body["personGroupId"] = PERSON_GROUP_ID
    body["faceIds"] = faceIdsList
    body["maxNumOfCandidatesReturned"] = 1 
    body["confidenceThreshold"] = 0.5
    body = str(body)

    # Request URL 
    FaceApiIdentify = f'{ENDPOINT}/face/v1.0/identify' 

    try:
        # REST Call 
        response = requests.post(FaceApiIdentify, data=body, headers=headers) 
        responseJson = response.json()
        personId = responseJson[0]["candidates"][0]["personId"]
        confidence = responseJson[0]["candidates"][0]["confidence"]
        print("PERSON ID: "+str(personId)+ ", CONFIDENCE :"+str(confidence))
            
    except Exception as e:
        print("Could not detect")
    
    # Request URL 
    FaceApiGetPerson = f"{ENDPOINT}/face/v1.0/persongroups/{PERSON_GROUP_ID}/persons/{personId}"

    try:
        response = requests.get(FaceApiGetPerson, headers=headers) 
        responseJson = response.json()
        print("This Is "+str(responseJson["name"]))
        
    except Exception as e:
        print(e)
    return responseJson["name"]

def prediction(PERSON_GROUP_ID,test_image_path):

    logger.info(f'Prediction starting')
    test_image_array = glob.glob(f'../../data/raw/{test_image_path}/*.jpg')
    logger.info(f"test image path is {test_image_array}")
    image = open(test_image_array[0], 'r+b')
    logger.info(f'Pausing for 10 seconds to avoid triggering rate limit on free account...')
    time.sleep (10)
    # Detect faces
    face_ids = []
    # We use detection model 3 to get better performance.
    logger.info("Faces are detection")
    faces = face_client.face.detect_with_stream(image, detection_model='detection_03')
    logger.info("face detection completed")
    for face in faces:
        face_ids.append(face.face_id)
    # Identify faces
    start_training_time = datetime.datetime.now()
    results = face_client.face.identify(face_ids, PERSON_GROUP_ID) 
    print("Identified result is :",results)
    end_training_time = datetime.datetime.now()
    logger.info(f"Time required for training is : {end_training_time - start_training_time}")
    if not results:
        print('No person identified in the person group for faces from {}.'.format(os.path.basename(image.name)))
    for person in results:
        if len(person.candidates) > 0:
            print("person:",person)
            print("Person candidate",person.candidates)
            print('Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id, os.path.basename(image.name), person.candidates[0].confidence)) # Get topmost confidence score
            #{Endpoint}/face/v1.0/persongroups/{personGroupId}/persons/{personId}
            print(PERSON_GROUP_ID)
            print(person.face_id)
            faceIdsList = [person.face_id]

            # Request Body
            logger.info("Try to find out the personid")
            body = dict()
            body["personGroupId"] = PERSON_GROUP_ID
            body["faceIds"] = person.face_id
            body["maxNumOfCandidatesReturned"] = 1 
            body["confidenceThreshold"] = 0.5
            body = str(body)

            # Request URL 
            FaceApiIdentify = '{ENDPOINT}/face/v1.0/identify' 

            try:
                # REST Call 
                response = requests.post(FaceApiIdentify, data=body, headers=headers) 
                print("Response  is:",response)
                responseJson = response.json()
                logger.info(f"response is :{responseJson} ")
                personId = responseJson[0]["candidates"][0]["personId"]
                confidence = responseJson[0]["candidates"][0]["confidence"]
                print("PERSON ID: "+str(personId)+ ", CONFIDENCE :"+str(confidence))
                   
            except Exception as e:
                print("Could not detect")

            # Request URL 
            FaceApiGetPerson = f'{ENDPOINT}/face/v1.0/persongroups/{PERSON_GROUP_ID}/persons/{personId}'

            try:
                response = requests.get(FaceApiGetPerson, headers=headers) 
                responseJson = response.json()
                print("This Is "+str(responseJson["name"]))
                
            except Exception as e:
                print(e)
            # url = f"https://madan.cognitiveservices.azure.com/face/v1.0/persongroups/{PERSON_GROUP_ID}/persons/{person.face_id}"
            # headers = {"Ocp-Apim-Subscription-Key" : "d1c82aaaf4f145c39e4397ec83602c7e"}
            # req = requests.get(url, headers=headers)
            # print(req.json())
        else:
            print('No person identified for face ID {} in {}.'.format(person.face_id, os.path.basename(image.name)))
    
if __name__=='__main__':

    if sys.argv[1]=="pre":
        prediction1(sys.argv[2],sys.argv[3])