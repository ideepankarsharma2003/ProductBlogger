from langchain_openai import ChatOpenAI
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv
from scripts import research_blog


load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")



blog_prompt= """
You're tasked with creating a compelling blog post on the latest trends in [industry/niche/topic]. Your blog, titled "Exploring [Industry/Niche/Topic]: A Comprehensive Guide," aims to inform and engage readers about recent developments and key insights in the field.

1. **Blog Title:** "Exploring [Industry/Niche/Topic]: A Comprehensive Guide"
   
2. **Introduction:** Craft an engaging introductory paragraph that sets the stage for the blog post. Provide a brief overview of the industry/niche/topic and hint at the exciting trends and insights to be discussed.

3. **Key Trends:** Delve into the latest trends shaping the [industry/niche/topic]. Highlight emerging technologies, innovative strategies, or noteworthy shifts in consumer behavior. Use examples and statistics to support your points.

4. **Relevant Products:** Identify and discuss products or services that are making waves in the industry. Whether it's a groundbreaking tool, a must-have gadget, or a game-changing app, showcase how these products are revolutionizing the landscape.

5. **Conclusion:** Summarize the key takeaways from the blog post. Reinforce the significance of the discussed trends and products, and encourage readers to stay informed and explore further.

**Note:** Ensure the content is informative, engaging, and well-structured. Maintain a conversational tone throughout the blog post to captivate the audience and keep them hooked till the end.

---





"""

class Blog(BaseModel):
    blog_title: str= Field(description="Title of the blog")
    intro: str= Field(description="Explanatory introduction of the blog.")
    products: list[str] = Field(description="A list of relevant products.")
    conclusion: str= Field(description="Wrap up of the blog.")

structured_llm = llm.with_structured_output(Blog)

def list_products(topic):
    """list all the products available"""
    try:
        response= research_blog(topic)
        content= response.choices[0].message.content
        prompt= f"{blog_prompt}\n\nWrite the blog elements related to `{topic}` from the following text: \n```\n{content}\n```"
        print(prompt)
        
        blog= structured_llm.invoke(prompt)
        return blog
        
    except Exception as e:
        print(e)
        return None
    