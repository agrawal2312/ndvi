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
import os
import streamlit as st
import rasterio
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from PIL import Image
import matplotlib.pyplot as plt
import tempfile
import requests
from rasterio.warp import transform_bounds, transform
from rasterio.crs import CRS

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="NDVI Viewer", layout="wide")
st.title("🗺️ NDVI Web Map Viewer (Pixel Accurate & Georeferenced)")

# --------------------------------------------------
# FIX PROJ PATH (Windows)
# --------------------------------------------------
os.environ["PROJ_LIB"] = r"C:\Users\Administrator\Desktop\CROP_VIEWER\env\Lib\site-packages\rasterio\proj_data"

# --------------------------------------------------
# GOOGLE DRIVE CONFIG
# --------------------------------------------------
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

DRIVE_FILE_ID = "1AopB-H5JXvRiUQeDEVRPanxJhTT9nXKO"
STACK_FILE = f"{CACHE_DIR}/NDVI_stack.tif"

TIME_LABELS = ["14 Nov", "16 Dec", "25 Jan", "23 Feb"]

# --------------------------------------------------
# DOWNLOAD STACK FROM DRIVE
# --------------------------------------------------
@st.cache_resource
def download_from_drive(file_id, output_path):
    if os.path.exists(output_path):
        return output_path

    url = f"https://drive.google.com/uc?id={file_id}"
    with st.spinner("⬇️ Downloading NDVI stack from Google Drive..."):
        r = requests.get(url)
        r.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(r.content)

    return output_path

STACK_FILE = download_from_drive(DRIVE_FILE_ID, STACK_FILE)

# --------------------------------------------------
# LOAD NDVI STACK
# --------------------------------------------------
@st.cache_resource
def load_ndvi(path):
    with rasterio.open(path) as src:
        data = src.read().astype(np.float32)
        rows, cols = src.height, src.width
        bounds = src.bounds
        transform_affine = src.transform
        crs = src.crs

    return data, rows, cols, crs, bounds, transform_affine

ndvi_stack, rows, cols, crs, bounds, transform_affine = load_ndvi(STACK_FILE)

# --------------------------------------------------
# CREATE NDVI PNG
# --------------------------------------------------
@st.cache_resource
def create_png(ndvi):
    ndvi_norm = (ndvi + 1) / 2
    rgb = plt.cm.RdYlGn(ndvi_norm)
    img = (rgb[:, :, :3] * 255).astype(np.uint8)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    Image.fromarray(img).save(tmp.name)
    return tmp.name

png_path = create_png(ndvi_stack[0])

# --------------------------------------------------
# TRANSFORM BOUNDS TO LAT/LON
# --------------------------------------------------
from rasterio.warp import transform_bounds
from rasterio.crs import CRS

with rasterio.open(STACK_FILE) as src:
    bounds = src.bounds
    src_crs = src.crs

if src_crs is None:
    st.error("❌ Raster has no CRS defined")
    st.stop()

dst_crs = CRS.from_epsg(4326)

geo_bounds = transform_bounds(
    src_crs,
    dst_crs,
    bounds.left,
    bounds.bottom,
    bounds.right,
    bounds.top,
    densify_pts=21
)


image_bounds = [
    [geo_bounds[1], geo_bounds[0]],
    [geo_bounds[3], geo_bounds[2]]
]

# --------------------------------------------------
# CREATE MAP
# --------------------------------------------------
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

# --------------------------------------------------
# DISPLAY MAP
# --------------------------------------------------
map_data = st_folium(m, height=650, width="100%")

# --------------------------------------------------
# CLICK → NDVI TIME SERIES
# --------------------------------------------------
st.subheader("📈 NDVI Time Series")

if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    x, y = transform("EPSG:4326", crs, [lon], [lat])
    x, y = x[0], y[0]

    row, col = ~transform_affine * (x, y)
    row, col = int(row), int(col)

    if 0 <= row < rows and 0 <= col < cols:
        ndvi_values = ndvi_stack[:, row, col]

        st.success(
            f"Row: {row}, Col: {col} | "
            f"Lat: {lat:.5f}, Lon: {lon:.5f} | "
            f"NDVI: {ndvi_values[0]:.3f}"
        )

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=TIME_LABELS,
            y=ndvi_values,
            mode="lines+markers",
            marker=dict(size=10),
            line=dict(width=3)
        ))

        fig.update_layout(
            title=f"NDVI Time Series (row={row}, col={col})",
            xaxis_title="Date",
            yaxis_title="NDVI",
            yaxis=dict(range=[-1, 1]),
            height=400,
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.warning("Clicked outside image extent")
else:
    st.info("Click anywhere on the NDVI image")



