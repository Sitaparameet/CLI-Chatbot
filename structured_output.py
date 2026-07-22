from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator


load_dotenv()


class UserInfo(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=50,
        description="The person's name"
    )

    age: int = Field(
        description="The person's actual age"
    )

    city: str | None = Field(
        default=None,
        description="The person's city if mentioned"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):

        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty")

        return value


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


structured_llm = llm.with_structured_output(UserInfo)


text = """
My name is Meet and I am 150 years old.
"""


try:

    userinfo = structured_llm.invoke(text)

    print("Structured Output:")
    print(userinfo)

    if not 0 <= userinfo.age <= 120:
        raise ValueError(
            f"Invalid age: {userinfo.age}. "
            "Age must be between 0 and 120."
        )

    print("Name:", userinfo.name)
    print("Age:", userinfo.age)
    print("City:", userinfo.city)


except Exception as e:

    print("Error:", e)