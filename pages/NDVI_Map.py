# import os
# import streamlit as st
# import rasterio
# import numpy as np
# import folium
# from streamlit_folium import st_folium
# import plotly.graph_objects as go
# from PIL import Image
# import matplotlib.pyplot as plt
# import tempfile
# from rasterio.warp import transform_bounds, transform
# from rasterio.crs import CRS
# import streamlit as st
# from home import resource_path
# st.title("🗺️ NDVI Map Viewer")


# # --------------------------------------------------
# # FIX PROJ PATH (important on Windows with PostGIS installed)
# # --------------------------------------------------
# os.environ["PROJ_LIB"] = r"C:\Users\Administrator\Desktop\CROP_VIEWER\env\Lib\site-packages\rasterio\proj_data"



# # --------------------------------------------------
# # PAGE CONFIG
# # --------------------------------------------------
# st.set_page_config(page_title="NDVI Viewer", layout="wide")
# st.title("🗺️ NDVI Web Map Viewer (Pixel Accurate & Georeferenced)")

# # --------------------------------------------------
# # CONFIG
# # --------------------------------------------------
# STACK_FILE = "NDVI_stack.tif"
# # STACK_FILE = resource_path("ndvi_outputs/NDVI_stack.tif")
# TIME_LABELS = ["14 Nov", "16 Dec", "25 Jan", "23 Feb"]

# # --------------------------------------------------
# # LOAD NDVI STACK WITH CRS
# # --------------------------------------------------
# @st.cache_resource
# def load_ndvi(path):
#     with rasterio.open(path) as src:
#         data = src.read().astype(np.float32)
#         rows, cols = src.height, src.width
#         bounds = src.bounds
#         transform_affine = src.transform
#     # Force CRS to EPSG:32643
#     crs = CRS.from_epsg(32643)
#     return data, rows, cols, crs, bounds, transform_affine

# ndvi_stack, rows, cols, crs, bounds, transform_affine = load_ndvi(STACK_FILE)

# # --------------------------------------------------
# # CREATE NDVI PNG
# # --------------------------------------------------
# @st.cache_resource
# def create_png(ndvi):
#     ndvi_norm = (ndvi + 1) / 2
#     rgb = plt.cm.RdYlGn(ndvi_norm)
#     img = (rgb[:, :, :3] * 255).astype(np.uint8)

#     tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
#     Image.fromarray(img).save(tmp.name)
#     return tmp.name

# png_path = create_png(ndvi_stack[0])

# # --------------------------------------------------
# # TRANSFORM BOUNDS TO LAT/LON
# # --------------------------------------------------

# geo_bounds = transform_bounds(crs, "EPSG:4326", *bounds)

# # Folium expects [[min_lat, min_lon], [max_lat, max_lon]]
# image_bounds = [[geo_bounds[1], geo_bounds[0]],   # (min_lat, min_lon)
#                 [geo_bounds[3], geo_bounds[2]]]   # (max_lat, max_lon)

# # --------------------------------------------------
# # CREATE MAP WITH BASEMAP
# # --------------------------------------------------
# m = folium.Map(
#     location=[(geo_bounds[1] + geo_bounds[3]) / 2,
#               (geo_bounds[0] + geo_bounds[2]) / 2],
#     zoom_start=12,
#     tiles="OpenStreetMap",
#     crs="EPSG3857"
# )

# folium.raster_layers.ImageOverlay(
#     image=png_path,
#     bounds=image_bounds,
#     opacity=1.0,
#     interactive=True,
#     zindex=1,
# ).add_to(m)

# m.fit_bounds(image_bounds)

# # --------------------------------------------------
# # DISPLAY MAP
# # --------------------------------------------------
# map_data = st_folium(
#     m,
#     height=650,
#     width="100%",
# )


# # --------------------------------------------------
# # HANDLE CLICK → TIME SERIES
# # --------------------------------------------------
# st.subheader("📈 NDVI Time Series")

