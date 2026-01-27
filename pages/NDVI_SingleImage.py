# import streamlit as st
# st.title("🖼️ NDVI Single Image Viewer")
# # import streamlit as st
# # import rasterio
# # import numpy as np
# # import plotly.graph_objects as go

# # # -----------------------------
# # # Step 1: Configuration
# # # -----------------------------
# # RED_BAND = 3   # adjust if needed
# # NIR_BAND = 4   # adjust if needed

# # IMAGE_FILES = {
# #     "14 Nov": r"C:\Users\Administrator\Desktop\classification\input_rabi\14_nov.tif",
# #     "16 Dec": r"C:\Users\Administrator\Desktop\classification\input_rabi\16_dec.tif",
# #     "25 Jan": r"C:\Users\Administrator\Desktop\classification\input_rabi\25_jan.tif",
# #     "23 Feb": r"C:\Users\Administrator\Desktop\classification\input_rabi\23_feb.tif",
# # }

# # TIME_LABELS = list(IMAGE_FILES.keys())


# # # -----------------------------
# # # Step 2: Utility functions
# # # -----------------------------
# # def calculate_ndvi_and_rgb(image_path, red_band=RED_BAND, nir_band=NIR_BAND):
# #     with rasterio.open(image_path) as src:
# #         red = src.read(red_band).astype(float)
# #         nir = src.read(nir_band).astype(float)
# #         ndvi = (nir - red) / (nir + red + 1e-10)

# #         # Read RGB (bands 1,2,3 assumed)
# #         rgb = src.read([1, 2, 3]).astype(float)
# #         rgb = np.transpose(rgb, (1, 2, 0))  # (rows, cols, bands)

# #         # Scale RGB to 0-255
# #         rgb = (255 * (rgb / np.max(rgb))).astype(np.uint8)

# #     return ndvi, rgb


# # # -----------------------------
# # # Step 3: Streamlit UI
# # # -----------------------------
# # st.set_page_config(page_title="NDVI Viewer", layout="wide")
# # st.title("🌱 NDVI Viewer with Interactive NDVI Values")

# # # Dropdown to select date
# # selected_date = st.selectbox("Select date:", TIME_LABELS)

# # # Compute NDVI + RGB for selected image
# # ndvi_arr, rgb_img = calculate_ndvi_and_rgb(IMAGE_FILES[selected_date])

# # # -----------------------------
# # # Step 4: Show side-by-side
# # # -----------------------------
# # col1, col2 = st.columns(2)

# # with col1:
# #     st.subheader(f"Original RGB — {selected_date}")
# #     st.image(rgb_img, use_column_width=True)

# # with col2:
# #     st.subheader(f"NDVI Heatmap — {selected_date}")
# #     # Plotly heatmap with hover NDVI values
# #     fig = go.Figure(
# #         data=go.Heatmap(
# #             z=ndvi_arr,
# #             colorscale="RdYlGn",
# #             zmin=-1, zmax=1,
# #             hovertemplate="Row: %{y}<br>Col: %{x}<br>NDVI: %{z:.3f}<extra></extra>",
# #             colorbar=dict(title="NDVI"),
# #         )
# #     )
# #     fig.update_layout(
# #         xaxis=dict(title="Column index"),
# #         yaxis=dict(title="Row index", autorange="reversed"),
# #         height=600,
# #         margin=dict(l=40, r=20, t=50, b=40),
# #     )
# #     st.plotly_chart(fig, use_container_width=True)
    
# #     #for run
# # # streamlit run ndvi_viewer.py

# # import streamlit as st
# # import rasterio
# # import numpy as np
# # import plotly.graph_objects as go

# # # -----------------------------
# # # Step 1: Configuration
# # # -----------------------------
# # RED_BAND = 3   # adjust if needed
# # NIR_BAND = 4   # adjust if needed

# # IMAGE_FILES = {
# #     "14 Nov": r"C:\Users\Administrator\Desktop\classification\input_rabi\14_nov.tif",
# #     "16 Dec": r"C:\Users\Administrator\Desktop\classification\input_rabi\16_dec.tif",
# #     "25 Jan": r"C:\Users\Administrator\Desktop\classification\input_rabi\25_jan.tif",
# #     "23 Feb": r"C:\Users\Administrator\Desktop\classification\input_rabi\23_feb.tif",
# # }

# # TIME_LABELS = list(IMAGE_FILES.keys())

# # # -----------------------------
# # # Step 2: Utility function
# # # -----------------------------
# # def calculate_ndvi_and_rgb(image_path, red_band=RED_BAND, nir_band=NIR_BAND):
# #     with rasterio.open(image_path) as src:
# #         red = src.read(red_band).astype(float)
# #         nir = src.read(nir_band).astype(float)

# #         ndvi = (nir - red) / (nir + red + 1e-10)

