from langchain_openai import ChatOpenAI
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv
from scripts import research_blog


load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")


class Products(BaseModel):
    products: list[str] = Field(description="A list of relevant products.")

structured_llm = llm.with_structured_output(Products)

def list_products(topic):
    """list all the products available"""
    try:
        response= research_blog(topic)
        content= response.choices[0].message.content
        prompt= f"find the products related to `{topic}` from the following text: \n```\n{content}\n```"
        print(prompt)
        
        product= structured_llm.invoke(prompt)
        return product.products
        
    except Exception as e:
        print(e)
        return None
    