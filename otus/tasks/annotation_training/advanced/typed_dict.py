"""
TODO:

Define a class `Undergraduate` using the predefined class `Student`.
`Undergraduate` has an extra key `major` of type string
"""

from typing import TypedDict


class Student(TypedDict):
    name: str
    age: int
    school: str


class Undergraduate(Student):
    major: str
