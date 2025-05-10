from pydantic import BaseModel  # establece el estilo del post
from fastapi import FastAPI, HTTPException  # crea la api
from typing import Text, Optional   # crea el tipo de archivo Text
from datetime import datetime  # importar fecha
from uuid import uuid4 as uuid  # crear ids unicas

app = FastAPI()

posts = []


# post model
class Post(BaseModel):
    id: Optional[str]=None
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]=None
    published: bool = False


@app.get("/")
def read_root():
    return {"Welcome": "Dragon's REST API"}


@app.get("/posts")
def get_posts():
    return posts


@app.post('/posts')
def save_post(post: Post):
    post.id = str(uuid())
    posts.append(post.model_dump())
    return posts[-1]


@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=404, detail='Post Not Found')

@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail='Post Not Found')

@app.put("/posts/{post_id}")
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]['title'] = updatedPost.title
            posts[index]['content'] = updatedPost.content
            posts[index]['author'] = updatedPost.author
            return {"message": "Post updated successfully"}
    raise HTTPException(status_code=404, detail='Post Not Found')