# if map_data and map_data.get("last_clicked"):
#     lat = map_data["last_clicked"]["lat"]
#     lon = map_data["last_clicked"]["lng"]

#     # Convert lat/lon → UTM (EPSG:32643)
#     x, y = transform("EPSG:4326", crs, [lon], [lat])
#     x, y = x[0], y[0]

#     # Convert UTM → row/col
#     row, col = ~transform_affine * (x, y)
#     row, col = int(row), int(col)

#     if 0 <= row < rows and 0 <= col < cols:
#         st.success(f"Clicked → Row: {row}, Col: {col}, Lat: {lat:.5f}, Lon: {lon:.5f}")

#         ndvi_values = ndvi_stack[:, row, col]
#         ndvi_val = float(ndvi_stack[0, row, col])

#         # Add marker with popup + tooltip showing NDVI value
#         folium.Marker(
#             location=[lat, lon],
#             popup=f"Row={row}, Col={col}<br>NDVI={ndvi_val:.3f}",
#             tooltip=f"NDVI={ndvi_val:.3f}"
#         ).add_to(m)

#         # Re-render map with marker
#         map_data = st_folium(
#             m,
#             height=650,
#             width="100%",
#         )

#         # Plot NDVI time series
#         fig = go.Figure()
#         fig.add_trace(
#             go.Scatter(
#                 x=TIME_LABELS,
#                 y=ndvi_values,
#                 mode="lines+markers",
#                 marker=dict(size=10),
#                 line=dict(width=3),
#                 hoverlabel=dict(
#                     font=dict(size=20),
#                     bgcolor="black",
#                     bordercolor="black"
#                 ),
#             )
#         )

#         fig.update_layout(
#             title=f"NDVI Time Series (row={row}, col={col})",
#             xaxis_title="Date",
#             yaxis_title="NDVI",
#             yaxis=dict(range=[-1, 1]),
#             height=400,
#         )

#         st.plotly_chart(fig, config={"displayModeBar": False}, use_container_width=True)

#     else:
#         st.warning("Clicked outside image extent")

# else:
#     st.info("Click anywhere on the NDVI image")
# ==================================================
# PROJ / CRS FIX  (MUST BE AT VERY TOP)
# ==================================================
# ==================================================
# PROJ / PYPROJ FIX (MUST BE FIRST)
# ==================================================


#PART2
import os
import pyproj

os.environ["PROJ_LIB"] = pyproj.datadir.get_data_dir()
os.environ["PROJ_NETWORK"] = "ON"
pyproj.network.set_network_enabled(True)

# ==================================================
# IMPORTS
# ==================================================
import streamlit as st
import rasterio
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from rasterio.crs import CRS
from rasterio.warp import transform, transform_bounds
import matplotlib.pyplot as plt
from PIL import Image
import tempfile
import requests

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="NDVI Web Map Viewer",
    layout="wide"
)
st.title("🗺️ NDVI Web Map Viewer (Pixel Accurate & Georeferenced)")

# ==================================================
# CRS DEFINITIONS (SAFE WKT)
# ==================================================
SRC_CRS = CRS.from_wkt(pyproj.CRS.from_epsg(32643).to_wkt())  # UTM zone
DST_CRS = CRS.from_wkt(pyproj.CRS.from_epsg(4326).to_wkt())  # WGS84

# ==================================================
# GOOGLE DRIVE CONFIG
# ==================================================
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

DRIVE_FILE_ID = "1AopB-H5JXvRiUQeDEVRPanxJhTT9nXKO"
STACK_FILE = f"{CACHE_DIR}/NDVI_stack.tif"

TIME_LABELS = ["14 Nov", "16 Dec", "25 Jan", "23 Feb"]

# ==================================================
# DOWNLOAD NDVI STACK
# ==================================================
@st.cache_resource
def download_from_drive(file_id, output_path):
    if os.path.exists(output_path):
        return output_path

    url = f"https://drive.google.com/uc?id={file_id}"
    with st.spinner("⬇️ Downloading NDVI stack..."):
        r = requests.get(url)
        r.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(r.content)

    return output_path

