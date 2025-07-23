
# 📊 PhonePe Pulse Data Dashboard

Welcome! 👋

This project is a labor of love for data, technology, and India's digital transformation. Dive in to explore, analyze, and visualize the story of digital payments across the country—powered by real PhonePe Pulse data and built for curious minds like yours.

---

---


## 🚀 Features
- **Visualize** user growth, transaction trends, and insurance insights
- **Interactive maps & charts** (Pie, Bar, Line, Treemap, Heatmap)
- **Filter by year, quarter, and state**
- **Downloadable tables** for further analysis
- **Live MySQL connection** for dynamic queries
- **Intuitive UI**: Designed for both data enthusiasts and business users

---


## 🛠️ Tech Stack
- Python 3.8+
- Streamlit
- Plotly
- MySQL
- Pandas

---


## 📦 Setup Instructions

1. **Clone the repository**
   ```sh
   git clone https://github.com/your-github-profile/phonepay.git
   cd phonepay
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up MySQL database**
   - Create a MySQL database (e.g., `phonepay`)
   - Import your PhonePe Pulse data into tables (`agg_user`, `agg_transaction`, `agg_insurance`, etc.)
   - Set your DB credentials as environment variables:
     - `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`

4. **Run the app**
   ```sh
   streamlit run steam.py
   ```

---


## 🖥️ Dashboard Pages
- **Home:** Overview, India map of users by state
- **Users:** Top/bottom states, growth trends, download tables
- **Transactions:** State performance, transaction type share
- **Insurance:** Treemap, heatmap, state-wise analysis
- **About:** Project info, my story, and how to connect

---


## 📁 Project Structure
```
project-phonepay/
├── steam.py              # Main Streamlit app
├── requirements.txt      # Python dependencies
├── Aggercated_User.csv   # Example CSV for user map
├── ...                   # Other CSVs, images, etc.
```

---


## 👤 About the Author

Hi, I'm **Karthik Mohan**—a passionate data enthusiast, Pythonista, and builder of things that make data come alive. I believe in the power of open data and visualization to tell stories, drive decisions, and spark curiosity.

This dashboard is my way of giving back to the community and learning in public. If you have ideas, feedback, or just want to talk data, feel free to connect!

- [GitHub](https://github.com/Karmukilkar/phonepay)
- [LinkedIn](https://www.linkedin.com/in/karthik-murugan-b1a14724a/overlay/about-this-profile/)

---


## 📄 License
This project is for educational and demonstration purposes only. If you find it useful or inspiring, let me know!

---


---

**Thank you for visiting! Wishing you happy exploring, learning, and building. 🚀**

