import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Steel Plant Exposure Dashboard",
    page_icon="🏭",
    layout="wide"
)


@st.cache_data
def load_data():
    return pd.read_csv("plant_exposure.csv")

plant_data = load_data()

# Make sure numeric columns are numeric
plant_data["total_capacity"] = pd.to_numeric(
    plant_data["total_capacity"], errors="coerce"
)

plant_data["LitPop_value"] = pd.to_numeric(
    plant_data["LitPop_value"], errors="coerce"
)


st.title("🏭 Steel Plant Exposure Dashboard")

st.write(
    """
    Explore steel plant capacity and local LitPop exposure
    across China, India, and Japan.
    """
)


st.sidebar.header("Filters")

countries = sorted(
    plant_data["Country/area"].dropna().unique()
)

selected_countries = st.sidebar.multiselect(
    "Country",
    countries,
    default=countries
)

companies = sorted(
    plant_data["Owner"].dropna().unique()
)

selected_companies = st.sidebar.multiselect(
    "Company",
    companies,
    default=companies
)


filtered_data = plant_data[
    plant_data["Country/area"].isin(selected_countries)
    & plant_data["Owner"].isin(selected_companies)
].copy()

st.subheader("Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Plants",
    filtered_data["GEM plant ID"].nunique()
)

col2.metric(
    "Total Capacity",
    f"{filtered_data['total_capacity'].sum():,.0f} ttpa"
)

col3.metric(
    "Average LitPop Exposure",
    f"{filtered_data['LitPop_value'].mean():.2e}"
)


st.subheader("Steel Plant Map")

map_data = filtered_data.dropna(
    subset=[
        "Latitude",
        "Longitude",
        "total_capacity",
        "LitPop_value"
    ]
)

fig = px.scatter_map(
    map_data,
    lat="Latitude",
    lon="Longitude",
    size="total_capacity",
    color="LitPop_value",
    hover_name="Plant name (English)",
    hover_data={
        "Owner": True,
        "Country/area": True,
        "total_capacity": ":,.0f",
        "LitPop_value": ":.2e",
        "Latitude": False,
        "Longitude": False
    },
    map_style="carto-positron",
    zoom=2,
    title="Plant Capacity and Local LitPop Exposure"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader("Plant Data")

st.dataframe(
    filtered_data[
        [
            "Plant name (English)",
            "Owner",
            "Country/area",
            "total_capacity",
            "LitPop_value"
        ]
    ],
    use_container_width=True
)


st.divider()

st.caption(
    "Data sources: Global Energy Monitor and LitPop (ETH Zurich). "
    "LitPop exposure is matched to steel plants using geographic proximity."
)
