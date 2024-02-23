import streamlit as st
from bs4 import BeautifulSoup
import requests
from collections import Counter
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

# Function to get metadata
def get_metadata(url):
    try:
        start_time = time.time()  # Record the start time
        page = requests.get(url)
        # Check the status code
        if 200 <= page.status_code < 300:
            page.raise_for_status()

        else:
            st.warning(f"Received an unexpected status code: {page.status_code}")
            return None

        soup = BeautifulSoup(page.content, 'html.parser')

        title_tag = soup.find("title")
        meta_tags = soup.find_all("meta")

        # Extract text content from elements with class "article--viewer_content"
        article_content_elements = soup.find_all(class_="article--viewer_content")
        article_text_content = ' '.join(element.get_text(separator=' ', strip=True) for element in article_content_elements)

        end_time = time.time()  # Record the end time
        analysis_time = end_time - start_time  # Calculate the time taken for analysis

        return {
            "title": title_tag.text.strip() if title_tag else None,
            "keywords": [meta.get("content", "").strip() for meta in meta_tags if "keywords" in str(meta).lower()],
            "description": [meta.get("content", "").strip() for meta in meta_tags if
                            "description" in str(meta).lower()],
            "text_content": article_text_content.strip(),  # Use the extracted content
            "analysis_time": analysis_time  # Add analysis time to the result
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

# Streamlit App
st.markdown("<h1 style ='text-align:center;'>GeeksforGeeks SEO Analysis Web App</h1>", unsafe_allow_html=True)
st.markdown("---")

url = st.text_input("Enter URL: ")

if url:
    metadata = get_metadata(url)

    if metadata:
        with st.spinner('Wait for it...'):
            time.sleep(0.5)
        st.success('Done!')
        st.title("Metadata Analysis")

        if metadata['title']:
            st.write(f"Title: {metadata['title']}")
        else:
            st.warning("No meta Title found on the provided URL.")

        st.title("Keywords Analysis")
        if metadata['keywords']:
            st.write("Keywords:")
            st.write(metadata['keywords'])
        else:
            st.warning("No meta keywords found on the provided URL.")

        st.title("Description Analysis")
        if metadata['description']:
            st.write("Description:")
            st.write(metadata['description'])
        else:
            st.warning("No meta description found on the provided URL.")

        # Keyword Density Analysis
        st.title("Word Analysis")
        total_words, most_common_words = analyze_keywords(metadata['text_content'])
        st.write(f"Total Words: {total_words}")
        keywords_list = [keyword.strip() for keyword in metadata['keywords'][0].split(',')] if metadata['keywords'] else []
        st.write(f"Total Keywords: {len(keywords_list)}")

        # Keyword Density Analysis
        st.title("Keyword Density Analysis")
        # Calculate keyword density for each keyword
        keyword_density_data = []
        for keyword in keywords_list:
            keyword_count = metadata['text_content'].lower().count(keyword.lower())
            keyword_density = (keyword_count / total_words) * 100
            if keyword_density != 0:  # Exclude keywords with density exactly 0
                keyword_density_data.append({"Keyword": keyword, "Density": keyword_density})

        # Create a Pandas DataFrame for Keyword Density
        keyword_density_df = pd.DataFrame(keyword_density_data)

        # Display the table for Keyword Density
        st.dataframe(keyword_density_df)

        # You can also display the average keyword density
        average_keyword_density = keyword_density_df["Density"].mean() if not keyword_density_df.empty else 0
        st.write(f"Average Keyword Density: {average_keyword_density:.2f}%")

        # Button to switch between charts
        tab1, tab2, tab3 = st.tabs(["Pie Chart", "Histogram", "Bar Chart"])

        with tab1:
            st.header("Keyword Density Pie Chart")
            fig = go.Figure(data=[go.Pie(labels=keyword_density_df['Keyword'],
                                         values=keyword_density_df['Density'],
                                         hole=.1,
                                         title="Keyword Density Distribution",
                                         textinfo='percent+label',  # Display percentage and label
                                         )])
            fig.update_layout(width=800, height=500)  # Adjust width and height
            st.plotly_chart(fig)

        with tab2:
            st.header("Keyword Density Histogram")
            fig = px.histogram(keyword_density_df, x='Density', nbins=20, title='Keyword Density Distribution')
            st.plotly_chart(fig)

        with tab3:
            st.header("Keyword Density Histogram Bar Chart")
            fig = px.bar(keyword_density_df, x='Keyword', y='Density', title='Keyword Density Distribution', height=500,
                         width=800)
            st.plotly_chart(fig)

        # Most Common Words Analysis
        st.title("Most Common Words Analysis")

        # Define stop words
        stop_words = set(stopwords.words('english'))

        # Define symbols to exclude using the string module
        symbols_to_exclude = set(string.punctuation)

        # Filter out common English words and symbols
        filtered_most_common_words = [
            (word, count) for word, count in most_common_words
            if word.lower() not in stop_words and not any(char in symbols_to_exclude for char in word)
        ]

        words, counts = zip(*filtered_most_common_words[:50])  # Take only the first 10 elements
        table_data = {"Word": words, "Count": counts}

        # Create a Pandas DataFrame for Most Common Words
        most_common_words_df = pd.DataFrame(table_data)
        st.dataframe(most_common_words_df)

        # Bar Chart for Most Common Words
        fig = px.bar(most_common_words_df, x='Word', y='Count', title='Most Common Words', height=500,
                     width=800)  # Adjust height and width
        st.plotly_chart(fig)

        st.markdown("---")
        st.success(f"Analysis completed in {metadata['analysis_time']:.2f} seconds.")
    else:
        st.warning("No metadata found for the provided URL.")

    # Footer
    st.markdown("---")
    st.markdown("Made with :red[❤️] by Srishti Jailty :cherry_blossom:. Powered by Streamlit, BeautifulSoup, Plotly, and NLTK.")
