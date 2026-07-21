from langchain_core.language_models.llms import LLM
from os import name
import os 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

# Model for output format       
class UserInfo(BaseModel):
    name: str = Field(description="Name of the user")
    age: int = Field(description="Age of the user")
    city: str = Field(description="city of the user")

llm = ChatOpenAI(
    model= "gpt-4o-mini"
)

structured_llm = llm.with_structured_output(UserInfo)

text = """
My name is Meet, I am 22 year old and I live in Ahmedabad
"""
try:
    userinfo = structured_llm.invoke(text)
    print("Structured_output:")
    print(userinfo)

    print("Name", userinfo.name)
    print("Age", userinfo.age)
    print("City", userinfo.city)

except Exception as e:
    print("Error",e) 