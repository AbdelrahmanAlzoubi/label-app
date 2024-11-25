import streamlit as st
import pandas as pd
from PIL import Image
from github import Github
import os

# Authenticate with GitHub
# Use an environment variable to securely store your token (recommended)
g = Github("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")
repo = g.get_repo("wolfabod/label-app")

FILE_PATH = "metadata.csv"  # Path to metadata.csv in your GitHub repo

# Load Metadata
metadata_file = FILE_PATH  # Path to your local CSV file
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
    # Update the metadata dataframe locally
    metadata.at[current_index, "projection"] = projection
    metadata.at[current_index, "presentation"] = presentation
    metadata.at[current_index, "findings"] = findings
    metadata.at[current_index, "age"] = age
    metadata.at[current_index, "gender"] = gender

    # Save the updated metadata locally
    metadata.to_csv(metadata_file, index=False)
    st.success("Changes saved locally!")

    # Push changes to GitHub
    try:
        # Get the file to update from the repository
        contents = repo.get_contents(FILE_PATH)

        # Read the updated local file
        with open(metadata_file, "r") as file:
            updated_content = file.read()

        # Update the file on GitHub
        repo.update_file(
            path=contents.path,
            message="Update metadata",
            content=updated_content,
            sha=contents.sha
        )
        st.success("Changes successfully pushed to GitHub!")
    except Exception as e:
        st.error(f"Failed to push changes to GitHub: {e}")

# Navigation
col1, col2 = st.columns(2)
if col1.button("Previous") and current_index > 0:
    st.session_state.current_index -= 1
if col2.button("Next") and current_index < len(metadata) - 1:
    st.session_state.current_index += 1
