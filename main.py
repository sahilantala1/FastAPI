# main.py
from typing import List
from fastapi import HTTPException
from fastapi import FastAPI,status

import schemas
from database import database
from models import Blog
from schemas import BlogCreate, BlogOut

app = FastAPI()

@app.on_event("startup")
async def startup():
    print("Connecting to PostgreSQL...")
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    print("Disconnecting from PostgreSQL...")
    await database.disconnect()

@app.post("/blogs")
async def create_blog(blog: BlogCreate):
    print(f"Received blog: {blog}")
    query = Blog.__table__.insert().values(title=blog.title, content=blog.content)
    last_record_id = await database.execute(query)
    print(f"Inserted blog ID: {last_record_id}")
    return {**blog.dict(), "id": last_record_id}

@app.get("/blogs", response_model=List[BlogOut])
async def get_blogs():
    query = Blog.__table__.select()
    results = await database.fetch_all(query)
    return results

@app.get("/blogs", response_model=List[BlogOut])
async def get_blogs():
    query = Blog.__table__.select()
    results = await database.fetch_all(query)
    return results

@app.get("/blogs/{id}", response_model=BlogOut)
async def get_blog_by_id(id: int):
    query = Blog.__table__.select().where(Blog.id == id)
    blog = await database.fetch_one(query)

    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog

@app.delete("/blogs/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: int):
    query = Blog.__table__.delete().where(Blog.id == id)
    result = await database.execute(query)

    if result == 0:
        raise HTTPException(status_code=404, detail="Blog not found")

    return {"message": f"Blog with ID {id} deleted successfully"}


@app.put("/blogs/{id}", response_model=BlogOut)
async def update_blog(id: int, blog: BlogCreate):
    # 1. Check if blog exists
    select_query = Blog.__table__.select().where(Blog.id == id)
    existing_blog = await database.fetch_one(select_query)

    if not existing_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # 2. Update the blog
    update_query = (
        Blog.__table__
        .update()
        .where(Blog.id == id)
        .values(title=blog.title, content=blog.content)
    )
    await database.execute(update_query)

    # 3. Fetch updated data using a fresh select query
    new_select_query = Blog.__table__.select().where(Blog.id == id)
    updated_blog = await database.fetch_one(new_select_query)

    if not updated_blog:
        raise HTTPException(status_code=500, detail="Failed to fetch updated blog")

    return updated_blog

@app.post('/user')
def create_user(req: schemas.User):
    return f'Created user with id {req.name}'



# ==== DATABASE =====
# @app.post('/blog')
# def create(req : schemas.Blog ):
#     return f'{req.title}'

# @app.get('/about/{id}')
# def index(id: int):
#     return {'data': id}
#
# @app.get('/about')
# def about():
#     return {'data': {"info": "about ds this page"}}
#
# @app.get('/blog')
# def blog(limit: int):
#     return {'message': f'{limit} blogs'}
#
# class Blog(BaseModel):
#     title: Optional[str] = None
#     content: Optional[str] = None
#
# @app.post('/show_blog')
# def cr_blog(req: Blog):
#     return {'message': 'blog created', 'title': req.title}