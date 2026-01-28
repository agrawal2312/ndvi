# import streamlit as st
# st.title("📈 NDVI Time Series Viewer")
# import streamlit as st
# import rasterio
# import numpy as np
# import plotly.graph_objects as go
# from streamlit_plotly_events import plotly_events
# from home import resource_path


# # --------------------------------------------------
# # PAGE CONFIG
# # --------------------------------------------------
# st.set_page_config(page_title="NDVI Time Series Viewer", layout="wide")
# st.title("🌱 NDVI Time Series Viewer (Click on map)")

# # --------------------------------------------------
# # CONFIG
# # --------------------------------------------------
# from home import resource_path
# STACK_FILE = resource_path("NDVI_stack.tif")

# # STACK_FILE = resource_path("ndvi_outputs/NDVI_stack.tif")
# TIME_LABELS = ["14 Nov", "16 Dec", "25 Jan", "23 Feb"]
# DOWNSAMPLE = 6   # 🔥 increase if raster is very large

# # --------------------------------------------------
# # LOAD NDVI STACK
# # --------------------------------------------------
# @st.cache_data(show_spinner=True)
# def load_ndvi_stack(path):
#     with rasterio.open(path) as src:
#         data = src.read().astype(np.float32)   # (time, rows, cols)
#     return data

# ndvi_stack = load_ndvi_stack(STACK_FILE)
# t, rows, cols = ndvi_stack.shape

# # --------------------------------------------------
# # DOWNSAMPLE FOR DISPLAY
# # --------------------------------------------------
# ndvi_display = ndvi_stack[0][::DOWNSAMPLE, ::DOWNSAMPLE]
# disp_rows, disp_cols = ndvi_display.shape

# # --------------------------------------------------
# # NDVI MAP
# # --------------------------------------------------
# customdata = []

# for i in range(ndvi_display.shape[0]):
#     row_list = []
#     for j in range(ndvi_display.shape[1]):
#         r = min(i * DOWNSAMPLE, rows - 1)
#         c = min(j * DOWNSAMPLE, cols - 1)
#         row_list.append([r, c, float(ndvi_stack[0, r, c])])
#     customdata.append(row_list)

# fig_map = go.Figure(
#     go.Heatmap(
#         z=ndvi_display.tolist(),          # ONLY for colors
#         customdata=customdata,            # 🔥 truth source
#         colorscale="RdYlGn",
#         zmin=-1,
#         zmax=1,
#         hovertemplate=(
#             "Row: %{customdata[0]}<br>"
#             "Col: %{customdata[1]}<br>"
#             "NDVI: %{customdata[2]:.3f}"
#             "<extra></extra>"
#         ),
#         colorbar=dict(title="NDVI"),
#     )
# )



# fig_map.update_layout(
#     title=f"NDVI Map — {TIME_LABELS[0]} (click a pixel)",
#     yaxis=dict(autorange="reversed"),
#     height=700,
#     margin=dict(l=40, r=40, t=60, b=40),
# )

# # --------------------------------------------------
# # SHOW MAP + CAPTURE CLICK
# # --------------------------------------------------
# selected_points = plotly_events(
#     fig_map,
#     click_event=True,
#     hover_event=False,
#     select_event=False,
#     override_height=700,
#     override_width=700,
# )

# # --------------------------------------------------
# # HANDLE CLICK
# # --------------------------------------------------
# st.subheader("📈 NDVI Time Series")

# if selected_points:
#     # convert display index → original pixel index
#     disp_row = int(selected_points[0]["y"])
#     disp_col = int(selected_points[0]["x"])

#     row = disp_row * DOWNSAMPLE
#     col = disp_col * DOWNSAMPLE

#     # safety clamp
#     row = min(row, rows - 1)
#     col = min(col, cols - 1)

#     # 🔥 PRINT TO CONSOLE
#     print(f"Clicked pixel → Row: {row}, Col: {col}")

#     st.success(f"Clicked pixel → Row: {row}, Col: {col}")

#     # extract NDVI time series
#     ndvi_values = ndvi_stack[:, row, col]

#     fig_ts = go.Figure()
#     fig_ts.add_trace(
#         go.Scatter(
#             x=TIME_LABELS,
#             y=ndvi_values,
#             mode="lines+markers",
#             marker=dict(size=10),          # 🔵 marker size
#             line=dict(width=3),
#             hoverlabel=dict(
#             font=dict(size=30),   # 🔥 hover text size
#             bgcolor="black",      # optional
#             bordercolor="black"   # optional
#         ),
#         )
#     )

