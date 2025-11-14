import streamlit as st
import pandas as pd

# The actual page content is executed here by Streamlit
st.title("Crystal Zhao: Popular Articles' Edits Analysis")
st.markdown("---")

# Retrieve shared data from the Home page's session state

DATA_FILE_KEY = 'st02_data'

if 'student_data' in st.session_state and DATA_FILE_KEY in st.session_state['student_data']:
    df = st.session_state['student_data'][DATA_FILE_KEY]
else:
    df = None

if df is None or df.empty:
    st.warning("Data not loaded. Please ensure the Home Page ran successfully and the data files exist.")
else:
    # Your original logic continues here
    # --- Student Introductory Section ---
    st.header("1. Introduction and Project Goal")
    st.markdown("""
        **Data Description:** .
        
        **Question:** 
        
        **Interaction:** Use the selection box below to 
    """)
    st.markdown("---")
    
    # --- Analysis Controls (Moved from Sidebar to Main Page) ---
    col_control, col_spacer = st.columns([1, 3])
    with col_control:
        article_filter = st.selectbox(
            "Select Article to Analyze:", 
            df['article'].unique()
        )
    
    # Filter data for the selected team (as Home Team)
    article = df[df['article'] == article_filter].copy()
    article_df = pd.DataFrame(article)
    
    # --- Analysis Content ---
    if article_df.empty:
        st.info(f"No home games found for the team '{article_filter}' in the dataset to analyze.")
    else:
        st.subheader(f"2. Patterns in Edits For {article_filter}")
        
        col1, col2 = st.columns(2)
        
        # edits per article by month
        article_monthly_edits = article_df.groupby('year_month')['revid'].count().reset_index(name='edits')

        total_edits = len(article_df)
        total_users = article_df['user'].nunique()
        
        with col1:
            st.metric(
                label="Total Edits Analyzed", 
                value=f"{total_edits:,.0f}"
            )
            # Display Top 5 Most Active Users
            top_users = article_df['user'].value_counts().head(5).to_frame(name='Edits')
            st.markdown("**Top 5 Active Users (by edit count):**")
            st.dataframe(top_users, use_container_width=True)

        with col2:
            st.metric(
                label="Total Unique Users", 
                value=f"{total_users:,.0f}"
            )
            # Bar chart showing edit size distribution instead of sports attendance
            st.markdown("**Edit Size Distribution (First 100 Edits):**")
            st.bar_chart(article_df.head(100).set_index('time')['size'])

        st.subheader(f"3. Monthly Edit Frequency for {article_filter}")
        
        # Prepare data for st.line_chart: set 'year_month' as index
        df_chart_data = article_monthly_edits.set_index('year_month')[['edits']]
        
        st.line_chart(
            df_chart_data,
            y='edits'
        )
        
        st.caption("X-axis: Year-Month, Y-axis: Number of Edits")