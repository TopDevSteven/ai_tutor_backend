import asyncio
import logging
import os
import json
import gzip
import uuid

from dotenv import load_dotenv
from quart import Quart, jsonify, request, Response, make_response, session
from quart.helpers import stream_with_context

from log import init_logging

load_dotenv()
init_logging()
logger = logging.getLogger(__name__)

app = Quart(__name__)
app.secret_key = os.getenv("SECRET_KEY")

from datetime import date

import openai

from util.utils import get_prompt

new_prompt_dict = {}  # Global dictionary to store new_prompt values

@app.before_serving
async def startup():
    loop = asyncio.get_event_loop()
    await openai.create_session(loop)


@app.after_serving
async def shutdown():
    await openai.teardown()


# For healthchecks
@app.route("/")
def index():
    return "ok"

@app.route("/lesson_style/", methods=["POST"])
async def set_prompt_to_session():
    body = await request.get_json()

    new_prompt = get_prompt(
        body['depth'], 
        body['learning_style'],
        body['communication_style'],
        body['tone_style'],
        body['reasoning_framework']
    )

    user_id = str(uuid.uuid4())

    new_prompt_dict[user_id] = new_prompt  # Store new_prompt in the global dictionary

    response = await make_response(jsonify({ "message": "success" }))
    response.set_cookie("user_id", user_id)

    return response


@app.route("/query/", methods=["POST"])
async def get_response_stream():
    body = await request.get_json()
    
    messages = body["messages"]

    user_id = request.cookies.get("user_id")

    if not user_id:
        return jsonify({ "message": "can't find user_id" })

    new_prompt = new_prompt_dict.get(user_id)  # Retrieve the new_prompt from the global dictionary

    if new_prompt is None:
        # Handle the case when new_prompt is not found
        return jsonify({ "error": "new_prompt not found for this session" })

    messages = [{'role': 'user', 'content': new_prompt}, *messages]

    model = "gpt-4"
    temperature = 0.2

    response = await make_response(openai.get_chat_completion_stream(
        messages, 
        model,
        temperature
    ))
    
    response.timeout = None  # No timeout for this route

    return response
