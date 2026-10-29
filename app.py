import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Scientific Visualisation Report - JIE42403",
    layout="wide"
)

st.title("📊 Scientific Visualisation Report")
st.caption("Course Code: JIE42403 | Scientific Visualisation Assignment")

# Sidebar Navigasi Berdasarkan 3 Objektif Utama
page = st.sidebar.radio("Select Objective Page:", [
    "Page 1: Socioeconomic & Demographic Trends Over Time",
    "Page 2: Demographic & Group Comparisons",
    "Page 3: Cross-Dataset Patterns & Correlations"
])

# Fungsi Muat Naik Data & Pembersihan Data
@st.cache_data
def load_data():
    income = pd.read_csv("income.csv")
    crime = pd.read_csv("crime.csv")
    marriages = pd.read_csv("marriages_age.csv")
    
    # Penukaran format tarikh & tahun
    for df in [income, crime, marriages]:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
        
    # Pembersihan Data Pendapatan
    income['income'] = pd.to_numeric(income['income'], errors='coerce')
    income['state'] = income['state'].astype(str).str.strip()
    income_mean = income[income['variable'].astype(str).str.lower() == 'mean'].dropna(subset=['income']).copy()
    
    # Pembersihan Data Banduan
    crime['state'] = crime['state'].astype(str).str.strip()
    crime['sex'] = crime['sex'].astype(str).str.strip().str.lower()
    crime['prisoners'] = pd.to_numeric(crime['prisoners'], errors='coerce')
    
    # Pembersihan Data Perkahwinan
    marriages['sex'] = marriages['sex'].astype(str).str.strip().str.lower()
    marriages['age'] = marriages['age'].astype(str).str.strip()
    marriages['abs'] = pd.to_numeric(marriages['abs'], errors='coerce')
    
    return income_mean, crime, marriages

inc_df, crime_df, mar_df = load_data()

# ---------------------------------------------------------
# PAGE 1: OBJECTIVE 1 (TEMPORAL TRENDS OVER TIME)
# ---------------------------------------------------------
if page == "Page 1: Socioeconomic & Demographic Trends Over Time":
    st.header("Page 1: Socioeconomic and Demographic Trends Over Time")
    
    st.info("**Objective 1:** To identify and compare trends and changes in Malaysia’s socioeconomic and demographic statistics over time.")
    
    # Summary Box
    st.subheader("📌 Summary Box")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Latest Avg Income (2024)", f"RM {inc_df[inc_df['year']==2024]['income'].mean():,.2f}")
    with col2:
        st.metric("Latest Total Prisoners (2024)", f"{crime_df[(crime_df['year']==2024)&(crime_df['state'].str.lower()=='malaysia')&(crime_df['sex']=='both')]['prisoners'].sum():,}")
    with col3:
        st.metric("Total Marriages Recorded (All Years)", f"{mar_df[mar_df['age'].str.lower()!='all']['abs'].sum():,}")
        
    st.markdown("---")
    st.subheader("📈 Visualizations (3 Visualizations)")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        inc_year = inc_df.groupby('year', as_index=False)['income'].mean()
        fig1 = px.line(inc_year, x='year', y='income', markers=True, title="1. Mean Household Income Trend", labels={'year':'Year', 'income':'Mean Income (RM)'})
        st.plotly_chart(fig1, use_container_width=True)
        
    with c2:
        mal_crime = crime_df[(crime_df['state'].str.lower()=='malaysia') & (crime_df['sex']=='both')]
        fig2 = px.line(mal_crime, x='year', y='prisoners', markers=True, title="2. Malaysia Total Prisoner Trend", labels={'year':'Year', 'prisoners':'Prisoner Count'})
        st.plotly_chart(fig2, use_container_width=True)
        
    with c3:
        mar_year = mar_df[mar_df['age'].str.lower()!='all'].groupby('year', as_index=False)['abs'].sum()
        fig3 = px.line(mar_year, x='year', y='abs', markers=True, title="3. Annual Total Marriage Registration Trend", labels={'year':'Year', 'abs':'Total Marriages'})
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("💡 Interpretation & Discussion")
    st.write("""
    - **Income Growth:** Average household income shows a steady upward trajectory across recorded survey years (2019–2024).
    - **Prisoner Fluctuations:** Total prisoner counts peaked around 2019 before experiencing a drop in 2020–2021, followed by a gradual increase towards 2024.
    - **Marriage Registration Trends:** Annual marriage volume exhibits cyclical changes with noticeable stability in post-2021 periods.
    """)

