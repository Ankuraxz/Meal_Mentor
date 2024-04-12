import logging
import json
import os
import requests
import certifi

from fastapi import APIRouter, Form, HTTPException, Header
from typing import Optional, Annotated, Union

from langchain.prompts import PromptTemplate
from langchain.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.llms import OpenAIChat
from langchain.chains import LLMChain



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dalle_llm = OpenAIChat(temperature=0.9,model="gpt-3.5-turbo-0125")

router = APIRouter()

@router.post("/dish_image", tags=["image_ai"])
def generate_image(dish_name:str):
    """
    Generate image of the dish
    :param dish_name:
    :return:
    """
    try:
        image_type = "realistic"
        template = """ Context: You are an AI bot responsible for Image generation of dishes. 
            TASK: You are given a dish {dish_name}. Please generate a Prompt to generate {image_type}, well-plated, mouth-watering and tempting image for the dish to display the serving suggestions.
            Answer: Provide the Prompt 
            """
        prompt = PromptTemplate.from_template(template)
        chain = LLMChain(prompt=prompt, llm=dalle_llm)
        image_url = DallEAPIWrapper().run(chain.run({'dish_name': dish_name, 'image_type': image_type}))
        logger.info(f"Image generated successfully")
        return {"image_url": image_url}

    except Exception as e:
        logger.error(f"Error in generating image: {str(e)}")
        raise HTTPException(status_code=500, detail="Error in generating image")