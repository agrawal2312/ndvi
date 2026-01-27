# import streamlit as st
# import os
# import sys

# # --------------------------------------------------
# # PAGE CONFIG
# # --------------------------------------------------
# st.set_page_config(page_title="NDVI Dashboard", layout="wide")

# # def resource_path(relative_path):
# #     if getattr(sys, 'frozen', False):
# #         return os.path.join(sys._MEIPASS, relative_path)
# #     return os.path.abspath(relative_path)
# if getattr(sys, 'frozen', False):
#     os.chdir(sys._MEIPASS)
# # --------------------------------------------------
# # HOME PAGE CONTENT
# # --------------------------------------------------
# st.title("🌱 NDVI Dashboard")

# st.write("""
# Welcome to the NDVI Dashboard!  
# This app brings together three NDVI exploration tools:

# - 🗺️ **NDVI Map Viewer** → Explore georeferenced NDVI overlays on a basemap and click pixels for time series.
# - 📈 **NDVI Time Series Viewer** → Click on a pixel in the NDVI stack to see its NDVI trend across dates.
# - 🖼️ **NDVI Single Image Viewer** → Compare RGB and NDVI heatmap for individual satellite images.

# Use the sidebar on the left to navigate between these tools.
# """)

# st.info("👈 Select a page from the sidebar to get started.")



## mew one code 
# import os
# import sys
# import streamlit as st

# st.set_page_config(page_title="NDVI Dashboard", layout="wide")

# def resource_path(rel_path):
#     base = os.path.dirname(__file__)
#     return os.path.join(base, rel_path)

# st.title("🌱 NDVI Dashboard")

# st.write("""
# Welcome to the NDVI Dashboard!

# - 🗺️ NDVI Map Viewer
# - 📈 NDVI Time Series Viewer
# - 🖼️ NDVI Single Image Viewer
# """)

# st.info("👈 Select a page from the sidebar")
import os
import sys
import socket
import streamlit as st
import qrcode
from io import BytesIO

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="NDVI Dashboard", layout="wide")

# -------------------------------
# QR CODE SECTION (NEW)
# -------------------------------
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "localhost"
    finally:
        s.close()
    return ip

PORT = 8501
APP_URL = f"http://{get_local_ip()}:{PORT}"

qr = qrcode.make(APP_URL)
buf = BytesIO()
qr.save(buf, format="PNG")
buf.seek(0)

# Show QR in sidebar (BEST PRACTICE)
st.sidebar.markdown("### 📱 Scan to Open App")
st.sidebar.image(buf, width=200)
st.sidebar.caption(APP_URL)

# -------------------------------
# Existing Functions
# -------------------------------
def resource_path(rel_path):
    base = os.path.dirname(__file__)
    return os.path.join(base, rel_path)

# -------------------------------
# Main UI (UNCHANGED)
# -------------------------------
st.title("🌱 NDVI Dashboard")


