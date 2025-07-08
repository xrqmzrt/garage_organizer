import streamlit as st
import pandas as pd
from PIL import Image
import os

# Configure page for mobile use
st.set_page_config(page_title="Garage Organizer", layout="centered")

excel_file = "garage_inventory.xlsx"
photo_folder = "uploaded_photos"
os.makedirs(photo_folder, exist_ok=True)

# Load or initialize the Excel database
try:
    df = pd.read_excel(excel_file)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Bin ID", "Item Name", "Description", "Location", "Photo Filename"])

st.title("📦 Garage Organizer")

# Form to add new items
with st.form("submit_form"):
    bin_id = st.text_input("Bin ID")
    item_name = st.text_input("Item Name")
    description = st.text_area("Description")
    location = st.text_input("Location")
    photo = st.file_uploader("Upload a Photo", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Submit")

    if submitted:
        photo_filename = ""
        if photo:
            photo_filename = f"{bin_id}_{item_name.replace(' ', '_')}.jpg"
            image = Image.open(photo)
            image.save(os.path.join(photo_folder, photo_filename))

        new_row = {
            "Bin ID": bin_id,
            "Item Name": item_name,
            "Description": description,
            "Location": location,
            "Photo Filename": photo_filename
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(excel_file, index=False)
        st.success(f"✅ Item '{item_name}' added to Bin {bin_id}!")

# Gallery View
st.header("📁 View Items")
selected_bin = st.selectbox("Filter by Bin ID", options=["All"] + sorted(df["Bin ID"].dropna().unique()))

for _, row in df.iterrows():
    if selected_bin != "All" and row["Bin ID"] != selected_bin:
        continue
    st.subheader(f"{row['Item Name']} ({row['Bin ID']})")
    st.caption(f"📍 {row['Location']}")
    st.write(row["Description"])
    if row["Photo Filename"]:
        image_path = os.path.join(photo_folder, row["Photo Filename"])
        if os.path.exists(image_path):
            st.image(image_path, width=250)
