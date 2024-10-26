import requests
import pandas as pd
import re
import streamlit as st
import html

# Function to get the webpage content
def get_webpage_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
        return None

# Function to read keywords from the uploaded file
def read_keywords_from_file(file):
    try:
        keywords = [line.decode('utf-8').strip().lower() for line in file if line.strip()]
        return keywords
    except Exception as e:
        st.error(f"Error reading keywords file: {e}")
        return []

# Function to remove HTML tags from content
def remove_html_tags(content):
    # Use a regular expression to remove HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', content)

# Function to count keyword occurrences accurately using regular expressions
def count_keywords(content, keywords):
    # Remove HTML tags and decode HTML entities
    text = remove_html_tags(content)
    text = html.unescape(text).lower()  # Convert text to lowercase for case-insensitive search

    # Dictionary to store keyword counts
    keyword_count = {}

    # Count occurrences of each keyword using regex
    for keyword in keywords:
        # Create a regex pattern to match the keyword as a whole word
        pattern = rf'\b{re.escape(keyword)}\b'
        count = len(re.findall(pattern, text))
        keyword_count[keyword] = count

    return keyword_count

# Streamlit UI setup
st.title("Keyword Count Analysis")

# URL input
url = st.text_input("Enter the URL to analyze: ")

# File upload for keywords
uploaded_file = st.file_uploader("Upload a file containing keywords (one per line)", type=['txt'])

# Main logic execution
if st.button("Analyze Keywords") and uploaded_file:
    # Read keywords from uploaded file
    keywords = read_keywords_from_file(uploaded_file)

    # Fetch the webpage content
    content = get_webpage_content(url)

    if content and keywords:
        # Count keywords
        keyword_count = count_keywords(content, keywords)

        # Display results as a DataFrame
        df = pd.DataFrame(list(keyword_count.items()), columns=['Keyword', 'Count'])
        st.write("Keyword Counts:")
        st.dataframe(df)

        # Download option for results as CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results as CSV", data=csv, file_name="keyword_counts.csv", mime="text/csv")
