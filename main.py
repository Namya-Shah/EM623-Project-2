import streamlit as st
import xarray as xr
import plotly.express as px
import glob
from datetime import datetime

st.set_page_config(layout="wide")

st.title("🌧️ Himalayan Extreme Rainfall Explorer")

# ------------------------------
# Load Data + Extract Dates
# ------------------------------
@st.cache_resource
def load_data():
    files = sorted(glob.glob("datasets/3B-DAY-*.nc4"))

    # Extract dates from filenames
    date_list = []
    for f in files:
        # filename example: 3B-DAY-L.MS.MRG.3IMERG.20251102-S000000...
        date_str = f.split(".")[4][:8]  # "20251102"
        dt = datetime.strptime(date_str, "%Y%m%d")
        date_list.append(dt)

    # Load dataset lazily
    ds = xr.open_mfdataset(files, combine="nested", concat_dim="time")

    # Assign extracted dates
    ds = ds.assign_coords(time=date_list)

    himalayas = ds.sel(lat=slice(26, 36), lon=slice(75, 95))
    precip = himalayas["precipitation"]

    return precip, date_list

precip, date_list = load_data()

# ------------------------------
# Slider Using Index but Show Date
# ------------------------------
time_index = st.slider("Select Time Index", 0, len(date_list) - 1, 0)
selected_date = date_list[time_index].strftime("%d-%m-%Y")

col1, col2 = st.columns([1.2, 0.8])

with col1:
    st.subheader(f"📊 Rainfall Map — Date: {selected_date}")

    precip_np = precip.isel(time=time_index).compute()

    fig = px.imshow(
        precip_np,
        labels={"color": "Rainfall (mm/hr)"},
        color_continuous_scale="Viridis",
        origin="lower",
        title="Himalayan Rainfall",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📝 Story / Interpretation")
    st.write(f"""
    **Date analyzed:** {selected_date}

    At this time step, we observe precipitation patterns across the Himalayan 
    arc. The distribution highlights the strong spatial gradients from the 
    south-facing slopes to the interior Tibetan plateau.

    - **Bright regions** indicate higher rainfall  
    - **Darker regions** indicate dry conditions  
    - Data comes from the *merged satellite precipitation product*  
    - Perfect for analyzing extreme events or monsoon dynamics  
    """)

# ------------------------------
# Two Images + Descriptions
# ------------------------------
st.markdown("---")
st.header("🗺️ Mind Maps")

img1_col, img2_col = st.columns(2)

with img1_col:
    st.image("plots/plot1.png", caption="Figure 1: Digital Payments Ecosystem (India)")
    st.markdown("**Type of mind map:** Radial")
    st.write("""
    I went with a mind map here because India's digital payments space is incredibly interconnected—you've got consumers, merchants, banks, fintechs, and regulators all playing different roles but constantly interacting with each other. The radial layout just makes it easier to see how a simple UPI payment actually touches so many different players, from the moment someone initiates a transaction to when it finally settles and gets reported to regulators.
    """)
with img2_col:
    st.image("plots/plot2.png", caption="Figure 2: Carbon Credit Market")
    st.markdown("**Type of mind map:** Radial")
    st.write("""
    For the carbon credit market, a mind map felt like the right choice because it's honestly a pretty complex system with lots of moving parts. You've got project developers planting trees or capturing methane, verifiers checking if it's all legit, trading platforms connecting buyers and sellers, and corporates trying to hit their net-zero goals—and a mind map lets you see how all these pieces fit together without getting overwhelmed by the details.
    """)