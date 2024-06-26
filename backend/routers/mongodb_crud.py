import json
import logging
import os
from typing import Union, Annotated

import certifi
import pymongo
from fastapi import APIRouter, status
from fastapi import Form, Header
from starlette.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
client = pymongo.MongoClient(os.environ.get('MONGO_URI'), ssl=True, tlsCAFile=certifi.where())

db = client["nutrition_ai"]
collection = db["nutrition_user"]

def verify_data(data: str) -> bool:
    """
    Verify presence of fields in data and its type
    Sample data
        {
      "name": "John Doe",
      "age": 25,
      "gender": "male", //male, female, other
      "height": 5.8, //in feet
      "weight": 150, //in lbs
      "activity_level": "moderate", //sedentary, light, moderate, active, very_active
      "exercise_hours": 3, //in hours
      "job_type": "student", //student, working
      "work_type": "office", //office, field, home, None
      "work_hours": 40,
      "cooking_hours": 5,
      "proficiency_in_cooking": "medium", //low, medium, high
      "goals": "healthy", //healthy, weight_loss, muscle_gain
      "dietary_restrictions": null, //None, vegetarian, vegan, gluten_free, dairy_free, nut_free
      "diet_type": "balanced", //balanced, keto, paleo, vegan, vegetarian
      "allergies": null, //None, peanuts, shellfish, soy, dairy, eggs, gluten
      "cuisine_preference": "indian", //american, italian, mexican, chinese, indian, thai, japanese
      "budget": 100, //0-100 dollars for weekly groceries
      "grocery_frequency": "weekly", //weekly, bi-weekly, monthly
    }
    :param data:
    :return: bool
    """
    try:
        data = json.loads(data)
        if "name" in data and "age" in data and "gender" in data and "height" in data and "weight" in data and "activity_level" in data and "exercise_hours" in data and "job_type" in data and "work_type" in data and "work_hours" in data and "cooking_hours" in data and "proficiency_in_cooking" in data and "goals" in data and "dietary_restrictions" in data and "diet_type" in data and "allergies" in data and "cuisine_preference" in data and "budget" in data and "grocery_frequency" in data:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error in verifying data: {str(e)}")
        return False




@router.post("/write_user_info_to_mongo", tags=["mongo_db"])
async def write_user_info_to_mongo(email_id: Annotated[Union[str, None], Header()],
                                   data: str = Form(...)) -> JSONResponse:
    """
       Writes data to mongo db
       :param email_id:
       :param data:
       :return:
    """
    if verify_data(data):

        try:
            logger.info(f"Data received for writing to mongo db")
            if email_id in collection.distinct("email_id"):
                collection.update_one({"email_id": email_id}, {"$set": {"data": data}})
            else:
                collection.insert_one({"email_id": email_id, "data": data})
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data written to mongo db"})
        except Exception as e:
            logger.error(f"Error in writing data to mongo db: {str(e)}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content={"message": "Internal server error"})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Invalid data"})


@router.post("/read_user_info_from_mongo", tags=["mongo_db"])
async def read_user_info_from_mongo(email_id: Annotated[Union[str, None], Header()]) -> JSONResponse:
    """
    Reads data from mongo db
    :param email_id:
    :return:
    """
    try:
        logger.info(f"Data received for reading from mongo db")
        if email_id in collection.distinct("email_id"):
            data = collection.find_one({"email_id": email_id}, {"_id": 0})
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data fetched from mongo db",
                                                                         "data": data})
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No data found in mongo db"})
    except Exception as e:
        logger.error(f"Error in reading data from mongo db: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "Internal server error"})


@router.post("/get_all_chats", tags=["mongo_db"])
async def get_all_chats(email_id: Annotated[Union[str, None], Header()]) -> JSONResponse:
    """
    Reads data from mongo db
    :param email_id:
    :return:
    """
    try:
        logger.info(f"Data received for reading from mongo db")
        collection_chat = db['chat_data']
        if email_id in collection_chat.distinct("email_id"):
            data = collection_chat.find({"email_id": email_id}, {"_id": 0})
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Data fetched from mongo db",
                                                                         "data": data})
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No data found in mongo db"})
    except Exception as e:
        logger.error(f"Error in reading data from mongo db: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message": "Internal server error"})


# @router.post("/get_all_emails", tags=["mongo_db"])
# async def get_all_emails() -> JSONResponse:
#     """
#     Reads data from mongo db
#     :return:
#     """
#     try:
#         logger.info(f"Data received for reading from mongo db")
#         data = collection.find({}, {"email_id": 1, "_id": 0})
#         if data:
#             return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Emails fetched from mongo db",
#                                                                          "data": json.dumps(data)})
#         else:
#             return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No data found in mongo db"})
#     except Exception as e:
#         logger.error(f"Error in reading data from mongo db: {str(e)}")
#         return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             content={"message": "Internal server error"})
