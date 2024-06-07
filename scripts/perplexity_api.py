import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI



PERPLEXITY_API_KEY= os.environ.get('PERPLEXITY_API_KEY')



BLOG_RESEARCHER_INSTRUCTIONS= """
## Instructions for Content Researcher
As an Content Researcher, your goal is to research about the given topic and find all the products relevant to the topic:
"""

ProductReviewInstructions= """
## Instructions for Product Reviewer
As an Product Reviewer, your goal is to foster a clear understanding of the `given product` for your readers. To achieve this, follow the structured approach outlined below:

```
        ### Product 
        Name of the product 
        
        #### **Concise Summaries with Subheadings**
        Break down the material into manageable sections, each with its own subheading. This helps readers absorb the information and develop the ability to apply their knowledge effectively. 
        Examples of manageable sections can be found below:
            - #### Features & Pricing
            - #### Pros and Cons
            - #### Customer Reviews

        #### **Overall**
        End with a overall takeaway of the product.
        
```


Adhere to following constraints while writing the blog post:
### Constraints
1. The output should have the structure provided above.
2. Do not generate anything except the product review.
3. Do not include any explanatory outputs.


**Note**: These product reviews are supposed to be sub sections of a bigger blog that summarizes product reviews. So ensuring the consistent markdown formatting is very important.
"""



client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

def create_streaming_blog(keyword: str, context: str= ""):
    messages = [
            {
                "role": "system",
                "content": (
                    "You are a famous blogger who writes detail blogs and product reviews."
                    "Before writing a blog you research about the product, it's product specifications and what other people review about it."
                    "You consider everything and then write a product review about the product."
                    "Use blog formatting: \n{}".format(ProductReviewInstructions)
                ),
            },
            {
                "role": "user",
                "content": (
                    f"write the product review of {keyword}, in context of `{context}`"
                ),
            },
        ]
    # print(f"messages: {messages}")
    response_stream = client.chat.completions.create(
                model="llama-3-sonar-large-32k-online",
                messages=messages,
                stream=True,
            )
    return response_stream
    

def research_blog(topic: str):
    messages = [
            {
                "role": "system",
                "content": (
                    "You are a product researcher who researches about all the products related to the given topic."
                    "Use blog formatting: \n{}".format(BLOG_RESEARCHER_INSTRUCTIONS)
                ),
            },
            {
                "role": "user",
                "content": (
                    topic
                ),
            },
        ]
    # print(f"messages: {messages}")
    response_stream = client.chat.completions.create(
                model="llama-3-sonar-large-32k-online",
                messages=messages,
                stream=False,
            )
    return response_stream
    