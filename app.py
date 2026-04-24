import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Spotify Analysis", layout="wide")



@st.cache_data
def load_data():
    cols = ['popularity', 'year', 'genre', 'danceability', 'energy', 
            'loudness', 'speechiness', 'acousticness', 'tempo', 'duration_ms']
    
    # Try the most likely path first
    try:
        data = pd.read_csv("spotify_data.zip", usecols=cols)
    except FileNotFoundError:
        # If that fails, try the root folder
        data = pd.read_csv("spotify_data.zip", usecols=cols)
    
    if 'Unnamed: 0' in data.columns:
        data = data.drop(columns=['Unnamed: 0'])
    return data

df = load_data()    
    # 2. Read only those columns
    data = pd.read_csv("spotify_data.zip", usecols=cols)
    
    # 3. Downcast numbers to take up less space
    data['year'] = data['year'].astype('int16')
    data['popularity'] = data['popularity'].astype('int8')
    
    return data
df = load_data()


st.sidebar.header("Filter Options")
year_list = ["All"] + sorted(df['year'].unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", year_list)

genre_list = ["All"] + sorted(df['genre'].unique().tolist())
selected_genre = st.sidebar.selectbox("Select Genre", genre_list)

st.sidebar.header("Search")
search_artist = st.sidebar.text_input("Type Artist Name:")

st.sidebar.header("Sorting Options")
sort_options = ['popularity', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'tempo', 'duration_ms']
sort_col = st.sidebar.selectbox("Sort by Feature:", options=sort_options)
pop_order = st.sidebar.radio("Order Direction:", options=["Highest First", "Lowest First"])
is_ascending = (pop_order == "Lowest First")


display_df = df.copy()
if selected_year != "All":
    display_df = display_df[display_df['year'] == selected_year]
if selected_genre != "All":
    display_df = display_df[display_df['genre'] == selected_genre]
if search_artist:
    display_df = display_df[display_df['artist_name'].str.contains(search_artist, case=False, na=False)]


tab_intro, tab_eda, tab_model, tab_conclusions = st.tabs(["📖 Data Explorer", "🔍 EDA", "🤖 Model Analysis", "Conclusion and Next Steps"])


with tab_intro:
  
    col1, col2 = st.columns([3, 1])

    with col1:
        st.title("🎵 Spotify Popularity 2000-2023")
        st.subheader("Decoding what makes a hit in the streaming era.")
        st.markdown("""
        The landscape of music is constantly shifting. This study investigates the complex 
        relationship between a song's **technical features** and its **commercial success.**
        """)

    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", width=100)

    st.divider()
    

    fact1, fact2, fact3 = st.columns(3)
    fact1.info("**Dataset**\n\nSpotify 1M+ Tracks")
    fact2.info("**Timeframe**\n\n2000 — 2023")
    fact3.info("**Focus**\n\n12+ Musical Features")

    st.caption("👈 Use the sidebar on the left to filter by Year, Genre, or Artist.")
    st.divider()


    if not display_df.empty:
        display_df = display_df.sort_values(by=sort_col, ascending=is_ascending)
        st.write(f"### 🎵 Top results sorted by {sort_col} ({pop_order})")
        st.dataframe(display_df.head(100), use_container_width=True)
    else:
        st.warning("No results found for those filters!")


import scipy.stats as stats 


with tab_eda:
    # --- DATA LOGIC ---
    df_period_b = df[df['year'] >= 2016]
    n_ten = int(len(df_period_b) * 0.1)
    top_b = df_period_b.nlargest(n_ten, 'popularity')
    bottom_b = df_period_b.nsmallest(n_ten, 'popularity')

    hi_df = df[df['popularity'] > 10] 
    yearly_trend = hi_df.groupby('year').apply(
        lambda x: stats.pearsonr(x['duration_ms'], x['popularity'])[0] if len(x) > 1 else None,
        include_groups=False
    )

    # --- HEADER ---
    st.title("🔍 Exploratory Data Analysis")
    st.markdown("This EDA is structured around **two core hypotheses** derived from market trends.")

    # --- HYPOTHESIS 1 & 2: TWO-COLUMN LAYOUT ---
    h_col1, h_col2 = st.columns(2)

    # --- HYPOTHESIS 1: DURATION ---
    with h_col1:        
        st.markdown("### ⏲️ Hypothesis 1: Song Duration")
        st.write("**Topic: The Shrinking Hit**")

        with st.expander("📊 View Evidence & Trends", expanded=True):
            # Standardized Metrics
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("Correlation (r)", "-0.12", help="A weak negative correlation indicating shorter songs trend slightly higher in popularity.")
            with col_stat2:
                st.metric("Avg. Length Change", "195s", delta="-45s vs 2000")
            
            st.info("While statistically weak, the consistent downward trend over 20 years suggests a structural shift in streaming.")

            # Plotly Chart
            trend_data = yearly_trend.reset_index()
            trend_data.columns = ['Year', 'Correlation']
            fig_trend = px.line(trend_data, x='Year', y='Correlation', markers=True, template='plotly_white')
            fig_trend.add_hline(y=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig_trend, use_container_width=True)

    # --- HYPOTHESIS 2: DANCEABILITY ---
    with h_col2:
        st.markdown("### 💃 Hypothesis 2: Danceability")
        st.write("**Topic: The Success Multiplier**")

        with st.expander("📊 View Key Insight", expanded=True):
            # Standardized Metrics
            met1, met2 = st.columns(2)
            with met1:
                st.metric("Correlation (r)", "0.10", help="A weak positive correlation.")
            with met2:
                st.metric("Success Multiplier", "1.53x", help="Likelihood of being a hit vs a flop.")

            st.info("Songs above **0.7** score are significantly more likely to reach the Top 10%.")

            # Density Plot
            fig_dance, ax = plt.subplots(figsize=(10, 6))
            sns.kdeplot(bottom_b['danceability'], label='Bottom 10% Songs', fill=True, ax=ax)
            sns.kdeplot(top_b['danceability'], label='Top 10% Songs', fill=True, ax=ax)
            ax.set_title('Distribution of Danceability (2016-2023)')
            ax.legend()
            st.pyplot(fig_dance) 

    st.divider()

    # --- TAKEAWAYS ---
    st.subheader("📌 Key Takeaways & Shift in Focus")
    c1, c2 = st.columns(2)
    with c1:
        st.success("**What we learned:** Duration is shorter; Danceability is a gatekeeper.")
    with c2:
        st.warning("**The Missing Piece:** Individual correlations are weak; we need an integrated view.")

    # --- HEATMAP SECTION ---
    st.header("🎯 Feature Correlation Overview")
    with st.expander("🗺️ View Full Heatmap", expanded=True):
        st.info("We can see that other features such as instrumentalness and loudness are also influential.")
        
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        corr_matrix = numeric_df.corr()

        fig_heatmap, ax_heat = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax_heat)
        
        # Centering logic strictly INSIDE the expander
        _, center_mid, _ = st.columns([1, 8, 1])
        with center_mid:
            st.pyplot(fig_heatmap)
        st.caption("Visualizing the relationship between all numeric features and song popularity.")

    st.divider()

    # --- TRANSITION TO MODEL ---
    with st.container(border=True):
        left_co, right_co = st.columns([1, 4])
        with left_co:
            st.markdown("<h1 style='text-align: center; font-size: 100px;'>🚀</h1>", unsafe_allow_html=True)
        with right_co:
            st.markdown("### **From Hypotheses to Predictive Modeling**")
            st.write("""
                Our deep dive confirmed that while individual traits have low correlation scores, 
                they represent 'rules of the game.' To win, we need to look at how these 
                features interact as a whole.
            """)
    
    st.success("""
        ### 🧠 **What's Next?**
        We have built a **Machine Learning Model** to decode the exact 'DNA' of a hit. 
        **Head over to the next tab to see if we can predict the next chart-topper!**
    """, icon="✅")


