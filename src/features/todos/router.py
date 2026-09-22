from fastapi import APIRouter, HTTPException
from src.features.todos.schemas import TodoCreate, TodoResponse


router = APIRouter(prefix="/todos", tags=["todos"])


fake_todos_db: list[TodoResponse] = []
next_id = 1





@router.post("/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate):
    global next_id
    new_todo = TodoResponse(id=next_id, **todo.model_dump())
    fake_todos_db.append(new_todo)
    next_id = next_id+1
    return new_todo





@router.get("/", response_model=list[TodoResponse])
async def get_todos():
    return fake_todos_db





@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int):
    for item in fake_todos_db:
        if item.id == todo_id:
            return item
    raise HTTPException(status_code=404, detail="Todo Not found")





@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, updated_todo: TodoCreate):
    for index, todo in enumerate(fake_todos_db):
        if todo.id == todo_id:
            fake_todos_db[index] = TodoResponse(id= todo.id, **updated_todo.model_dump())
            return fake_todos_db[index]
    raise HTTPException(status_code=404, detail="Todo Not found")





@router.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    for index, todo in enumerate(fake_todos_db):
        if todo.id == todo_id:
            fake_todos_db.pop(index)
            return  {"message":"Todo deleted successfully!"}
    raise HTTPException(status_code=404, detail="Todo Not found")







"""
## লাইনগুলো কেন এভাবে
- **`APIRouter(prefix="/todos", ...)`**: এই `router`-এর সব `endpoint`-এর সামনে `/todos` বসবে। তাই নিচে `"/"` লিখলেও আসল `path` হবে `/todos/`। `tags=["todos"]` শুধু `/docs` page-এ সুন্দর group করে দেখানোর জন্য।
- **`fake_todos_db: list[TodoResponse] = []`**: আসল database-এর বদলি, memory-তে data রাখছে। Server বন্ধ হলে data হারিয়ে যাবে, এটা স্বাভাবিক এই পর্যায়ে।
- **`todo: TodoCreate`**: FastAPI নিজে `request body`-কে `TodoCreate`-এ পরিণত (`validate`) করে দেয়। ভুল type দিলে user নিজেই `422 error` পাবে, আমাদের কিছু লিখতে হয় না।
- **`response_model=TodoResponse`**: FastAPI-কে বলছি reply এই shape-এ পাঠাতে, আর `/docs`-এ ঠিক `schema` দেখাতে (আগে test project-এ যে `null` দেখেছিলেন, সেটা এখানে ঠিক হয়ে যাবে)।
- **`todo.model_dump()`**: `TodoCreate` object-কে plain `dict`-এ ভাঙে, যাতে `id` যোগ করে নতুন `TodoResponse` বানানো যায়।
- **`global next_id`**: `function`-এর ভেতর থেকে বাইরের `next_id` variable বদলাতে এটা লাগে।
"""


"""
## কেন এভাবে
- **`response_model=list[TodoResponse]`**: আগে single `TodoResponse` ছিল, এখানে `list[TodoResponse]` — মানে বলছি output একটা `array`, প্রতিটা item `TodoResponse`-এর shape মেনে চলবে।
- **`return fake_todos_db`**: যত `todo` POST করে জমা করেছেন, সব একসাথে ফেরত যাবে। `database`-এর বদলি হিসেবে এই একটা `list`-ই আমাদের সব data রাখছে।
"""


"""
## কেন এভাবে
- **`"/{todo_id}"`**: `path parameter`, ঠিক আগের test project-এ `/hello/{name}` যেমন ছিল সেভাবে।
- **`todo_id: int`**: `type hint` দেওয়ায় FastAPI নিজে `string` থেকে `int`-এ রূপান্তর করে, আর কেউ `/todos/abc` দিলে নিজে থেকেই `422 Validation Error` দেয়।
- **`for` loop দিয়ে খোঁজা**: `fake_todos_db`-তে যেহেতু কোনো real database নেই, তাই list-এর ভেতর ঘুরে `id` মিলিয়ে দেখছি। এটা অস্থায়ী পদ্ধতি — পরে SQLAlchemy আসলে এই কাজ `query`-তে এক লাইনে হবে (`WHERE id = ...`), `loop` লাগবে না।
- **`raise HTTPException(status_code=404, ...)`**: `id` না মিললে খালি `None` ফেরত দেওয়া ভুল, কারণ `response_model=TodoResponse` সেটা মানবে না, error দেবে। তার বদলে সঠিকভাবে `404 Not Found` পাঠাচ্ছি।

## একটা গুরুত্বপূর্ণ বিষয়: Route-এর ক্রম
`get_todo` (`/{todo_id}`) অবশ্যই `get_todos`-এর (`/`) **নিচে** থাকতে হবে, কিন্তু `create_todo`-র (`POST /`) সাথে কোনো conflict নেই যেহেতু `method` (`POST` vs `GET`) আলাদা। এখানে ঠিক আছে, কিন্তু মনে রাখবেন: FastAPI উপর থেকে নিচে route মেলায়, তাই general path-এর (`/{todo_id}`) আগে যদি কোনো specific path (যেমন ভবিষ্যতে `/search`) লেখেন, সেটা ভুলভাবে `todo_id="search"` হিসেবে ধরে নেবে।
"""


"""
## কেন এভাবে

- **`todo_id: int` + `updated_todo: TodoCreate`**: এখানে দুটো জিনিস একসাথে লাগছে — `path`-এ কোনটা update হবে (`todo_id`), আর `body`-তে নতুন data (`TodoCreate`)। FastAPI নিজেই বুঝে নেয় কোনটা `path parameter`, কোনটা `body`।
- **`TodoCreate` কেন এখানেও ব্যবহার করলাম, নতুন class না বানিয়ে?** কারণ update করার সময়ও ঠিক create-এর মতোই সব field (`title`, `description`, `priority`, `completed`) লাগবে, `id` লাগবে না (সেটা `path`-এ আছে)। তাই একই shape, নতুন class বানানোর দরকার নেই।
- **`enumerate(fake_todos_db)`**: শুধু `todo` না, তার `index`-ও লাগবে, কারণ `list`-এর ভেতর সরাসরি সেই জায়গায় নতুন object বসাতে হবে (`fake_todos_db[index] = ...`)।
- **`404` আগের মতোই**: `id` না পেলে একই ধরনের error।

## একটা সীমাবদ্ধতা, যেটা মাথায় রাখা ভালো
এই `PUT` পদ্ধতিতে **সব field** নতুন করে দিতে হয়, একটা field বাদ দিলে সেটা তার `default`-এ ফিরে যাবে (যেমন `priority` না দিলে `1` হয়ে যাবে)। শুধু একটা field (যেমন শুধু `completed`) বদলানোর জন্য আলাদা পদ্ধতি (`PATCH`) লাগে, সেটা চাইলে CRUD শেষে দেখাব।
"""


"""
## কেন এভাবে
- **`response_model` নেই এখানে**: কারণ delete-এর পর কোনো `Todo` object ফেরত দেওয়ার মানে হয় না, শুধু একটা confirmation message যথেষ্ট। তাই `TodoResponse` লাগেনি।
- **`fake_todos_db.pop(index)`**: `list` থেকে ওই `index`-এর item সরিয়ে দেয়।
- **`404` আগের মতোই**: না পেলে একই pattern follow করছি, পুরো `router.py` জুড়ে consistency থাকছে।
"""

