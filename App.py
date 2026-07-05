import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Data Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Background */
.stApp{
    background:#F4F7FC;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0F172A,#2563EB);
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* Main Title */

.main-title{
    font-size:45px;
    text-align:center;
    font-weight:bold;
    color:#2563EB;
}

/* Section */

.section-title{
    color:#1E3A8A;
    font-size:28px;
    font-weight:bold;
}

/* Card */

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 15px rgba(0,0,0,.15);
    margin-bottom:20px;
}

/* Metric */

.metric{
    background:linear-gradient(90deg,#2563EB,#3B82F6);
    color:white;
    border-radius:12px;
    padding:15px;
    text-align:center;
}

/* Button */

.stButton>button{

background:#2563EB;
color:white;
border-radius:10px;
font-weight:bold;
border:none;

}

.stButton>button:hover{

background:#1E40AF;
color:white;

}

/* Download */

.stDownloadButton>button{

background:#16A34A;
color:white;
border-radius:10px;
font-weight:bold;

}

/* Dataframe */

[data-testid="stDataFrame"]{

border-radius:15px;
border:2px solid #2563EB;

}

hr{
border:1px solid #CBD5E1;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.markdown("""
<div class='main-title'>
📊 Streamlit Data Analytics Dashboard
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------
# LOAD DATASETS
# ---------------------------------------------------

iris_path = "data/Iris/iris.csv"

titanic_path = "data/Titanic/Titanic.csv"

medal_path = "data/Medal/Medal.csv"

monthly_path = "data/Monthly Value/Monthly_value.csv"

monthly_df = pd.read_csv(monthly_path)

iris_df = pd.read_csv(iris_path)

titanic_df = pd.read_csv(titanic_path)

medal_df = pd.read_csv(medal_path)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.image(
    "https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png",
    width=180
)

st.sidebar.title("📂 Dashboard Menu")

dataset = st.sidebar.selectbox(

"Choose Dataset",

[
    "Iris Dataset",
    "Titanic Dataset",
    "Medal Dataset"
]

)

st.sidebar.markdown("---")

st.sidebar.info("""

### Dashboard Features

✅ Date Filter

✅ Dataset Explorer

✅ Search Dataset

✅ Summary Statistics

✅ Correlation Matrix

✅ Charts

✅ Plotly Visualizations

✅ Download CSV

✅ Interactive Questions

""")

# ---------------------------------------------------
# SELECT DATASET
# ---------------------------------------------------

if dataset=="Iris Dataset":

    selected_df=iris_df

elif dataset=="Titanic Dataset":

    selected_df=titanic_df

else:

    selected_df=medal_df

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

st.markdown("<hr>",unsafe_allow_html=True)

col1,col2,col3,col4=st.columns(4)

with col1:

    st.metric(
        "Rows",
        selected_df.shape[0]
    )

with col2:

    st.metric(
        "Columns",
        selected_df.shape[1]
    )

with col3:

    st.metric(
        "Missing Values",
        selected_df.isnull().sum().sum()
    )

with col4:

    st.metric(
        "Duplicate Rows",
        selected_df.duplicated().sum()
    )

st.markdown("<hr>",unsafe_allow_html=True)

# =====================================================
# MONTHLY VALUE DASHBOARD
# =====================================================

st.markdown("""
<div class="card">
<h2 class="section-title">📅 Monthly Value Dashboard</h2>
</div>
""", unsafe_allow_html=True)

# Convert Period to datetime
monthly_df["Period"] = pd.to_datetime(monthly_df["Period"])

# Date Slider
min_date = monthly_df["Period"].min().date()
max_date = monthly_df["Period"].max().date()

start_date, end_date = st.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    key="date_slider"
)

filtered_df = monthly_df[
    monthly_df["Period"].between(
        pd.to_datetime(start_date),
        pd.to_datetime(end_date)
    )
]

# =====================================================
# MONTHLY KPI
# =====================================================

k1, k2, k3 = st.columns(3)

with k1:
    st.metric(
        "Filtered Rows",
        len(filtered_df)
    )

with k2:

    if "Value" in filtered_df.columns:
        st.metric(
            "Total Value",
            round(filtered_df["Value"].sum(),2)
        )
    else:
        st.metric("Total Value","N/A")

with k3:

    if "Value" in filtered_df.columns:
        st.metric(
            "Average Value",
            round(filtered_df["Value"].mean(),2)
        )
    else:
        st.metric("Average Value","N/A")

# =====================================================
# FILTERED DATA
# =====================================================

st.markdown("""
<div class="card">
<h4>Filtered Dataset</h4>
</div>
""", unsafe_allow_html=True)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=300
)