# ---------------------------------------------------------
# PAGE 2: OBJECTIVE 2 (GROUP & DEMOGRAPHIC COMPARISONS)
# ---------------------------------------------------------
elif page == "Page 2: Demographic & Group Comparisons":
    st.header("Page 2: Group Differences Across Income, Prisoner, and Marriage Data")
    
    st.info("**Objective 2:** To compare differences between relevant groups across Malaysia’s household income, prisoner, and marriage statistics.")
    
    # Summary Box
    st.subheader("📌 Summary Box")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Highest State Avg Income", f"RM {inc_df.groupby('state')['income'].mean().max():,.2f}")
    with col2:
        males = crime_df[crime_df['sex']=='male']['prisoners'].sum()
        total_p = crime_df[crime_df['sex'].isin(['male','female'])]['prisoners'].sum()
        st.metric("Male Prisoner Percentage", f"{(males/total_p)*100:.1f}%")
    with col3:
        st.metric("Peak Marriage Age Bracket", "25 - 29")
        
    st.markdown("---")
    st.subheader("📈 Visualizations (3 Visualizations)")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        inc_state = inc_df.groupby('state', as_index=False)['income'].mean().sort_values('income', ascending=False)
        fig1 = px.bar(inc_state, x='state', y='income', title="1. Mean Income Comparison by State", labels={'state':'State', 'income':'Mean Income (RM)'})
        st.plotly_chart(fig1, use_container_width=True)
        
    with c2:
        sex_crime = crime_df[(crime_df['sex'].isin(['male','female'])) & (crime_df['state'].str.lower()!='malaysia')].groupby(['year','sex'], as_index=False)['prisoners'].sum()
        fig2 = px.bar(sex_crime, x='year', y='prisoners', color='sex', barmode='group', title="2. Prisoner Counts by Gender Group", labels={'year':'Year', 'prisoners':'Count', 'sex':'Gender'})
        st.plotly_chart(fig2, use_container_width=True)
        
    with c3:
        mar_age = mar_df[mar_df['age'].str.lower()!='all'].groupby(['age','sex'], as_index=False)['abs'].sum()
        fig3 = px.bar(mar_age, x='age', y='abs', color='sex', barmode='group', title="3. Marriage Counts by Age Group & Sex", labels={'age':'Age Group', 'abs':'Total Marriages', 'sex':'Gender'})
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("💡 Interpretation & Discussion")
    st.write("""
    - **Regional Income Gap:** Highly urbanized areas (e.g., Kuala Lumpur, Selangor) record substantially higher average household income compared to other states.
    - **Gender Disparity in Prisoners:** Male prisoners account for the vast majority of prisoner populations consistently across all observed years.
    - **Age Dynamics in Marriage:** Marriage counts peak prominently in the 25–29 age bracket for both males and females before tapering off in older groups.
    """)

# ---------------------------------------------------------
# PAGE 3: OBJECTIVE 3 (CROSS-DATASET PATTERNS & CORRELATIONS)
# ---------------------------------------------------------
elif page == "Page 3: Cross-Dataset Patterns & Correlations":
    st.header("Page 3: Cross-Dataset Patterns and Synthesis")
    
    st.info("**Objective 3:** To examine similarities and differences in the patterns observed across Malaysia’s economic and social datasets.")
    
    # Summary Box
    st.subheader("📌 Summary Box")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Income Inequality Gap", "High Top-Percentile Growth")
    with col2:
        st.metric("High-Density State Crime", "Concentrated in Urban States")
    with col3:
        st.metric("Demographic Shift", "Marriage Concentrated in Young Adults")
        
    st.markdown("---")
    st.subheader("📈 Visualizations (3 Visualizations)")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        p_inc = inc_df.pivot_table(index='state', columns='percentile', values='income', aggfunc='mean')
        fig1 = px.imshow(p_inc, aspect='auto', color_continuous_scale='Blues', title="1. Income Heatmap (State vs Percentile)", labels={'x':'Percentile', 'y':'State', 'color':'RM'})
        st.plotly_chart(fig1, use_container_width=True)
        
    with c2:
        state_crime = crime_df[crime_df['state'].str.lower()!='malaysia'].pivot_table(index='state', columns='year', values='prisoners', aggfunc='sum')
        fig2 = px.imshow(state_crime, aspect='auto', color_continuous_scale='YlOrRd', title="2. Prisoner Heatmap (State vs Year)", labels={'x':'Year', 'y':'State', 'color':'Count'})
        st.plotly_chart(fig2, use_container_width=True)
        
    with c3:
        mar_pivot = mar_df[mar_df['age'].str.lower()!='all'].pivot_table(index='age', columns='year', values='abs', aggfunc='sum')
        fig3 = px.imshow(mar_pivot, aspect='auto', color_continuous_scale='Viridis', title="3. Marriage Heatmap (Age Group vs Year)", labels={'x':'Year', 'y':'Age Group', 'color':'Count'})
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("💡 Interpretation & Discussion")
    st.write("""
    - **Economic Distribution:** The income heatmap highlights steep vertical gradients at upper percentiles across all states, revealing income inequality.
    - **Socio-Geographic Patterns:** Highly populated and economic-hub states (e.g., Selangor) display higher prisoner volumes parallel to higher average income levels.
    - **Demographic Synthesis:** Combining demographic marriage age concentration with socioeconomic distribution provides a holistic view of social transitions in Malaysia.
    """)
