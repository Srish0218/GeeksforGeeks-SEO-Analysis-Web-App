# [GeeksforGeeks SEO Analysis Web App](https://srish-geeksforgeeks-seo-analysis.streamlit.app/)

GeeksforGeeks SEO Analysis Web App is a Streamlit-based web application designed for analyzing the SEO aspects of GeeksforGeeks web pages. It provides a comprehensive insight into the metadata, keywords, keyword density, and most common words present in the article content of GeeksforGeeks pages. The primary focus is on the content of the articles, excluding navigation bars and sidebars.

*Note: Keywords are currently extracted from the meta keyword tag. In its current state, the app considers words present in the meta keyword tag as keywords. Future updates will include more sophisticated algorithms to determine keywords, making it a beginner-friendly project. Contributions and improvements are welcome!*

## Features

- **Metadata Analysis:** Retrieve and display the title, keywords, and description of a GeeksforGeeks web page.

- **Keywords Analysis:** Analyze and display the keywords used in the GeeksforGeeks web page.

- **Keyword Density Analysis:** Visualize the distribution of keyword density through pie charts, histograms, and bar charts.

- **Most Common Words Analysis:** Identify and display the most common words used in the article content.

## Getting Started

### Prerequisites

Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Srish0218/GeeksforGeeks-SEO-Analysis-Web-App.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open the GeeksforGeeks URL in your web browser.

3. Enter the URL of the GeeksforGeeks web page you want to analyze and explore the SEO insights.

### Contributing
If you would like to contribute to the project, feel free to fork the repository and submit pull requests.

### License
This project is licensed under the MIT License.

### Acknowledgments
1. [Streamlit](https://streamlit.io/)
2. [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
3. [NLTK](https://www.nltk.org/)