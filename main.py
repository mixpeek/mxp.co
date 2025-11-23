import os
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from starlette.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set")
client = MongoClient(MONGO_URI)
db = client["mxp"]
redirects_collection = db["redirects"]

BASE_URL = "https://mixpeek.com/"


@app.get("/{path}")
def redirect_to_mp_apps(path: str):
    # Check if the path exists in the apps collection
    redirect = redirects_collection.find_one({"slug": path})
    if redirect:
        target_url = redirect["target"]
        return RedirectResponse(url=target_url)
    else:
        return RedirectResponse(url="https://mixpeek.com/404")


@app.get("/")
def redirect_to_mp_apps():
    return RedirectResponse(url="https://mixpeek.com")
