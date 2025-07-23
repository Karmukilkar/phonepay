import streamlit as st
import pymysql
import os
import mysql.connector
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

def get_connection():
    return pymysql.connect(
        host= "localhost",
        user="demo",
        password="Kart123@",
        database="phonepay"
    )

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


with st.sidebar:
    st.image(
        "download.png",
        use_container_width=True
    )

    st.title("📌 Navigation")
    menu = st.radio("Go to", ["🏠 Home", "👥 Users", "💳 Transactions", "🛡️ Insurance", "ℹ️ About"])

    st.markdown("---")
    st.markdown("**📅 Tip:** Use the main page to select year & filters.")
    st.markdown("Developed by [Karthik Mohan](https://github.com/Karmukilkar/phonepay)")
    st.markdown("🔗 [GitHub](https://github.com/Karmukilkar/phonepay)")



if menu == "🏠 Home":
    st.header("Welcome to the PhonePe Pulse Data Dashboard!")
    st.markdown("""
    This dashboard allows you to explore PhonePe Pulse data interactively.
    ...
    """)
    st.info("Use the sidebar to navigate to Users, Transactions, or Insurance sections.")

    st.markdown("## Users by State (India Map)")
    Year = st.radio("Select Year", [2018, 2019, 2020, 2021, 2022], index=4)

    try:
        agg_user_df = pd.read_csv("Aggercated_User.csv")

        if "Year" not in agg_user_df.columns:
            st.error("Column 'Year' not found in CSV.")
        else:
            df_year = agg_user_df[agg_user_df["Year"] == Year]
            state_users = df_year.groupby("State")["User_count"].sum().reset_index()

            india_geojson = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            fig = px.choropleth(
                state_users,
                geojson=india_geojson,
                featureidkey="properties.ST_NM",
                locations="State",
                color="User_count",
                color_continuous_scale="Blues",
                title=f"Number of Users by State in India ({Year})",
                width=500,
                height=500
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.info(f"Could not load Aggregated Users map: {e}")




elif menu == "👥 Users":
    st.header("Users Data")
    st.markdown("Explore user demographics and statistics.")

    # 👉 Year selector
    selected_year = st.radio(
        "Select Year",
        [2018, 2019, 2020, 2021, 2022, 2023],
        index=5
    )

    try:
        
        top_states_query = f"""
            SELECT State, SUM(User_count) AS Total_Users
            FROM agg_user
            WHERE Year = {selected_year}
            GROUP BY State
            ORDER BY Total_Users DESC
            LIMIT 10;
        """
        top_states_df = run_query(top_states_query)

        
        bottom_states_query = f"""
            SELECT State, SUM(User_count) AS Total_Users
            FROM agg_user
            WHERE Year = {selected_year}
            GROUP BY State
            ORDER BY Total_Users ASC
            LIMIT 10;
        """
        bottom_states_df = run_query(bottom_states_query)

       
        growth_query = """
            SELECT Year, State, SUM(User_count) AS Total_Users
            FROM agg_user
            GROUP BY Year, State
            ORDER BY Year ASC, State;
        """
        growth_df = run_query(growth_query)

       
        full_table_query = f"""
            SELECT State, SUM(User_count) AS Total_Users
            FROM agg_user
            WHERE Year = {selected_year}
            GROUP BY State
            ORDER BY State ASC;
        """
        full_table_df = run_query(full_table_query)

        # 👉 Charts
        st.markdown(f"### Top 10 States by User Count in {selected_year}")
        fig1 = px.pie(
            top_states_df, names='State', values='Total_Users',
            title=f'Top 10 States by Total Users ({selected_year})',
            hole=0.3
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown(f"### Bottom 10 States by User Count in {selected_year}")
        fig2 = px.bar(
            bottom_states_df, x='Total_Users', y='State',
            orientation='h',
            title=f'Bottom 10 States by Total Users ({selected_year})'
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Yearly User Growth by State")
        fig3 = px.line(
            growth_df, x='Year', y='Total_Users',
            color='State',
            title='User Growth by State Over the Years'
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown(f"### All States - User Count in {selected_year}")
        st.dataframe(full_table_df)
        csv = full_table_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f'users_by_state_{selected_year}.csv',
            mime='text/csv'
        )

    except Exception as e:
        st.error(f"Could not load Users data: {e}")


elif menu == "💳 Transactions":
    st.header("Transactions - State Performance Over Time")
    st.markdown("""
    This chart shows how states have performed over time.
    You can filter states and highlight those with the highest growth.
    """)

    try:
        
        trend_query = """
            SELECT Year, State, SUM(Transaction_amount) AS Total_Amount
            FROM agg_transaction
            WHERE Transaction_amount IS NOT NULL
            GROUP BY Year, State
            ORDER BY Year ASC, State;
        """
        trend_df = run_query(trend_query)

        
        first_year = trend_df['Year'].min()
        last_year = trend_df['Year'].max()

        first_year_df = trend_df[trend_df['Year'] == first_year]
        last_year_df = trend_df[trend_df['Year'] == last_year]

        growth_df = last_year_df.merge(
            first_year_df,
            on='State',
            suffixes=('_last', '_first')
        )

        growth_df['Growth'] = ((growth_df['Total_Amount_last'] - growth_df['Total_Amount_first']) /
                               growth_df['Total_Amount_first']) * 100

        
        top_risers = growth_df[growth_df['Growth'] > 200].sort_values(by='Growth', ascending=False)

      
        states = trend_df['State'].unique().tolist()
        selected_states = st.multiselect(
            "Select States to Show",
            options=states,
            default=top_risers['State'].tolist() if not top_risers.empty else states
        )

        
        filtered_trend_df = trend_df[trend_df['State'].isin(selected_states)]

      
        fig = px.line(
            filtered_trend_df,
            x='Year',
            y='Total_Amount',
            color='State',
            title='State Transaction Amount Trend Over Years',
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🚀 States with Highest Growth")
        if not top_risers.empty:
            st.dataframe(
                top_risers[['State', 'Total_Amount_first', 'Total_Amount_last', 'Growth']]
                .rename(columns={
                    'Total_Amount_first': f'Total in {first_year}',
                    'Total_Amount_last': f'Total in {last_year}',
                    'Growth': 'Growth (%)'
                })
                .sort_values(by='Growth', ascending=False)
            )
        else:
            st.info("No high-growth states found based on your data.")

    except Exception as e:
        st.error(f"Could not load trend data: {e}")

            # ---------------------------------------------------------------

    st.markdown("## 📊 Transaction Type Distribution")
    st.markdown("""
    Select Year and Quarter to see the distribution of transaction types.
    """)

    available_years = sorted(trend_df['Year'].unique())
    selected_year = st.selectbox("Select Year", options=available_years, index=len(available_years)-1)   
    
    quarter_df = run_query("SELECT DISTINCT Quater FROM agg_transaction ORDER BY Quater;")
    available_quarters = quarter_df['Quater'].tolist()
    selected_quarter = st.selectbox("Select Quarter", options=available_quarters)

    try:
        type_query = f"""
            SELECT Transaction_type, SUM(Transaction_amount) AS Total_Amount
            FROM agg_transaction
            WHERE Year = {selected_year} AND Quater = {selected_quarter}
            GROUP BY Transaction_type
            ORDER BY Total_Amount DESC;
        """

        type_df = run_query(type_query)

        fig_type = px.pie(
            type_df,
            names='Transaction_type',
            values='Total_Amount',
            title=f'Transaction Type Share - {selected_year} Q{selected_quarter}',
            hole=0.4
        )

        st.plotly_chart(fig_type, use_container_width=True)

    except Exception as e:
        st.error(f"Could not load Transaction Type data: {e}")


elif menu == "🛡️ Insurance":
    st.header("🛡️ Insurance Dashboard")
    st.markdown("Dive into insurance transactions with unique visuals!")

    
    selected_year = st.selectbox("Year", [2018, 2019, 2020, 2021, 2022, 2023], index=5)
    selected_state = st.selectbox(
        "State",
        ["All"] + ["Andhra Pradesh", "Karnataka", "Maharashtra", "Tamil Nadu", "Kerala"]
    )

    try:
        
        treemap_query = f"""
            SELECT State, SUM(Transaction_amount) AS Total_Amount
            FROM agg_insurance
            WHERE Year = {selected_year}
            GROUP BY State
            ORDER BY Total_Amount DESC
            LIMIT 15;
        """
        treemap_df = run_query(treemap_query)

        st.markdown("### 🌳 States by Insurance Amount")
        fig1 = px.treemap(
            treemap_df,
            path=['State'],
            values='Total_Amount',
            color='Total_Amount',
            color_continuous_scale='plasma',
            title='Treemap of Insurance by State'
        )
        st.plotly_chart(fig1, use_container_width=True)

       
       
        heatmap_query = """
            SELECT Year, Quater, SUM(Transaction_amount) AS Total_Amount
            FROM agg_insurance
            GROUP BY Year, Quater
            ORDER BY Year, Quater;
        """
        heatmap_df = run_query(heatmap_query)

        st.markdown("### 🔥 Insurance Heatmap (Year vs Quarter)")
        fig3 = px.density_heatmap(
            heatmap_df,
            x='Quater',
            y='Year',
            z='Total_Amount',
            color_continuous_scale='Viridis',
            title='Insurance Amount by Year & Quarter'
        )
        st.plotly_chart(fig3, use_container_width=True)

    except Exception as e:
        st.error(f"Could not load Insurance data: {e}")



elif menu == "ℹ️ About":
    st.header("About 📚")
    st.markdown("""
    ## 👋 Hi, I'm Karthik Mohan

    Welcome to the **PhonePe Pulse Data Dashboard** — an interactive data app built to analyze and visualize India’s digital payment trends using PhonePe Pulse data.

    ---
    ## 📌 What is this Project?

    - 📈 **Visualize:** Explore user growth, transaction trends, and insurance insights.
    - 🗺️ **Maps & Charts:** Interactive charts, filters by year and quarter.
    - ⚙️ **Tech Stack:** Python · Streamlit · Plotly · MySQL

    ---
    ## 🎯 Why did I build this?

    - To showcase **real-world data skills**: ETL, SQL queries, data visualization.
    - To practice building **dynamic dashboards** for business insights.
    - To demonstrate how to connect **Python with live databases** securely.

    ---
    ## 🚀 Connect with Me

    - 🔗 [GitHub](https://github.com/Karmukilkar/phonepay)
    - 💼 [LinkedIn](https://www.linkedin.com/in/karthik-murugan-b1a14724a/overlay/about-this-profile/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3B9Guf8AuLSD%2BAXLGoXFweMA%3D%3D)
    

    ---
    **Thanks for visiting!** 👋  
    Feel free to connect if you’d like to discuss data, analytics, or dashboards.
    """)
