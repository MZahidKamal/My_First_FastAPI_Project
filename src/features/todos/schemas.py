from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    description: str | None = None
    priority: int = 1
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoResponse(TodoBase):
    id: int








"""
Type-এর সিদ্ধান্তগুলো কেন এমন

- **`title: str`**: বাধ্যতামূলক, `default` নেই।
- **`description: str | None = None`**: সবাই description লিখবে না, তাই `Optional`। `str | None` মানে হয় `string` হবে, নাহলে `None`। `default = None` দেওয়ায় এই field না দিলেও চলবে।
- **`priority: int = 1`**: আপাতত simple `int` রাখলাম (যেমন `1`, `2`, `3`)। এটা পরে চাইলে `Enum` (`low`/`medium`/`high`) দিয়ে ভালোভাবে লেখা যায়, কিন্তু সেটা একটা নতুন concept, তাই এখন শুধু `int` দিয়ে শুরু করছি।
- **`completed: bool = False`**: নতুন `todo` তৈরি হলে default-ভাবে অসম্পূর্ণ থাকবে।

## একটা জিনিস খেয়াল করুন
`str | None` syntax কাজ করতে Python `3.10+` লাগে। আপনার `.venv`-এ Python `3.14` আছে (আগের screenshot-এ দেখেছিলাম), তাই সমস্যা হবে না।

লিখে ফেলুন, তারপর জানান কোনো লাল দাগ/error আছে কি না। এরপর Step 4-এ `TodoCreate` আর `TodoResponse` বানিয়ে বোঝাব `id` কেন আলাদাভাবে যোগ হয়।
"""


"""
## কেন দুটো আলাদা class লাগে
- **`TodoCreate(TodoBase)`**: user যখন নতুন `todo` বানাতে `POST` করবে, তখন `request body`-তে এই shape লাগবে। এখানে `TodoBase`-এর সব field-ই আছে, নতুন কিছু নেই, তাই শুধু `pass` লিখে বলছি হুবহু `TodoBase`-এর মতোই"। আলাদা class কেন বানালাম যদি হুবহু একই? কারণ ভবিষ্যতে `create`-এর সময় আলাদা কোনো rule লাগলে (যেমন `title` অন্তত ৩ অক্ষর) শুধু এই class-এ বদলাব, `TodoBase` বা `TodoResponse` ছোঁব না।
- **`TodoResponse(TodoBase)`**: `database` থেকে `todo` ফেরত পাঠানোর সময় এই shape ব্যবহার হবে। এখানে `TodoBase`-এর সব field + নতুন `id: int`। আগে বলেছিলাম, `id` user দেয় না, `database` বানায়, তাই এটা শুধু `response`-এ থাকে, `create`-এ না।
"""

