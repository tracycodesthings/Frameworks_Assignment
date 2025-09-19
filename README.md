# 📊 CORD-19 Data Exploration and Visualization

## 📖 Overview
This project explores the **CORD-19 metadata dataset**, focusing on metadata of COVID-19 related research papers.  
The workflow follows the **data science pipeline**: loading, cleaning, analyzing, visualizing, and deploying with **Streamlit**.

---

## 🗂️ Project Structure
- **Part 1: Data Loading and Basic Exploration**
  - Download and load `metadata.csv`
  - Explore the first rows, data types, dimensions, and missing values
  - Generate summary statistics

- **Part 2: Data Cleaning and Preparation**
  - Handle missing values (drop/fill where needed)
  - Convert `publish_time` to datetime
  - Extract year from publication date
  - Create additional columns (e.g., abstract word count)

- **Part 3: Data Analysis and Visualization**
  - Count publications by year
  - Identify top publishing journals
  - Find frequent words in titles
  - Visualizations:
    - Publications over time
    - Bar chart of top journals
    - Word cloud of titles
    - Distribution by source

- **Part 4: Streamlit Application**
  - Interactive dashboard for exploration
  - Widgets (sliders, dropdowns) for filtering
  - Displays charts and sample data

- **Part 5: Documentation and Reflection**
  - Well-commented code
  - Short report summarizing findings
  - Reflections on challenges and lessons learned

---

## 🚀 Getting Started

### 1️⃣ Prerequisites
Install the required Python packages:

```bash
pip install pandas matplotlib streamlit wordcloud


   
