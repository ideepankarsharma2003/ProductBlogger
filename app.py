import streamlit as st
from scripts import (
    create_streaming_blog,
    list_products,
    get_ranking_products
)
import json




# Sidebar with input and button
st.sidebar.header("Blog Settings")
keyword = st.sidebar.text_input("Keyword", "")
write_blog_button = st.sidebar.button("Write Blog")

# Placeholder for the blog content
title_placeholder = st.empty()

# Generate and display blog if button is clicked
if write_blog_button and keyword:
    blog= list_products(keyword)
    
    if blog:
        # Streamlit app layout
        title_placeholder.title(f":blue[{blog.blog_title}]")
        st.write(blog.intro)
        # full_response+=f"{blog.intro}\n"
        products= blog.products
        print(f"products: {products}")
        # placeholder.markdown(full_response)
        for product in products:
            full_response = ""
            st.subheader(product)
            image_placeholder = st.empty()
            placeholder = st.empty()
            amazon_results= get_ranking_products(product, 1)
            # print(amazon_results)
            if not amazon_results["error"]:
                image= amazon_results.get("results")[0].get("image")
                name= amazon_results.get("results")[0].get("name")
                image_placeholder.image(image, caption=name)
            response_stream = create_streaming_blog(product, keyword)
            # Iterate through the response stream
            for response in response_stream:
                # Append the new content to the full response
                full_response += response.choices[0].delta.content
                # Update the placeholder with the accumulated response
                placeholder.markdown(full_response)
            full_response+="\n\n"
            
        st.subheader("Conclusion")
        st.markdown(blog.conclusion)
        
    
            
    
