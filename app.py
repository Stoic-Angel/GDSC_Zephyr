from fastapi import FastAPI, responses, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import redis

from request_parser.chat_schemas import QuestionModel
from settings import Settings
import json
from datetime import datetime, UTC

import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.DEBUG, force=True)
logger = logging.getLogger("uvicorn")

file_handler = RotatingFileHandler("app.log", maxBytes=5 * 1024 * 1024, backupCount=3)
logger.addHandler(file_handler)

log_format = "%(asctime)s - %(levelname)s - %(message)s"
for handler in logger.handlers:
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(log_format))

logger.setLevel(logging.DEBUG)

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

app = FastAPI(title=f"{Settings.PROJECT_NAME} API",
              version=Settings.PROJECT_VERSION)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_api_key(authorization: str = Header(...)):
    expected_key = Settings.SECRET_KEY
    if authorization != f"Bearer {expected_key}":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return authorization


from google import genai
from google.genai import types
from google.api_core.exceptions import ResourceExhausted

client = genai.Client()
model = 'models/gemini-1.5-flash-001'
cache = None
TTL = 3559

async def create_cache():
    global cache  # Access the global cache variable
    
    # Read the content from the file
    with open('zephyr.txt', 'r') as f:
        file_content = f.read()
    
    # Create a cache with a 5 minute TTL, embedding file content in system_instruction
    cache = client.caches.create(
        model=model,
        config=types.CreateCachedContentConfig(
            display_name='GDG OnCampus Zephyr',  # used to identify the cache
            system_instruction=(
                "You are a virtual AI assistance named Zephyr (exclusive to GDG OnCampus (previously GDSC) JSSATEN ) whose job is to clear the doubts of students related to  GDG OnCampus (previously GDSC) JSSATEN club. AVOID any political or controversial topic.\
  YOU CAN answer questions that are not about GDG OnCampus or its members with your general knowledge. YOU MUST KEEP YOUR ANSWER SHORT. Dont give links unless specifically asked for. \
  If you are not able to answer query using the context, just reply 'Sorry, I didn't get that. You can try contacting GDG OnCampus members directly from https://www.instagram.com/gdgoncampus.jss/' \
  This is the data related to GDG OnCampus and you should use this for context regarding the society, the people, the process for recruitment and everything."
             + file_content  # Add the file content here
            ),
            ttl=f"{TTL}s",  # 5 minutes TTL
        )
    )


async def refresh_cache():
    global cache
    try:
        cache_info = client.caches.get(name=cache.name)
        return
    except Exception as e:
        # If the cache is not found (expired), create a new one
        logger.debug(f"Cache expired or not found. Creating a new cache... Error: {e}")
        await create_cache()
        logger.debug("New cache created.")



from uuid import uuid4
import json
from fastapi import Response

@app.get("/create_chat")
async def create_chat(_: str = Depends(get_api_key)):
    session = uuid4()
    chat = []
    redis_client.setex(str(session), 43200, json.dumps(chat))  # Expire in 12 hours
    logger.debug(f"Session created sucessfully for ID: {session} at time: {datetime.now(UTC)}")

    return { "session_id": session }, 200


@app.post("/chat")
async def handle_chat(question_model: QuestionModel):
    question = question_model.question
    session = question_model.session_id

    try:
        logger.debug("Fetching Session")
        chat = json.loads(redis_client.get(session))
        logger.debug(f"Session fetched successfully for ID: {session} and data: {chat}")
    except Exception as e:
        logger.debug(f"Error fetching session for ID: {session} due to {e}")
        return {"error": "No session found"}, 500
    
    chat.append({"role": "user", "content": question})
    logger.debug(f"Requesting response for messages: {chat}")
    
    try:
        await refresh_cache() # Refresh cache if expired

        response = client.models.generate_content(
            model = model,
            contents = json.dumps(chat),
            config = types.GenerateContentConfig(
                cached_content=cache.name,
                temperature=0.2,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
            )
        )

        resp = response.text
        chat.append({"role": "assistant", "content": str(resp)})
        redis_client.setex(session, 43200, json.dumps(chat))
        logger.debug(f"Returning LLM response: {resp}")

        return {"answer": resp}, 200
    
    except ResourceExhausted:  # Catch token limit error
        raise HTTPException(status_code=503, detail="Our servers are full. Please try again later.")
    except Exception as e:
        return {"error": str(e)}, 500


@app.get("/")
async def root():
    return {"message": "Welcome to Zephyr!"}