st.markdown("<hr>",unsafe_allow_html=True)

# =====================================================
# MONTHLY LINE CHART
# =====================================================

if "Value" in filtered_df.columns:

    st.subheader("📈 Monthly Trend")

    fig = px.line(
        filtered_df,
        x="Period",
        y="Value",
        markers=True
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("<hr>",unsafe_allow_html=True)

# =====================================================
# GLOBAL MAP
# =====================================================

st.markdown("""
<div class="card">
<h2 class="section-title">🌍 Global Cities Map</h2>
</div>
""", unsafe_allow_html=True)

cities = pd.DataFrame({
    "City":[
        "Seoul",
        "Tokyo",
        "New York",
        "Paris",
        "Sydney",
        "London",
        "Cape Town",
        "Johannesburg"
    ],

    "lat":[
        37.5665,
        35.6895,
        40.7128,
        48.8566,
        -33.8688,
        51.5074,
        -33.9249,
        -26.2041
    ],

    "lon":[
        126.9780,
        139.6917,
        -74.0060,
        2.3522,
        151.2093,
        -0.1278,
        18.4241,
        28.0473
    ]
})

left,right = st.columns([1,2])

with left:

    st.subheader("Cities")

    st.dataframe(
        cities,
        use_container_width=True
    )

with right:

    st.subheader("World Map")

    st.map(cities)

st.markdown("<hr>",unsafe_allow_html=True)

# =====================================================
# DATASET OVERVIEW
# =====================================================

st.markdown("""
<div class="card">
<h2 class="section-title">📂 Dataset Overview</h2>
</div>
""", unsafe_allow_html=True)

st.success(f"Current Dataset : {dataset}")

st.dataframe(
    selected_df,
    use_container_width=True,
    height=350
)

# Overview Metrics

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "Rows",
        selected_df.shape[0]
    )

with c2:
    st.metric(
        "Columns",
        selected_df.shape[1]
    )

with c3:
    st.metric(
        "Missing",
        selected_df.isnull().sum().sum()
    )

with c4:
    st.metric(
        "Duplicates",
        selected_df.duplicated().sum()
    )

st.markdown("<hr>",unsafe_allow_html=True)

# =====================================================
# DATASET ANALYSIS
# =====================================================

st.markdown("""
<div class="card">
<h2 class="section-title">📊 Dataset Analysis</h2>
<p>Explore your selected dataset using the options below.</p>
</div>
""", unsafe_allow_html=True)

question = st.selectbox(
    "Choose an Analysis",
    [
        "Show First 5 Rows",
        "Show Last 5 Rows",
        "Dataset Shape",
        "Column Names",
        "Data Types",
        "Missing Values",
        "Summary Statistics",
        "Search Dataset",
        "Select Columns",
        "Random Sample",
        "Download Dataset",
        "Show Entire Dataset"
    ],
    key="analysis1"
)

# =====================================================
# FIRST 5 ROWS
# =====================================================

if question == "Show First 5 Rows":

    st.subheader("First Five Rows")

    st.dataframe(
        selected_df.head(),
        use_container_width=True
    )

# =====================================================
# LAST 5 ROWS
# =====================================================

elif question == "Show Last 5 Rows":

    st.subheader("Last Five Rows")

    st.dataframe(
        selected_df.tail(),
        use_container_width=True
    )

# =====================================================
# SHAPE
# =====================================================

elif question == "Dataset Shape":

    c1,c2 = st.columns(2)

    with c1:
        st.metric(
            "Rows",
            selected_df.shape[0]
        )

    with c2:
        st.metric(
            "Columns",
            selected_df.shape[1]
        )

# =====================================================
# COLUMN NAMES
# =====================================================

