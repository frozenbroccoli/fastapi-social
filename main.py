from random import randrange
from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = []


def find_post(post_id):
    for post in my_posts:
        if post_id == post["id"]:
            return post
        return {"message": "This post does not exist."}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": "These are your posts."}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = find_post(post_id)
    return {**post}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {**post_dict}
