from random import randrange
from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
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
    for index, post in enumerate(my_posts):
        if post_id == post["id"]:
            return index, post
    return None, None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"posts": my_posts}


@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):
    _, post = find_post(post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A post with post_id: {post_id} does not exist.",
        )

    return {**post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {**post_dict}


@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id: int, response: Response):
    index, post = find_post(post_id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A post with post_id: {post_id} does not exist.",
        )

    my_posts.pop(index)
    return {"message": "This post has been successfully deleted.", **post}