elif question == "Column Names":

    st.subheader("Columns")

    st.write(selected_df.columns.tolist())

# =====================================================
# DATA TYPES
# =====================================================

elif question == "Data Types":

    st.subheader("Data Types")

    st.dataframe(
        pd.DataFrame(
            selected_df.dtypes,
            columns=["Data Type"]
        )
    )

# =====================================================
# MISSING VALUES
# =====================================================

elif question == "Missing Values":

    missing = pd.DataFrame({
        "Column":selected_df.columns,
        "Missing":selected_df.isnull().sum().values
    })

    st.dataframe(
        missing,
        use_container_width=True
    )

# =====================================================
# SUMMARY
# =====================================================

elif question == "Summary Statistics":

    st.dataframe(
        selected_df.describe(),
        use_container_width=True
    )

# =====================================================
# SEARCH
# =====================================================

elif question == "Search Dataset":

    search = st.text_input("Search any value")

    if search:

        result = selected_df.astype(str).apply(
            lambda x:
            x.str.contains(
                search,
                case=False
            ).any(),
            axis=1
        )

        st.dataframe(
            selected_df[result],
            use_container_width=True
        )

# =====================================================
# SELECT COLUMNS
# =====================================================

elif question == "Select Columns":

    cols = st.multiselect(
        "Choose Columns",
        selected_df.columns
    )

    if cols:

        st.dataframe(
            selected_df[cols],
            use_container_width=True
        )

# =====================================================
# RANDOM SAMPLE
# =====================================================

elif question == "Random Sample":

    rows = st.slider(
        "Rows",
        1,
        min(20,len(selected_df)),
        5
    )

    st.dataframe(
        selected_df.sample(rows),
        use_container_width=True
    )

# =====================================================
# DOWNLOAD
# =====================================================

elif question == "Download Dataset":

    csv = selected_df.to_csv(index=False)

    st.download_button(
        "⬇ Download CSV",
        csv,
        file_name="dataset.csv",
        mime="text/csv"
    )

# =====================================================
# SHOW ALL
# =====================================================

elif question == "Show Entire Dataset":

    st.dataframe(
        selected_df,
        use_container_width=True,
        height=500
    )

st.markdown("<hr>", unsafe_allow_html=True)

# =====================================================
# ADVANCED DATASET ANALYSIS
# =====================================================

st.markdown("""
<div class="card">
<h2 class="section-title">📈 Advanced Dataset Analysis</h2>
</div>
""", unsafe_allow_html=True)

advanced_question = st.selectbox(
    "Choose Advanced Analysis",
    [
        "Correlation Matrix",
        "Histogram",
        "Box Plot",
        "Scatter Plot",
        "Bar Chart",
        "Pie Chart",
        "Line Chart",
        "Value Counts",
        "Unique Values",
        "Duplicate Rows",
        "Remove Duplicates",
        "Sort Dataset",
        "Filter Numeric Column",
        "Group By Analysis",
        "Correlation Heatmap"
    ],
    key="advanced_analysis"
)

# =====================================================
# CORRELATION MATRIX
# =====================================================

if advanced_question == "Correlation Matrix":

    numeric = selected_df.select_dtypes(include="number")

    if numeric.shape[1] >= 2:

        st.subheader("Correlation Matrix")

        st.dataframe(
            numeric.corr(),
            use_container_width=True
        )

    else:
        st.warning("Dataset has fewer than two numeric columns.")

# =====================================================
# HISTOGRAM
# =====================================================

elif advanced_question == "Histogram":

    numeric = selected_df.select_dtypes(include="number").columns

    if len(numeric):

        column = st.selectbox(
            "Choose Numeric Column",
            numeric
        )

        fig = px.histogram(
            selected_df,
            x=column,
            title=f"Histogram of {column}"
        )

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# BOX PLOT
# =====================================================

elif advanced_question == "Box Plot":

    numeric = selected_df.select_dtypes(include="number").columns

    if len(numeric):

        column = st.selectbox(
            "Choose Numeric Column",
            numeric,
            key="box"
        )

        fig = px.box(
            selected_df,
            y=column,
            title=f"Box Plot of {column}"
        )

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# SCATTER PLOT
# =====================================================

