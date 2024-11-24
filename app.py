import streamlit as st
import pandas as pd
from PIL import Image

# Load Metadata
metadata_file = "metadata.csv"  # Path to your CSV file
images_folder = "images/"  # Folder where images are stored
metadata = pd.read_csv(metadata_file)

# App title
st.title("Image Metadata Editor")

# Initialize session state for the current index
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# Get the current row
current_index = st.session_state.current_index
row = metadata.iloc[current_index]

# Display the image
image_path = f"{images_folder}/{row['filename']}"  # Assuming 'filename' is the column with image names
try:
    st.image(Image.open(image_path), caption=row['filename'], use_column_width=True)
except FileNotFoundError:
    st.error(f"Image {row['filename']} not found in {images_folder}.")

# Editable fields
st.write("### Metadata:")
projection = st.text_input("Projection", row["projection"])
presentation = st.text_area("Presentation", row["presentation"])
findings = st.text_area("Findings", row["findings"])

# Optional fields
age = st.number_input("Age", value=row["age"], min_value=0, step=1)
gender = st.selectbox("Gender", options=["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(row["gender"]))

# Save changes
if st.button("Save Changes"):
    metadata.at[current_index, "projection"] = projection
    metadata.at[current_index, "presentation"] = presentation
    metadata.at[current_index, "findings"] = findings
    metadata.at[current_index, "age"] = age
    metadata.at[current_index, "gender"] = gender
    metadata.to_csv(metadata_file, index=False)
    st.success("Changes saved!")

# Navigation
col1, col2 = st.columns(2)
if col1.button("Previous") and current_index > 0:
    st.session_state.current_index -= 1
if col2.button("Next") and current_index < len(metadata) - 1:
    st.session_state.current_index += 1