STACK_FILE = download_from_drive(DRIVE_FILE_ID, STACK_FILE)

# ==================================================
# LOAD NDVI STACK
# ==================================================
@st.cache_resource
def load_ndvi_stack(path):
    with rasterio.open(path) as src:
        ndvi = src.read().astype(np.float32)   # (time, rows, cols)
        bounds = src.bounds
        transform_affine = src.transform
        rows, cols = src.height, src.width

    return ndvi, rows, cols, bounds, transform_affine

ndvi_stack, rows, cols, bounds, transform_affine = load_ndvi_stack(STACK_FILE)

# ==================================================
# CREATE NDVI PNG (DISPLAY ONLY)
# ==================================================
@st.cache_resource
def create_ndvi_png(ndvi):
    ndvi_norm = (ndvi + 1) / 2
    rgb = plt.cm.RdYlGn(ndvi_norm)
    img = (rgb[:, :, :3] * 255).astype(np.uint8)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    Image.fromarray(img).save(tmp.name)
    return tmp.name

png_path = create_ndvi_png(ndvi_stack[0])

# ==================================================
# TRANSFORM BOUNDS → LAT/LON
# ==================================================
geo_bounds = transform_bounds(
    SRC_CRS,
    DST_CRS,
    bounds.left,
    bounds.bottom,
    bounds.right,
    bounds.top,
    densify_pts=21
)

image_bounds = [
    [geo_bounds[1], geo_bounds[0]],  # south-west
    [geo_bounds[3], geo_bounds[2]]   # north-east
]

# ==================================================
# CREATE FOLIUM MAP
# ==================================================
m = folium.Map(
    location=[
        (geo_bounds[1] + geo_bounds[3]) / 2,
        (geo_bounds[0] + geo_bounds[2]) / 2
    ],
    zoom_start=12,
    tiles="OpenStreetMap"
)

folium.raster_layers.ImageOverlay(
    image=png_path,
    bounds=image_bounds,
    opacity=1.0,
    interactive=True,
).add_to(m)

m.fit_bounds(image_bounds)

# ==================================================
# DISPLAY MAP
# ==================================================
map_data = st_folium(m, height=650, width="100%")

# ==================================================
# CLICK → PIXEL-ACCURATE NDVI TIME SERIES
# ==================================================
st.subheader("📈 NDVI Time Series")

if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    # --- Lat/Lon → Raster CRS ---
    x, y = transform(
        DST_CRS, SRC_CRS,
        [lon], [lat]
    )
    x, y = x[0], y[0]

    # --- Raster CRS → Fractional Pixel ---
    col_f, row_f = ~transform_affine * (x, y)

    # --- Snap to nearest pixel (CRITICAL FIX) ---
    row = int(round(row_f))
    col = int(round(col_f))

    # --- Clamp to raster extent ---
    row = max(0, min(rows - 1, row))
    col = max(0, min(cols - 1, col))

    # --- Extract NDVI time series ---
    ndvi_values = ndvi_stack[:, row, col]
    ndvi_values = np.clip(ndvi_values, -1, 1)

    st.success(
        f"Pixel → Row: {row}, Col: {col} | "
        f"Lat: {lat:.5f}, Lon: {lon:.5f} | "
        f"NDVI (first date): {ndvi_values[0]:.3f}"
    )

    # --- Plot NDVI Time Series ---
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=TIME_LABELS,
            y=ndvi_values,
            mode="lines+markers",
            marker=dict(size=8),
            line=dict(width=3),
        )
    )

    fig.update_layout(
        title="NDVI Time Series (Pixel Accurate)",
        xaxis_title="Date",
        yaxis_title="NDVI",
        yaxis=dict(range=[-1, 1]),
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Click anywhere on the NDVI image to view NDVI values")
