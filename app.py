import os
from PIL import Image
import streamlit as st

# Determine the directory of the currently executing script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Path to the 'loras' directory
loras_path = os.path.join(script_dir, 'loras')

# Function to recursively load images from 'loras' and its subdirectories
def load_images(directory):
    images = []
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return images
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".jpeg"):  # Target specific image file extensions
                image_path = os.path.join(root, filename)
                images.append((filename, image_path))
    return images

# Function to display images in a grid
def display_images(images):
    target_size = (300, 400)  # Set the target size of each image
    cols_per_row = 4
    cols = st.columns(cols_per_row)
    for idx, (filename, image_path) in enumerate(images):
        with cols[idx % cols_per_row]:
            image = Image.open(image_path)
            # Resize and crop the image to fit the target size
            image.thumbnail(target_size, Image.LANCZOS)  # Resize image maintaining aspect ratio
            image = image.crop((0, 0, target_size[0], target_size[1]))  # Crop to fix the size
            st.image(image, caption=filename, use_column_width=True)
            if st.button(f"Add lora", key=filename):
                display_name = os.path.splitext(image_path)[0]
                lora_display_name = f"<{display_name}:1.0>"
                st.session_state['lora_display_name'] = lora_display_name
                st.session_state['show_details'] = True

# Navigation setup
st.sidebar.title('Navigation')
choice = st.sidebar.radio('Go to', ['Home', 'Lora', 'Checkpoint'])

if choice == 'Home':
    st.header('Home')
    st.write('Welcome to the Home Page!')
elif choice == 'Lora':
    st.header('Lora Files')
    images = load_images(loras_path)
    display_images(images)
    st.write('Manage your Lora here.')
elif choice == 'Checkpoint':
    st.header('Checkpoint')
    images = load_images('checkpoints')
    display_images(images)
    st.write('Manage your checkpoints here.')

# Display lora file name in popup
if 'show_details' in st.session_state and st.session_state.show_details:
    with st.expander("Lora File Details", expanded=True):
        st.write(st.session_state.lora_display_name)
        if st.button("Close Details"):
            st.session_state.show_details = False