# #         # Read RGB (bands 1,2,3)
# #         rgb = src.read([1, 2, 3]).astype(float)
# #         rgb = np.transpose(rgb, (1, 2, 0))

# #         # Normalize RGB to 0–255
# #         rgb = (rgb - rgb.min()) / (rgb.max() - rgb.min())
# #         rgb = (rgb * 255).astype(np.uint8)

# #     return ndvi, rgb

# # # -----------------------------
# # # Step 3: Streamlit UI
# # # -----------------------------
# # st.set_page_config(page_title="NDVI Viewer", layout="wide")
# # st.title("🌱 NDVI Viewer with Interactive NDVI Values")

# # selected_date = st.selectbox("Select date:", TIME_LABELS)

# # ndvi_arr, rgb_img = calculate_ndvi_and_rgb(IMAGE_FILES[selected_date])

# # # -----------------------------
# # # Step 4: Side-by-side display
# # # -----------------------------
# # col1, col2 = st.columns(2)

# # with col1:
# #     st.subheader(f"Original RGB — {selected_date}")
# #     st.image(rgb_img, use_column_width=True)

# # with col2:
# #     st.subheader(f"NDVI Heatmap — {selected_date}")

# #     rows, cols = ndvi_arr.shape
# #     aspect_ratio = rows / cols

# #     fig = go.Figure(
# #         data=go.Heatmap(
# #             z=ndvi_arr,
# #             colorscale="RdYlGn",
# #             zmin=-1,
# #             zmax=1,
# #             hovertemplate="Row: %{y}<br>Col: %{x}<br>NDVI: %{z:.3f}<extra></extra>",
# #             colorbar=dict(title="NDVI"),
# #         )
# #     )

# #     fig.update_layout(
# #         xaxis=dict(
# #             title="Column index",
# #             scaleanchor="y",
# #             scaleratio=1
# #         ),
# #         yaxis=dict(
# #             title="Row index",
# #             autorange="reversed"
# #         ),
# #         height=1000,
# #         width=int(1000 / aspect_ratio),
# #         margin=dict(l=40, r=20, t=50, b=40),
# #     )

# #     st.plotly_chart(fig, use_container_width=False)

# import streamlit as st
# import rasterio
# import numpy as np
# import plotly.graph_objects as go

# # -----------------------------
# # Step 1: Configuration
# # -----------------------------
# RED_BAND = 3
# NIR_BAND = 4

# IMAGE_FILES = {
#     "14_Nov": "20241114_054915_88_24d5_3B_AnalyticMS_SR_clip.tif",
#     "16_Dec": "20241216_055040_33_24e5_3b_analyticms_sr_mosaic.tif",
#     "25_Jan": "20250125_051526_67_24c2_3b_analyticms_sr_mosaic.tif",
#     "23_Feb": "20250223_055317_82_251c_3b_analyticms_sr_mosaic.tif",
# }

# TIME_LABELS = list(IMAGE_FILES.keys())

# # -----------------------------
# # Step 2: Utility function
# # -----------------------------
# def calculate_ndvi_and_rgb(image_path):
#     with rasterio.open(image_path) as src:
#         red = src.read(RED_BAND).astype(float)
#         nir = src.read(NIR_BAND).astype(float)

#         ndvi = (nir - red) / (nir + red + 1e-10)

#         rgb = src.read([1, 2, 3]).astype(float)
#         rgb = np.transpose(rgb, (1, 2, 0))

#         rgb = (rgb - rgb.min()) / (rgb.max() - rgb.min())
#         rgb = (rgb * 255).astype(np.uint8)

#     return ndvi, rgb

# # -----------------------------
# # Step 3: Streamlit UI
# # -----------------------------
# st.set_page_config(page_title="NDVI Viewer", layout="wide")
# st.title("🌱 NDVI Viewer with Interactive NDVI Values")

# selected_date = st.selectbox("Select date:", TIME_LABELS)

# ndvi_arr, rgb_img = calculate_ndvi_and_rgb(IMAGE_FILES[selected_date])

# rows, cols = ndvi_arr.shape
# aspect_ratio = rows / cols

# DISPLAY_HEIGHT = 1000
# DISPLAY_WIDTH = int(DISPLAY_HEIGHT / aspect_ratio)

# # -----------------------------
# # Step 4: Side-by-side display
# # -----------------------------
# col1, col2 = st.columns(2)

# # -------- ORIGINAL IMAGE --------
# with col1:
#     st.subheader(f"Original RGB — {selected_date}")
#     st.image(
#         rgb_img,
#         width=DISPLAY_WIDTH   # 🔑 keeps same aspect ratio as NDVI
#     )

# # -------- NDVI HEATMAP --------
# with col2:
#     st.subheader(f"NDVI Heatmap — {selected_date}")

