import logging
import os
import time
import json
import aiohttp

logger = logging.getLogger(__name__)

api_root = os.getenv("OPENAI_API_ROOT")
logger.info(f"OpenAI API URL: {api_root}")

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY"),
}


async def create_session(loop):
    global session
    session = aiohttp.ClientSession(loop=loop)
    return session


async def teardown():
    await session.close()


async def get_chat_completion_stream(messages, model, temperature=0.2):
    time.sleep(0.4)
    body = {
        "messages": messages,
        "model": model,
        "temperature": temperature,
        "stream": True
    }
    async with session.post(
        f"{api_root}/chat/completions",
        headers=headers,
        data=json.dumps(body),
    ) as resp:
        while True:
            line = await resp.content.readline()
            print(line)
            if not line:
                break
            line_str = line.decode('utf-8').strip()
            if line_str == '':
                continue
            if line_str == 'data: [DONE]':
                continue
            if not line_str.startswith('data: '):
                continue
            json_line = json.loads(line_str[6:])  # slicing "data: " off
            yield json.dumps(json_line)

