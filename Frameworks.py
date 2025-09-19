import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

@st.cache_data(ttl=3600)
def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)

    # Drop columns with >50% missing values
    threshold = 0.5
    missing_fraction = df.isnull().mean()
    columns_many_missing = missing_fraction[missing_fraction > threshold].index
    df.drop(columns=columns_many_missing, inplace=True)

    # Fill missing key columns
    df['title'].fillna('No Title', inplace=True)
    df['publish_time'].fillna(method='ffill', inplace=True)
    df['abstract'].fillna('No Abstract', inplace=True)

    # Convert publish_time to datetime and extract year
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['publish_year'] = df['publish_time'].dt.year

    # Abstract word count
    df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()))

    return df

def plot_publications_over_time(df):
    papers_per_year = df['publish_year'].value_counts().sort_index()
    fig, ax = plt.subplots()
    papers_per_year.plot(kind='line', marker='o', ax=ax)
    ax.set_title('Number of COVID-19 Publications by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.grid(True)
    st.pyplot(fig)

def plot_top_journals(df):
    if 'journal' in df.columns:
        top_journals = df['journal'].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(y=top_journals.index, x=top_journals.values, ax=ax, palette='viridis')
        ax.set_title('Top 10 Journals Publishing COVID-19 Research')
        ax.set_xlabel('Number of Publications')
        ax.set_ylabel('Journal')
        st.pyplot(fig)
    else:
        st.write("No 'journal' column found in dataset.")

def plot_wordcloud(df):
    if 'title' in df.columns:
        all_titles = ' '.join(df['title'].dropna().astype(str)).lower()
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
        fig, ax = plt.subplots(figsize=(15, 7.5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Word Cloud of Paper Titles')
        st.pyplot(fig)
    else:
        st.write("No 'title' column found in dataset.")

def plot_source_distribution(df):
    if 'source_x' in df.columns:
        source_counts = df['source_x'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(y=source_counts.index, x=source_counts.values, ax=ax, palette='coolwarm')
        ax.set_title('Distribution of Paper Counts by Source')
        ax.set_xlabel('Number of Papers')
        ax.set_ylabel('Source')
        st.pyplot(fig)
    else:
        st.write("No 'source_x' column found in dataset.")

def main():
    st.set_page_config(page_title="CORD-19 Metadata Analysis", layout="wide")
    st.title("CORD-19 Metadata Analysis Dashboard")
    st.write("Explore the COVID-19 Open Research Dataset metadata interactively.")

    csv_path = 'metadata.csv'  # Your CSV file path

    try:
        df = load_and_clean_data(csv_path)
        st.success(f"Loaded dataset with {len(df)} records and {len(df.columns)} columns.")
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        return

    # Sidebar filters
    st.sidebar.header("Filter Options")
    min_year = int(df['publish_year'].min())
    max_year = int(df['publish_year'].max())
    year_filter = st.sidebar.slider("Publication Year Range", min_year, max_year, (min_year, max_year))

    journal_options = ["All"]
    if 'journal' in df.columns:
        journal_options += sorted(df['journal'].dropna().unique())
    selected_journal = st.sidebar.selectbox("Select Journal", journal_options)

    # Filtering data
    filtered_df = df[(df['publish_year'] >= year_filter[0]) & (df['publish_year'] <= year_filter[1])]
    if selected_journal != "All":
        filtered_df = filtered_df[filtered_df['journal'] == selected_journal]

    # Display filtered data sample
    st.header("Sample of Filtered Data")
    st.dataframe(filtered_df.head(10))

    # Visualizations
    st.header("Publications Over Time")
    plot_publications_over_time(filtered_df)

    st.header("Top Journals")
    plot_top_journals(filtered_df)

    st.header("Word Cloud of Paper Titles")
    plot_wordcloud(filtered_df)

    st.header("Source Distribution")
    plot_source_distribution(filtered_df)

if __name__ == "__main__":
    main()