#     fig_ts.update_layout(
#         title=f"NDVI Time Series (row={row}, col={col})",
#         xaxis_title="Date",
#         yaxis_title="NDVI",
#         yaxis=dict(range=[-1, 1]),
#         height=400,
#     )

#     st.plotly_chart(fig_ts, config={
#         "displayModeBar": False   # 🔥 hides the toolbar
#     },use_container_width=True)
# else:
#     st.info("Click on any pixel in the NDVI map to see its NDVI time series.")
import os
import streamlit as st
import rasterio
import numpy as np
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
from streamlit_plotly_events import plotly_events
import requests

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="NDVI Time Series Viewer", layout="wide")
st.title("🌱 NDVI Time Series Viewer (Click on map)")

# --------------------------------------------------
# GOOGLE DRIVE CONFIG
# --------------------------------------------------
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

DRIVE_FILE_ID = "1AopB-H5JXvRiUQeDEVRPanxJhTT9nXKO"
STACK_FILE = f"{CACHE_DIR}/NDVI_stack.tif"

TIME_LABELS = ["14 Nov", "16 Dec", "25 Jan", "23 Feb"]
DOWNSAMPLE = 6   # increase if raster is large

# --------------------------------------------------
# DOWNLOAD NDVI STACK FROM DRIVE
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
@st.cache_data(show_spinner=True)
def load_ndvi_stack(path):
    with rasterio.open(path) as src:
        data = src.read().astype(np.float32)   # (time, rows, cols)
    return data

ndvi_stack = load_ndvi_stack(STACK_FILE)
t, rows, cols = ndvi_stack.shape

# --------------------------------------------------
# DOWNSAMPLE FOR DISPLAY
# --------------------------------------------------
ndvi_display = ndvi_stack[0][::DOWNSAMPLE, ::DOWNSAMPLE]
disp_rows, disp_cols = ndvi_display.shape

# --------------------------------------------------
# NDVI MAP (PLOTLY)
# --------------------------------------------------
customdata = []

for i in range(disp_rows):
    row_list = []
    for j in range(disp_cols):
        r = min(i * DOWNSAMPLE, rows - 1)
        c = min(j * DOWNSAMPLE, cols - 1)
        row_list.append([r, c, float(ndvi_stack[0, r, c])])
    customdata.append(row_list)

fig_map = go.Figure(
    go.Heatmap(
        z=ndvi_display.tolist(),      # only for color
        customdata=customdata,        # truth pixels
        colorscale="RdYlGn",
        zmin=-1,
        zmax=1,
        hovertemplate=(
            "Row: %{customdata[0]}<br>"
            "Col: %{customdata[1]}<br>"
            "NDVI: %{customdata[2]:.3f}"
            "<extra></extra>"
        ),
        colorbar=dict(title="NDVI"),
    )
)

fig_map.update_layout(
    title=f"NDVI Map — {TIME_LABELS[0]} (click a pixel)",
    yaxis=dict(autorange="reversed"),
    height=700,
    margin=dict(l=40, r=40, t=60, b=40),
)

# --------------------------------------------------
# SHOW MAP + CAPTURE CLICK
# --------------------------------------------------
selected_points = plotly_events(
    fig_map,
    click_event=True,
    hover_event=False,
    select_event=False,
    override_height=700,
    override_width=700,
)

# --------------------------------------------------
# HANDLE CLICK → TIME SERIES
# --------------------------------------------------
st.subheader("📈 NDVI Time Series")

if selected_points:
    disp_row = int(selected_points[0]["y"])
    disp_col = int(selected_points[0]["x"])

    row = min(disp_row * DOWNSAMPLE, rows - 1)
    col = min(disp_col * DOWNSAMPLE, cols - 1)

    st.success(f"Clicked pixel → Row: {row}, Col: {col}")

    ndvi_values = ndvi_stack[:, row, col]

    fig_ts = go.Figure()
    fig_ts.add_trace(
        go.Scatter(
            x=TIME_LABELS,
            y=ndvi_values,
            mode="lines+markers",
            marker=dict(size=10),
            line=dict(width=3),
            hoverlabel=dict(
                font=dict(size=30),
                bgcolor="black",
                bordercolor="black"
            ),
        )
    )

    fig_ts.update_layout(
        title=f"NDVI Time Series (row={row}, col={col})",
        xaxis_title="Date",
        yaxis_title="NDVI",
        yaxis=dict(range=[-1, 1]),
        height=400,
    )

    st.plotly_chart(
        fig_ts,
        use_container_width=True,
        config={"displayModeBar": False}
    )
else:
    st.info("Click on any pixel in the NDVI map to see its NDVI time series.")
