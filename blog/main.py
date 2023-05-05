from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from . import models
from .hashing import Hash
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

from passlib.context import CryptContext

app = FastAPI()


models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(req: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req.title, body=req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def destory(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not available yet",
        )
    blog.delete(synchronize_session=False)
    db.commit()

    return {"detail": f"The blog with id {id} is destroyed"}


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id, req: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not available yet",
        )

    blog.update({"title": req.title, "body": req.body}, synchronize_session=False)

    db.commit()
    return f"Blog with id {id} is updated"


@app.get("/blog", response_model=List[schemas.ShowBlog], tags=["blogs"])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=200, response_model=schemas.ShowBlog, tags=["blogs"])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not available",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} is not available"}

    return blog


# PassWord hashing using passlib
# pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/user", response_model=schemas.ShowUser, tags=["users"])
def create_user(req: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=req.name, email=req.email, password=Hash.bcrypt(req.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/user/{id}", response_model=schemas.ShowUser, tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} is not available",
        )
    return user
