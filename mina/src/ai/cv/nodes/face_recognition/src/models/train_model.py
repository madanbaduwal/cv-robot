import glob
import os
import sys
import requests
from loguru import logger
import datetime
import requests
from urllib.parse import urlparse
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person


KEY = "d1c82aaaf4f145c39e4397ec83602c7e"
ENDPOINT = "https://madan.cognitiveservices.azure.com/"
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
logger.info(f"Set  endpoint :{ENDPOINT}, key : *** and face_client object")
name_person_id = {}

def create_persogroup(personal_group_id):

    '''Create the PersonGroup
    Args:
        persongroup_name(str) : persongroup_name
    '''    
    global PERSON_GROUP_ID 
    PERSON_GROUP_ID = personal_group_id
    logger.info(f"set global PERSON_GROUP_ID : {PERSON_GROUP_ID}")
    face_client.person_group.create(person_group_id = PERSON_GROUP_ID, name = PERSON_GROUP_ID)
    logger.info(f"PERSON_GROUP_ID : {PERSON_GROUP_ID} is created")

def person_group_list():

    url = "https://madan.cognitiveservices.azure.com/face/v1.0/persongroups"
    headers = {"Ocp-Apim-Subscription-Key" : "d1c82aaaf4f145c39e4397ec83602c7e"}
    req = requests.get(url, headers=headers)
    print(req.json())


def add_new_person(PERSON_GROUP_ID, person_name):
    '''Training a person images.
    Args:
        person_name(str) : Name of the person.
        folder_name(str) : Image folder of the person.
    '''
    folder_name = person_name # note we save the name of folder as a person name
    person = face_client.person_group_person.create(PERSON_GROUP_ID, name = person_name) 
    person_images = [file for file in glob.glob(f'../../data/raw/{folder_name}/*.jpg')] 
    print(person_images)
    logger.info(f"Load images path from folder:{person_images}")
    for image in person_images:
        image  = open(image, 'r+b')
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, person.person_id, image) 
    logger.info(f"Local directory images are added into the face api server")
    logger.info(f"Now Person group id {PERSON_GROUP_ID}")
    start_training_time = datetime.datetime.now()
    face_client.person_group.train(PERSON_GROUP_ID)
    end_training_time = datetime.datetime.now()
    logger.info(f"Time required for training is : {end_training_time - start_training_time}")

    while (True):
        training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
        logger.info(f"Training ststus is:{training_status.status}")
        if (training_status.status is TrainingStatusType.succeeded):
            logger.info(f"Training status is:succeeded")
            break
        elif (training_status.status is TrainingStatusType.failed):
            logger.info(f"Training status is:failed")
            face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
            sys.exit('Training the person group has failed.')
        time.sleep(5)

def person_group_person_list(person_group):
    url = f"https://madan.cognitiveservices.azure.com/face/v1.0/persongroups/{person_group}/persons"
    headers = {"Ocp-Apim-Subscription-Key" : "d1c82aaaf4f145c39e4397ec83602c7e"}
    req = requests.get(url, headers=headers)
    print(req.json())

def delete_person_group(PERSON_GROUP_ID):
    face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
    print("Deleted the person group {} from the source location.".format(PERSON_GROUP_ID))
    print()
    # url = "https://madan.cognitiveservices.azure.com/face/v1.0/persongroups/{personGroupId}"
    # headers = {"Ocp-Apim-Subscription-Key" : "d1c82aaaf4f145c39e4397ec83602c7e"}
    # requests.delete(url, headers=headers)
    
# We can also delete person group person

if __name__=='__main__':

    if sys.argv[1]=="pg":
        create_persogroup(sys.argv[2])

    elif sys.argv[1]=="pgl":
        person_group_list()

    elif sys.argv[1]=="adp":
        add_new_person(sys.argv[2], sys.argv[3]) # PERSON_GROUP_ID, person_name
    
    elif sys.argv[1]=="pgpl":
        person_group_person_list(sys.argv[2])
    
    elif sys.argv[1]=="delpg":
        delete_person_group(sys.argv[2])