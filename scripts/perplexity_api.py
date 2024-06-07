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
        
        **Concise Summaries with Subheadings**
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
4. The product review should be strictly in context of `given_context`.


**Note**: These product reviews are supposed to be sub sections of a bigger blog that summarizes product reviews. So ensuring the consistent markdown formatting is very important.
"""

ProductReviewInstructions_v2= """
## Instructions for Product Reviewer
As an Product Reviewer, your goal is to foster a clear understanding of the `given product` for your readers. 
To achieve this, follow the structured approach outlined below:

```
Start with a plain text description of the product. Don't include any Markdown heading as it is already in the initial blog.
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
4. The product review should be strictly in context of `given_context`.
5. Do not generate any markdown heading for the product review.


user following example to generate the product review:

### Example 1: `Sony WH-1000XM4`

Output:
---
#### Features & Pricing
The Sony WH-1000XM4 wireless noise-canceling headphones are a technological marvel. They boast a rich-textured, slightly warm tonality and a wide soundstage with excellent stereo separation. The headphones are lightweight and comfortable, with intuitive controls and impressive smart technologies like automatic pause and proximity sensors. They also feature a 30-hour battery life and flawless microphone quality. The noise-canceling capabilities are exceptional, making them a virtual isolation chamber that blocks out external noise.

The headphones are priced at $349, which some may find a bit steep considering their plastic-and-leatherette build. However, they are a solid product within their limitations.

#### Pros and Cons
###### Pros:
- Excellent noise-canceling capabilities
- Comfortable and lightweight design
- Intuitive controls and smart technologies
- Good sound quality with a balanced signature
- Long battery life

###### Cons:
- Plastic-and-leatherette build may not be as durable as metal-enhanced alternatives
- Noise-canceling can compromise sound quality
- May not be the best choice for audiophiles seeking high-fidelity sound
#### Customer Reviews
Many users have praised the headphones for their exceptional noise-canceling abilities, comfort, and sound quality. Some have noted that the touch gestures can be finicky and that the call quality can be hit-or-miss. However, overall, the headphones have received positive reviews for their performance and features.

##### Overall
The Sony WH-1000XM4 headphones are a technological landmark in the world of noise-canceling headphones. While they may not be the best choice for audiophiles seeking high-fidelity sound, they are an excellent option for those seeking a comfortable, feature-rich, and effective noise-canceling experience.
---


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
                    "Use blog formatting: \n{}".format(ProductReviewInstructions_v2)
                ),
            },
            {
                "role": "user",
                "content": (
                    f"write the product review of {keyword}, in context of `given_context`: '{context}'"
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
    