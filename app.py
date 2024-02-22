import streamlit as st
from bs4 import BeautifulSoup
import requests
from collections import Counter
import pandas as pd


# Function to get metadata
def get_metadata(url):
    try:
        page = requests.get(url)
        page.raise_for_status()

        soup = BeautifulSoup(page.content, 'html.parser')

        title_tag = soup.find("title")
        meta_tags = soup.find_all("meta")

        return {
            "title": title_tag.text.strip() if title_tag else None,
            "keywords": [meta.get("content", "").strip() for meta in meta_tags if "keywords" in str(meta).lower()],
            "description": [meta.get("content", "").strip() for meta in meta_tags if
                            "description" in str(meta).lower()],
            "text_content": soup.get_text(separator=' ').strip()
        }

    except requests.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None


# Function to analyze keywords
def analyze_keywords(text_content):
    words = text_content.split()
    total_words = len(words)
    word_counter = Counter(words)
    most_common_words = word_counter.most_common()

    return total_words, most_common_words


## Streamlit App
st.markdown("<h1 style ='text-align:center;'>Simple SEO Analysis Web App</h1>", unsafe_allow_html=True)
st.markdown("---")

url = st.text_input("Enter URL: ")

if url:
    metadata = get_metadata(url)

    if metadata:
        st.title("Metadata Analysis")
        st.write(f"Title: {metadata['title']}")

        st.title("Keywords Analysis")
        st.write("Keywords:")
        st.write(metadata['keywords'])

        st.title("Description Analysis")
        st.write("Description:")
        st.write(metadata['description'])

        st.title("Keyword Density Analysis")
        total_words, most_common_words = analyze_keywords(metadata['text_content'])
        st.write(f"Total Words: {total_words}")
        keywords_list = metadata['keywords'][0].split(',')
        st.write(f"Total Keywords: {len(keywords_list)}")

        keyword_density = len(metadata['text_content'].split()) / len(keywords_list) if len(
            metadata['keywords']) > 0 else 0
        st.write(f"Keyword Density: {keyword_density:.2f} words per keyword")  # ...

        # st.title("Most Common Words Analysis")
        # words, counts = zip(*most_common_words[:10])  # Take only the first 10 elements
        # table_data = {"Word": words, "Count": counts}
        #
        # # Create a Pandas DataFrame
        # df = pd.DataFrame(table_data)
        #
        # # Display the scrolling table using HTML and CSS
        # st.markdown(
        #     f"""
        #     <style>
        #         .scrolling-table {{
        #             overflow: auto;
        #             max-height: 400px;
        #         }}
        #     </style>
        #     <div class="scrolling-table">
        #         {df.to_html(index=False, escape=False)}
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )
    else:
        st.warning("No metadata found for the provided URL.")
