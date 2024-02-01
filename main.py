from fastapi import FastAPI, Response, status
from models import studentSchema,booksSchema
from bson.objectid import ObjectId
from fastapi.responses import HTMLResponse

from dbConnection import database

app = FastAPI()

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)

@app.get("/students")
async def get_all_student_details():
    result = database['students'].find()
    students_list = []

    for document in await result.to_list(length=100):
        students_list.append(str(document))
    return {"succcess" : True,"students" : students_list}



@app.post("/students")
async def create_students_data(req:studentSchema.Student):
    student = { "name" : req.name,
                "class_name" : req.class_name,
                "section" : req.section,
                "is_member" : req.is_member,
                "books_issued" : req.books_issued
            }
    
    result = await database["students"].insert_one(student)

    return {"success":True,"id":str(result.inserted_id)}



@app.post("/books")
async def create_books_data(req:booksSchema.Book):
    book = { "title" : req.title,
                "price" : req.price,
                "is_in_circulation" : req.is_in_circulation,
                "is_issued" : req.is_issued
            }
    
    result = await database["books"].insert_one(book)

    return {"success":True,"id":str(result.inserted_id)}



@app.get("/books/{book_id}")
async def get_book_details(book_id:str):
    result = await database['books'].find_one({"_id":ObjectId(book_id)})
    print(result,book_id)

    return {"success":True,"book_details":str(result)}



@app.put("/student/{student_id}")
async def add_book_to_student(book_name,student_id:str,response:Response):

    book = await database['books'].find_one({"title":book_name})
    student = await database['students'].find_one({"_id":ObjectId(student_id)})

    print(student)

    if(book):
        if(book["is_in_circulation"]):
            if(book["is_issued"]):
                return {"success":False,"message":"the book is already issued"}
            else:
                if(student):
                    if(student["is_member"]):
                        await database['students'].update_one({"_id":ObjectId(student_id)},{"$push":{"books_issued":ObjectId(book["_id"])}})
                        await database["books"].update_one({"_id":ObjectId(book["_id"])},{"$set":{"is_issued":True}})
                    else:
                        {"success":False,"message":f"the student {student['_id']} is not a member"}
                else:
                    response.status_code = status.HTTP_204_NO_CONTENT
                    return {"success":False,"message":"no such student present"}
        else:
            return {"success":False,"message":"the book is not in circulation"}
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"success":False,"message":"no book found with this name"}

    return {"success":True,"message":"book issued successfully"}