with tab_model:
    # --- SECTION 1: THE BIG REVEAL ---
    st.title("🧠 The Modern Hit Formula")
    st.markdown("""
    After analyzing thousands of tracks, we moved beyond simple correlations. 
    We built a **Predictive Engine** to determine if a song has the 'DNA' of a hit 
    before it ever touches a playlist.
    """)

    # --- SECTION 2: THE METHODOLOGY ---
    st.header("🤖 Our Methodology: The Random Forest")
    
    col_text, col_link = st.columns([2, 1])
    
    with col_text:
        st.write("""
        To predict popularity, we utilized a **Random Forest Regressor**. 
        Think of this model as a 'Council of 100 Experts.' Each 'expert' (a decision tree) 
        looks at the data and makes a prediction based on different features. 
        We then take the average of all these experts to get our final answer.
        """)
        
    with col_link:
        st.info("**Want to dive deeper?**")
        st.markdown("""
        Check out [this article](https://www.ibm.com/topics/random-forest) 
        which explains how Random Forest balances complexity and accuracy.
        """)
        st.markdown("""And check [this link](https://github.com/henriqueg-berbari) for the GitHub repository for the walk through of the full methodology""")

    st.divider()

    # --- SECTION 3: THE "WHY" ---
    st.subheader("🎯 Why this solution?")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### **Non-Linearity**")
        st.caption("Music isn't a straight line. High energy might be good, but TOO much energy might hurt. Random Forest captures these 'sweet spots.'")
    with c2:
        st.markdown("#### **Feature Importance**")
        st.caption("It tells us exactly which features (like danceability vs. loudness) weighed heaviest in the final decision.")
    with c3:
        st.markdown("#### **Stability**")
        st.caption("By using many trees, the model avoids being fooled by 'one-hit wonders' or outliers in the data.")

    # --- NEW STUFF: FEATURE IMPORTANCE (The DNA) ---
    st.divider()
    st.header("🧬 The DNA of a Hit: Feature Importance")
    st.write("Before looking at the final score, let's see which 'ingredients' the model found most important:")

    # Data from your model findings
    importance_df = pd.DataFrame({
        'Feature': ['Danceability', 'Loudness', 'Energy', 'Acousticness', 'Duration', 'Valence', 'Speechiness'],
        'Importance': [0.25, 0.18, 0.16, 0.12, 0.10, 0.10, 0.09]
    }).sort_values(by='Importance', ascending=True)

    fig_imp, ax_imp = plt.subplots(figsize=(10, 5))
    ax_imp.barh(importance_df['Feature'], importance_df['Importance'], color='#1DB954')
    ax_imp.set_title("Which features carry the most weight?")
    st.pyplot(fig_imp)
    # -----------------------------------------------

    st.header("📊 Model Performance Results")

    # --- TOP ROW: BIG NUMBERS ---
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Overall Accuracy", "67%", delta="High Confidence")
    with m2:
        st.metric("Flop Detection", "78%", help="Ability to correctly identify non-hits")
    with m3:
        st.metric("Hit Detection (Recall)", "54%", delta="-13%", delta_color="inverse")

    st.divider()

    # --- THE FLASHY CONFUSION MATRIX ---
    st.subheader("🎯 Prediction Accuracy Matrix")
    st.write("How well did the 'Council of Experts' actually perform?")

    col_spacer, col_matrix = st.columns([1, 3])

    with col_matrix:
        l1, l2 = st.columns(2)
        l1.markdown("<h4 style='text-align: center;'>Predicted FLOP</h4>", unsafe_allow_html=True)
        l2.markdown("<h4 style='text-align: center;'>Predicted HIT</h4>", unsafe_allow_html=True)

        r1_c1, r1_c2 = st.columns(2)
        with r1_c1:
            st.success("### 78%\n**Correctly Identified Flops**")
        with r1_c2:
            st.error("### 22%\n**Predicted Hit, but Floped**")

        r2_c1, r2_c2 = st.columns(2)
        with r2_c1:
            st.warning("### 46%\n**Missed Hits**")
        with r2_c2:
            st.info("### 54%\n**Correctly Identified Hits**")

    st.caption("**Note: The model is an 'Expert Critic'—it is very good at telling you what WON'T work.**")

    st.divider()
    st.header("🧐 What did the model get wrong?")
    st.write("""
        No model is perfect. By comparing what our Random Forest **expected** a hit to 
        sound like versus what **actually** topped the charts in 2023, we can see 
        how musical tastes are evolving in real-time.
    """)

    features = ['danceability', 'energy', 'valence', 'speechiness'] 
    comparison_df = pd.DataFrame({
        'Expected (Model)': [0.62, 0.58, 0.45, 0.09], 
        'Actual (Reality)': [0.58, 0.63, 0.43, 0.09]  
    }, index=features)

    fig_comp, ax_comp = plt.subplots(figsize=(10, 6))
    comparison_df.plot(kind='bar', ax=ax_comp, color=['#1f77b4', '#ff7f0e'])
    ax_comp.set_title("Musical Features: Model Expectation vs. 2023 Reality")
    ax_comp.set_ylabel("Normalized Score (0.0 - 1.0)")
    st.pyplot(fig_comp)

    c1, c2 = st.columns(2)
    with c1:
        st.warning("⚠️ **The 'Perfect Production' Trap**")
        st.write("The model expected hits to be more 'processed,' but 2023 showed a surge in acoustic and live-sounding elements.")
    with c2:
        st.success("✅ **Danceability is Still King**")
        st.write("While other features drifted, the model was almost spot-on regarding danceability, confirming it's the most stable predictor.")
        
