from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": "These are your posts."}


@app.post("/createposts")
def create_posts(post: Post):
    return {"message": "Successfully created posts.", "post": post}
