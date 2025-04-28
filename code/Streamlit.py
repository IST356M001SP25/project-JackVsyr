import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("Aircraft Listings by State")

@st.cache_data
def load_data():
    path = '/Users/jack/Downloads/IST 356/Cleaned_ASOlistings_20250423.csv'
    data = pd.read_csv(path)
    return data

data = load_data()

def extract_state(location):
    if pd.isna(location):
        return None
    parts = location.split(',')
    if len(parts) == 2:
        return parts[0].strip()
    return None

data['State'] = data['Location'].apply(extract_state)

state_co = {
    'AL': [32.806671, -86.791130], 'AK': [61.370716, -152.404419], 'AZ': [33.729759, -111.431221],
    'AR': [34.969704, -92.373123], 'CA': [36.116203, -119.681564], 'CO': [39.059811, -105.311104],
    'CT': [41.597782, -72.755371], 'DE': [39.318523, -75.507141], 'FL': [27.766279, -81.686783],
    'GA': [33.040619, -83.643074], 'HI': [21.094318, -157.498337], 'ID': [44.240459, -114.478828],
    'IL': [40.349457, -88.986137], 'IN': [39.849426, -86.258278], 'IA': [42.011539, -93.210526],
    'KS': [38.526600, -96.726486], 'KY': [37.668140, -84.670067], 'LA': [31.169546, -91.867805],
    'ME': [44.693947, -69.381927], 'MD': [39.063946, -76.802101], 'MA': [42.230171, -71.530106],
    'MI': [43.326618, -84.536095], 'MN': [45.694454, -93.900192], 'MS': [32.741646, -89.678696],
    'MO': [38.456085, -92.288368], 'MT': [46.921925, -110.454353], 'NE': [41.125370, -98.268082],
    'NV': [38.313515, -117.055374], 'NH': [43.452492, -71.563896], 'NJ': [40.298904, -74.521011],
    'NM': [34.840515, -106.248482], 'NY': [42.165726, -74.948051], 'NC': [35.630066, -79.806419],
    'ND': [47.528912, -99.784012], 'OH': [40.388783, -82.764915], 'OK': [35.565342, -96.928917],
    'OR': [44.572021, -122.070938], 'PA': [40.590752, -77.209755], 'RI': [41.680893, -71.511780],
    'SC': [33.856892, -80.945007], 'SD': [44.299782, -99.438828], 'TN': [35.747845, -86.692345],
    'TX': [31.054487, -97.563461], 'UT': [40.150032, -111.862434], 'VT': [44.045876, -72.710686],
    'VA': [37.769337, -78.169968], 'WA': [47.400902, -121.490494], 'WV': [38.491226, -80.954453],
    'WI': [44.268543, -89.616508], 'WY': [42.755966, -107.302490]
}

data['Coordinates'] = data['State'].map(state_co)
data = data.dropna(subset=['Coordinates'])
data[['Latitude', 'Longitude']] = pd.DataFrame(data['Coordinates'].tolist(), index=data.index)

state_counts = data['State'].value_counts().reset_index()
state_counts.columns = ['State', 'AircraftCount']
state_counts['Coordinates'] = state_counts['State'].map(state_co)
state_counts[['Latitude', 'Longitude']] = pd.DataFrame(state_counts['Coordinates'].tolist(), index=state_counts.index)

layer_points = pdk.Layer(
    'ScatterplotLayer',
    data=state_counts,
    get_position='[Longitude, Latitude]',
    get_fill_color='[0, 100, 255, 160]',
    get_radius=40000,
    pickable=True
)

layer_text = pdk.Layer(
    "TextLayer",
    data=state_counts,
    get_position='[Longitude, Latitude]',
    get_text='AircraftCount',
    get_size=16,
    get_color=[0, 0, 0],
    get_text_anchor='"middle"',
    get_alignment_baseline='"center"'
)

deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=37.0902,
        longitude=-95.7129,
        zoom=3.5,
        pitch=0,
    ),
    layers=[layer_points, layer_text],
    tooltip={"text": "State: {State}\nAircraft Count: {AircraftCount}"}
)

# --- Show Map ---
st.pydeck_chart(deck, use_container_width=True)

# --- Simulated Click by Dropdown ---
st.write("Select a state to see the aircraft for sale:")

selected_state = st.selectbox("Choose a state:", sorted(state_counts['State'].tolist()))

if selected_state:
    filtered_data = data[data['State'] == selected_state]
    st.subheader(f"Aircraft in {selected_state}")
    st.write(f"{len(filtered_data)} aircraft found.")
    st.dataframe(filtered_data[['Year', 'Make', 'Model', 'Reg #', 'Price', 'Location', 'Company']])