with tab_conclusions:
    st.title("🎯 Final Verdict & Strategic Roadmap")
    
    # --- 1. THE PERFORMANCE BREAKDOWN (The "So What?") ---
    st.subheader("📊 Model Results: The 'So What?'")
    performance_data = {
        "Role": ["🛡️ The Expert Critic", "🎯 The Selective Scout", "🧠 The Human Factor"],
        "Metric": ["Flop Recall", "Hit Precision", "Hit Recall"],
        "Result": ["78%", "68%", "54%"],
        "The 'So What?'": [
            "Excellent at spotting songs that lack the technical 'DNA' of a hit.",
            "When the model predicts a 'Hit,' it’s right nearly 70% of the time.",
            "Confirms that 46% of hits succeed due to 'invisible' factors like marketing."
        ]
    }
    # Centering the table slightly for better readability
    _, table_col, _ = st.columns([0.1, 0.8, 0.1])
    with table_col:
        st.table(performance_data)

    st.divider()

    # --- 2. THE 2026 HIT BLUEPRINT (The "Actionable Spec") ---
    st.header("🔮 The 2026 Hit Blueprint")
    st.write("""
        Based on our Random Forest optimization, a track designed to maximize 
        statistical probability in the current market would follow this profile:
    """)

    blueprint_data = {
        "Feature": ["Danceability", "Loudness", "Energy", "Duration", "Acousticness"],
        "Target Value": ["> 0.72", "-6.5 dB", "0.65 - 0.75", "185s - 210s", "< 0.20"],
        "Strategic Reason": [
            "Movement-friendly rhythm remains the strongest gatekeeper.",
            "Optimized for high-end streaming playlist normalization.",
            "Balanced for engagement without listener fatigue.",
            "The 'Streaming Sweet Spot' for maximum replayability.",
            "Modern hits favor clean, electronic-processed textures."
        ]
    }
    
    _, b_col, _ = st.columns([0.1, 0.8, 0.1])
    with b_col:
        st.table(blueprint_data)

    st.warning("""
        ### 🧪 Statistical Probability: **67%**
        **Analyst Reality Check:** Meeting these criteria gives a song a **67% chance** of success 
        based on musical DNA. The remaining **33%** is the 'X-Factor' (Marketing, Viral Trends, Artist Brand).
    """)

    st.divider()

    # --- 3. NEXT RECOMMENDED STEPS (The "Strong Closer") ---
    st.header("🚀 Future Roadmap: Expanding the Scope")
    st.write("""
    To move from 67% to 90% accuracy, the next phase of this project must move 
    beyond musical features and integrate external market drivers:
    """)

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("##### **1. Marketing & Investment**")
        st.caption("Integrating Label ad-spend, TikTok viral velocity, and playlist placement data.")
    with s2:
        st.markdown("##### **2. Social Sentiment**")
        st.caption("Analyzing real-time follower growth and audience sentiment on social platforms.")
    with s3:
        st.markdown("##### **3. Cultural Context**")
        st.caption("Mapping regional trends and seasonal preferences (e.g., 'Summer Anthems').")

    # --- 4. FINAL SUMMARY ---
    st.divider()
    st.success("""
    **Project Conclusion:** This analysis proves that while data provides a stable 'floor' 
    for success, the 'ceiling' is determined by human connection and cultural timing. 
    This model acts as a powerful **Risk Mitigation** tool for any music-focused team.
    """)
    
    st.balloons()
