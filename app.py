import streamlit as st
from scripts import (
    create_streaming_blog,
    list_products
)





# Sidebar with input and button
st.sidebar.header("Blog Settings")
keyword = st.sidebar.text_input("Keyword", "")
write_blog_button = st.sidebar.button("Write Blog")

# Placeholder for the blog content
title_placeholder = st.empty()
placeholder = st.empty()

# Generate and display blog if button is clicked
if write_blog_button and keyword:
    full_response = ""
    blog= list_products(keyword)
    
    if blog:
        # Streamlit app layout
        title_placeholder.title(blog.blog_title)
        full_response+=f"{blog.intro}\n"
        products= blog.products
        print(f"products: {products}")
        placeholder.markdown(full_response)
        for product in products:
            response_stream = create_streaming_blog(product, keyword)
            # Iterate through the response stream
            for response in response_stream:
                # Append the new content to the full response
                full_response += response.choices[0].delta.content
                # Update the placeholder with the accumulated response
                placeholder.markdown(full_response)
            full_response+="\n"
        full_response+=f"## Conclusion\n{blog.conclusion}"
        placeholder.markdown(full_response)
        
    
            
    