#     fig = go.Figure(
#         data=go.Heatmap(
#             z=ndvi_arr,
#             colorscale="RdYlGn",
#             zmin=-1,
#             zmax=1,
#             hovertemplate="Row: %{y}<br>Col: %{x}<br>NDVI: %{z:.3f}<extra></extra>",
#             colorbar=dict(title="NDVI"),
#         )
#     )

#     fig.update_layout(
#         xaxis=dict(
#             title="Column index",
#             scaleanchor="y",
#             scaleratio=1
#         ),
#         yaxis=dict(
#             title="Row index",
#             autorange="reversed"
#         ),
#         height=DISPLAY_HEIGHT,
#         width=DISPLAY_WIDTH,
#         margin=dict(l=40, r=20, t=50, b=40),
#     )

#     st.plotly_chart(fig, config={
#         "displayModeBar": False   # 🔥 hides the toolbar
#     }, use_container_width=False)
import streamlit as st
import rasterio
import numpy as np
import plotly.graph_objects as go
import requests
import os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="NDVI Viewer", layout="wide")
st.title("🌱 NDVI Viewer with Interactive NDVI Values")

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
RED_BAND = 3
NIR_BAND = 4

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

IMAGE_FILES = {
    "14_Nov": {
        "file_id": "1ASG8zzrokTj-76jqP696a0A4tv_Kq9BU",
        "local": f"{CACHE_DIR}/14_nov.tif"
    },
    "16_Dec": {
        "file_id": "1_pF2SE2y6afE3lAznouQqOekYPVhY3kE",
        "local": f"{CACHE_DIR}/16_dec.tif"
    },
    "25_Jan": {
        "file_id": "1KYmeWd79s3RVTV-gRlczR6vNmQuMF0Ik",
        "local": f"{CACHE_DIR}/25_jan.tif"
    },
    "23_Feb": {
        "file_id": "1aOKGIRoqAlYXKc4lVi18qwkkYZyru_br",
        "local": f"{CACHE_DIR}/23_feb.tif"
    },
}

TIME_LABELS = list(IMAGE_FILES.keys())

# --------------------------------------------------
# DOWNLOAD FROM GOOGLE DRIVE
# --------------------------------------------------
def download_from_drive(file_id, output_path):
    if os.path.exists(output_path):
        return output_path

    url = f"https://drive.google.com/uc?id={file_id}"
    with st.spinner("Downloading image from Google Drive..."):
        r = requests.get(url)
        r.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(r.content)

    return output_path

# --------------------------------------------------
# NDVI + RGB FUNCTION
# --------------------------------------------------
def calculate_ndvi_and_rgb(image_path):
    with rasterio.open(image_path) as src:
        red = src.read(RED_BAND).astype(float)
        nir = src.read(NIR_BAND).astype(float)

        ndvi = (nir - red) / (nir + red + 1e-10)

        rgb = src.read([1, 2, 3]).astype(float)
        rgb = np.transpose(rgb, (1, 2, 0))

        rgb = (rgb - rgb.min()) / (rgb.max() - rgb.min())
        rgb = (rgb * 255).astype(np.uint8)

    return ndvi, rgb

# --------------------------------------------------
# UI
# --------------------------------------------------
selected_date = st.selectbox("📅 Select date:", TIME_LABELS)

file_info = IMAGE_FILES[selected_date]
image_path = download_from_drive(
    file_info["file_id"],
    file_info["local"]
)

ndvi_arr, rgb_img = calculate_ndvi_and_rgb(image_path)

rows, cols = ndvi_arr.shape
aspect_ratio = rows / cols

DISPLAY_HEIGHT = 900
DISPLAY_WIDTH = int(DISPLAY_HEIGHT / aspect_ratio)

# --------------------------------------------------
# DISPLAY
# --------------------------------------------------
col1, col2 = st.columns(2)

# ---- RGB IMAGE ----
with col1:
    st.subheader(f"🖼️ Original RGB — {selected_date}")
    st.image(rgb_img, width=DISPLAY_WIDTH)

# ---- NDVI ----
with col2:
    st.subheader(f"🌿 NDVI Heatmap — {selected_date}")

    fig = go.Figure(
        data=go.Heatmap(
            z=ndvi_arr,
            colorscale="RdYlGn",
            zmin=-1,
            zmax=1,
            hovertemplate="Row: %{y}<br>Col: %{x}<br>NDVI: %{z:.3f}<extra></extra>",
            colorbar=dict(title="NDVI"),
        )
    )

    fig.update_layout(
        xaxis=dict(scaleanchor="y", scaleratio=1),
        yaxis=dict(autorange="reversed"),
        height=DISPLAY_HEIGHT,
        width=DISPLAY_WIDTH,
        margin=dict(l=30, r=20, t=40, b=30),
    )

    st.plotly_chart(
        fig,
        use_container_width=False,
        config={"displayModeBar": False}
    )
