from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.get("/")
def name():
    return {"data": {"name": "Avijit"}}


@app.get("/blog")
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f"You have only {limit} published blogs"}
    else:
        return {"data": f"You have only {limit} unpublished blogs"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "All unpublished"}


@app.get("/blog/{id}")
def show(id: int):
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id, limit=10):
    return {"data": {"a", "b"}}


@app.get("/about")
def about():
    return {"data": "about page"}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post("/blog")
def create_blog(blog: Blog):
    return {"data": f"Blog is {blog.title}"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)
