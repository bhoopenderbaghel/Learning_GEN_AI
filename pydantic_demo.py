from pydantic import BaseModel

class Student(BaseModel):
    name: str

    new_student = {'name':'bhoopender'}

    students = students(**new_student)

print(Student)