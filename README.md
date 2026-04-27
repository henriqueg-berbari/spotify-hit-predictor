# 🎵 Spotify Hit Predictor: A Data Science Journey

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://spotify-hit-predictor-g7krvylpaaqzh3dnlyuqsp.streamlit.app/)
📖 The Story Behind the Data
My journey into data science began with a simple goal: to make storytelling with data both accessible and compelling. Over the past few months, I have been honing my skills in Python—mastering the manipulation of Pandas and NumPy, and now of visualization libraries like Plotly, MatplotLib and Seaborn.

As a huge music-enthusiast myself, I was lucky to find such a dataset, that would allow me to put my skills into a test, with something I am passionate about:

### 🔍 Finding the Dataset
I found the dataset Spotify 1 Million Tracks dataset on Kaggle, which was really fascinating to me. Not only was it a dataset with 1 million datapoints from songs from 2000 - 2023, but the different collumns it provided, such as Danceability, Instrumentalness, and Energy were really intriguing.

Now, as much excited as I was, I had to have some initial structure, to guide my investigation.

Before diving into the code, I focused my investigation on one core question:  
> **"What makes a song popular in the streaming era?"**

###🧪 Personal Hypotheses
I had to control myself before starting the EDA and diving deep into the data, by creating two initial hypotheses, that would then initiate my investigation

**Hypothesis 1** - Duration of Songs: I suspected that songs are getting shorter as a direct side-effect of social media, and the aim of artists of becoming viral

**Hypothesis 2** - Danceability : I also suspstected that songs are getting progressively more danceable, also with artist´ aim to get viral, potentialized by social media.

Detailed exploration of these theories can be found in my **[Exploratory Data Analysis Notebook 🔍](./eda.ipynb)**. *(Note: Replace ./eda.ipynb with your actual filename)*
---

## 🤖 Challenging the Machine
As I uncovered trends in the EDA, I decided to push my boundaries. Despite being early in my Machine Learning journey, I implemented a **Random Forest Regressor** to see if a machine could predict a hit more accurately than a human ear.

### 🏆 High-Level Findings
* **Accuracy:** The model correctly identifies the DNA of a "hit" with **67% accuracy**.
* **The Blueprint:** Data suggests a 2026 "Hit" sweet spot: **185s–210s** duration and a **Danceability score > 0.72**.
* **The Human Factor:** While data provides a stable "floor," my study suggests that 33% of a song's success remains in the "X-Factor"—the unquantifiable magic of art.
  
## 🚀 Experience the Live App
I built a fully interactive dashboard to make these findings come to life. 

### [👉 Open the Spotify Hit Predictor](https://spotify-hit-predictor-g7krvylpaaqzh3dnlyuqsp.streamlit.app/)

**Inside the app, you can:**
* **Filter** 20+ years of history by genre and artist.
* **Visualize** correlation heatmaps of musical features.
* **Interact** with the Model Analysis to see where the machine succeeded and where it was surprised.

---

## 🛠️ Technical Toolkit
* **Language:** Python
* **Libraries:** Pandas, NumPy, Scipy, Matplotlib, Seaborn, Plotly
* **Deployment:** Streamlit Cloud
* **Data Sourcing:** GDown (Google Drive API)