elif advanced_question == "Scatter Plot":

    numeric = selected_df.select_dtypes(include="number").columns

    if len(numeric) >= 2:

        x = st.selectbox(
            "X Axis",
            numeric,
            key="scatterx"
        )

        y = st.selectbox(
            "Y Axis",
            numeric,
            index=1,
            key="scattery"
        )

        fig = px.scatter(
            selected_df,
            x=x,
            y=y,
            title=f"{x} vs {y}"
        )

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# BAR CHART
# =====================================================

elif advanced_question == "Bar Chart":

    column = st.selectbox(
        "Choose Column",
        selected_df.columns,
        key="bar"
    )

    counts = selected_df[column].value_counts().head(10)

    fig = px.bar(
        x=counts.index.astype(str),
        y=counts.values,
        labels={"x":column,"y":"Count"},
        title=f"{column} Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# PIE CHART
# =====================================================

elif advanced_question == "Pie Chart":

    column = st.selectbox(
        "Choose Column",
        selected_df.columns,
        key="pie"
    )

    counts = selected_df[column].value_counts().head(10)

    fig = px.pie(
        names=counts.index,
        values=counts.values,
        title=f"{column} Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# LINE CHART
# =====================================================

elif advanced_question == "Line Chart":

    numeric = selected_df.select_dtypes(include="number").columns

    if len(numeric):

        column = st.selectbox(
            "Choose Column",
            numeric,
            key="line"
        )

        fig = px.line(
            selected_df,
            y=column,
            title=column
        )

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# VALUE COUNTS
# =====================================================

elif advanced_question == "Value Counts":

    column = st.selectbox(
        "Choose Column",
        selected_df.columns,
        key="counts"
    )

    st.dataframe(
        selected_df[column].value_counts(),
        use_container_width=True
    )

# =====================================================
# UNIQUE VALUES
# =====================================================

elif advanced_question == "Unique Values":

    column = st.selectbox(
        "Choose Column",
        selected_df.columns,
        key="unique"
    )

    st.write(selected_df[column].unique())

# =====================================================
# DUPLICATE ROWS
# =====================================================

elif advanced_question == "Duplicate Rows":

    duplicates = selected_df[selected_df.duplicated()]

    st.write(f"Duplicate Rows: {duplicates.shape[0]}")

    st.dataframe(
        duplicates,
        use_container_width=True
    )

# =====================================================
# REMOVE DUPLICATES
# =====================================================

elif advanced_question == "Remove Duplicates":

    cleaned = selected_df.drop_duplicates()

    st.success(
        f"Rows before: {len(selected_df)}"
    )

    st.success(
        f"Rows after: {len(cleaned)}"
    )

    st.dataframe(
        cleaned,
        use_container_width=True
    )

# =====================================================
# SORT DATASET
# =====================================================

elif advanced_question == "Sort Dataset":

    column = st.selectbox(
        "Sort By",
        selected_df.columns,
        key="sort"
    )

    ascending = st.checkbox(
        "Ascending",
        True
    )

    st.dataframe(
        selected_df.sort_values(
            column,
            ascending=ascending
        ),
        use_container_width=True
    )

# =====================================================
# FILTER NUMERIC COLUMN
# =====================================================

elif advanced_question == "Filter Numeric Column":

    numeric = selected_df.select_dtypes(include="number").columns

    if len(numeric):

        column = st.selectbox(
            "Choose Numeric Column",
            numeric,
            key="filter"
        )

        minimum = float(selected_df[column].min())
        maximum = float(selected_df[column].max())

        value = st.slider(
            "Minimum Value",
            minimum,
            maximum,
            minimum
        )

        st.dataframe(
            selected_df[
                selected_df[column] >= value
            ],
            use_container_width=True
        )

# =====================================================
# GROUP BY ANALYSIS
# =====================================================

elif advanced_question == "Group By Analysis":

    cat = selected_df.select_dtypes(
        exclude="number"
    ).columns

    num = selected_df.select_dtypes(
        include="number"
    ).columns

    if len(cat) and len(num):

        group = st.selectbox(
            "Category",
            cat
        )

        value = st.selectbox(
            "Numeric",
            num
        )

        grouped = selected_df.groupby(group)[value].mean().reset_index()

        st.dataframe(grouped)

        fig = px.bar(
            grouped,
            x=group,
            y=value,
            title=f"Average {value} by {group}"
        )

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# HEATMAP
# =====================================================

elif advanced_question == "Correlation Heatmap":

    numeric = selected_df.select_dtypes(include="number")

    if numeric.shape[1] >= 2:

        fig = px.imshow(
            numeric.corr(),
            text_auto=True,
            color_continuous_scale="Blues",
            title="Correlation Heatmap"
        )

        st.plotly_chart(fig, use_container_width=True)
    
# =====================================================
# PROFESSIONAL DASHBOARD
# =====================================================

st.markdown("""
<div class="card">
<h2 class="section-title">📊 Interactive Dashboard</h2>
</div>
""", unsafe_allow_html=True)

numeric_cols = selected_df.select_dtypes(include="number").columns.tolist()
categorical_cols = selected_df.select_dtypes(exclude="number").columns.tolist()

# Dashboard Filters
col1, col2 = st.columns(2)

with col1:
    chart_type = st.selectbox(
        "Select Chart",
        [
            "Bar Chart",
            "Pie Chart",
            "Line Chart",
            "Scatter Plot",
            "Histogram",
            "Box Plot",
            "Area Chart",
            "Violin Plot"
        ]
    )

with col2:
    theme = st.selectbox(
        "Chart Theme",
        [
            "plotly",
            "plotly_white",
            "ggplot2",
            "seaborn",
            "simple_white"
        ]
    )

# =====================================================
# BAR CHART
# =====================================================

if chart_type == "Bar Chart":

    if len(categorical_cols) > 0:

        column = st.selectbox(
            "Choose Category",
            categorical_cols
        )

        counts = selected_df[column].value_counts().reset_index()

        counts.columns = [column, "Count"]

        fig = px.bar(
            counts,
            x=column,
            y="Count",
            color="Count",
            template=theme,
            title=f"{column} Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# PIE CHART
# =====================================================

elif chart_type == "Pie Chart":

    if len(categorical_cols) > 0:

        column = st.selectbox(
            "Choose Category",
            categorical_cols,
            key="pie2"
        )

        counts = selected_df[column].value_counts().reset_index()

        counts.columns = [column, "Count"]

        fig = px.pie(
            counts,
            names=column,
            values="Count",
            hole=.45,
            template=theme
        )

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# LINE CHART
# =====================================================

elif chart_type == "Line Chart":

    if len(numeric_cols):

        column = st.selectbox(
            "Choose Numeric Column",
            numeric_cols
        )

        fig = px.line(
            selected_df,
            y=column,
            markers=True,
            template=theme
        )

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# SCATTER
# =====================================================

elif chart_type == "Scatter Plot":

    if len(numeric_cols) >= 2:

        x = st.selectbox(
            "X Axis",
            numeric_cols
        )

        y = st.selectbox(
            "Y Axis",
            numeric_cols,
            index=1
        )

        fig = px.scatter(
            selected_df,
            x=x,
            y=y,
            color=y,
            size=y,
            template=theme
        )

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# HISTOGRAM
# =====================================================

elif chart_type == "Histogram":

    column = st.selectbox(
        "Choose Column",
        numeric_cols
    )

    fig = px.histogram(
        selected_df,
        x=column,
        color_discrete_sequence=["royalblue"],
        template=theme
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# BOX PLOT
# =====================================================

elif chart_type == "Box Plot":

    column = st.selectbox(
        "Choose Column",
        numeric_cols
    )

    fig = px.box(
        selected_df,
        y=column,
        points="all",
        template=theme
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# AREA CHART
# =====================================================

elif chart_type == "Area Chart":

    column = st.selectbox(
        "Choose Column",
        numeric_cols
    )

    fig = px.area(
        selected_df,
        y=column,
        template=theme
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# VIOLIN PLOT
# =====================================================

elif chart_type == "Violin Plot":

    column = st.selectbox(
        "Choose Column",
        numeric_cols
    )

    fig = px.violin(
        selected_df,
        y=column,
        box=True,
        template=theme
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# DASHBOARD METRICS
# =====================================================

st.subheader("📈 Dataset Metrics")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Rows", len(selected_df))

with m2:
    st.metric("Columns", len(selected_df.columns))

with m3:
    st.metric("Missing Values", selected_df.isnull().sum().sum())

with m4:
    st.metric("Duplicates", selected_df.duplicated().sum())

# =====================================================
# NUMERIC SUMMARY
# =====================================================

if len(numeric_cols):

    st.subheader("📋 Numeric Summary")

    summary = pd.DataFrame({
        "Minimum": selected_df[numeric_cols].min(),
        "Maximum": selected_df[numeric_cols].max(),
        "Average": selected_df[numeric_cols].mean(),
        "Median": selected_df[numeric_cols].median(),
        "Std Dev": selected_df[numeric_cols].std()
    })

    st.dataframe(summary, use_container_width=True)

st.divider()

# =====================================================
# PART 6 - PROFESSIONAL FOOTER & EXTRA FEATURES
# =====================================================

st.divider()

st.markdown("""
<div class="card">
<h2 class="section-title">⚙ Dashboard Settings</h2>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# DARK MODE
# -----------------------------------------------------

dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:

    st.markdown("""
    <style>

    .stApp{
        background:#111827;
        color:white;
    }

    h1,h2,h3,h4,h5,h6,p,label{
        color:white !important;
    }

    section[data-testid="stSidebar"]{
        background:#000000;
    }

    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------
# EXPORT DATA
# -----------------------------------------------------

st.subheader("📥 Export Dataset")

csv = selected_df.to_csv(index=False)

st.download_button(
    "Download Selected Dataset",
    csv,
    file_name=f"{dataset}.csv",
    mime="text/csv"
)

st.divider()

# =====================================================
# DATASET INFORMATION
# =====================================================

st.markdown("""
<div class="card">
<h2 class="section-title">📚 Dataset Information</h2>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:

    st.write("### General Information")

    st.write(f"**Dataset Name:** {dataset}")
    st.write(f"**Rows:** {selected_df.shape[0]}")
    st.write(f"**Columns:** {selected_df.shape[1]}")
    st.write(f"**Missing Values:** {selected_df.isnull().sum().sum()}")
    st.write(f"**Duplicate Rows:** {selected_df.duplicated().sum()}")

with c2:

    st.write("### Numeric Columns")

    numeric = selected_df.select_dtypes(include="number").columns

    if len(numeric):

        st.write(list(numeric))

    else:

        st.info("No numeric columns found.")

st.divider()

# =====================================================
# ABOUT PROJECT
# =====================================================

st.markdown("""
<div class="card">

<h2 class="section-title">
👨‍💻 About This Dashboard
</h2>

This dashboard was developed using:

<ul>

<li>🐍 Python</li>

<li>📊 Streamlit</li>

<li>🐼 Pandas</li>

<li>📈 Plotly</li>

<li>📉 Matplotlib</li>

<li>📂 CSV Datasets</li>

</ul>

The purpose of this project is to provide an interactive data analytics dashboard
where users can explore datasets, generate charts, analyze statistics,
and visualize data in real time.

</div>
""", unsafe_allow_html=True)

st.divider()

# =====================================================
# TECHNOLOGIES
# =====================================================

st.subheader("🚀 Technologies Used")

tech1, tech2, tech3, tech4 = st.columns(4)

with tech1:
    st.info("🐍 Python")

with tech2:
    st.info("📊 Streamlit")

with tech3:
    st.info("📈 Plotly")

with tech4:
    st.info("🐼 Pandas")

st.divider()

# =====================================================
# CONTACT
# =====================================================

st.subheader("📞Software Developer")

st.success("Name: Sello Derick Maila")

st.info("Email: dericksello794@gmail.com")

st.info("Phone: +27 79 266 0510")

st.info("University: Nelson Mandela University")

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<style>

.footer{

position:fixed;

left:0;

bottom:0;

width:100%;

background:#2563EB;

color:white;

text-align:center;

padding:12px;

font-size:16px;

font-weight:bold;

}

</style>

<div class="footer">

🚀 Developed by Sello Derick Maila |
Samsung Innovation Campus |
Python • Streamlit • Data Analytics • Machine Learning

</div>

""", unsafe_allow_html=True)