# download_data.py

import os
import requests
import shutil
from sklearn.model_selection import train_test_split
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib.parse import urljoin  # Import urljoin to handle relative URLs
from duckduckgo_search import DDGS
import os
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# List of top 14 highest mountains
mountains = [
    "Mount Everest",
    "K2",
    "Kangchenjunga",
    "Lhotse",
    "Makalu",
    "Cho Oyu",
    "Dhaulagiri",
    "Manaslu",
    "Nanga Parbat",
    "Annapurna",
    "Gasherbrum I",
    "Broad Peak",
    "Gasherbrum II",
    "Shishapangma"
]

def search_images(mountain_name, max_images=10):
    with DDGS() as ddgs:
        search_results = ddgs.images(keywords=mountain_name, max_results=max_images, type_image="photo")
        image_data = list(search_results)
        image_urls = [item.get("image") for item in image_data[:max_images]]
        return image_urls

def download_images(mountain_name, max_images=50):
    image_urls = search_images(mountain_name, max_images + 20)
    downloaded_images = 0
    counter = 0
    while downloaded_images < max_images and counter < len(image_urls):
        url = image_urls[counter]
        try:
            img_response = requests.get(url)
            img = Image.open(BytesIO(img_response.content))
            img.save(f"data/temp/{mountain_name}/{mountain_name}_{counter + 1}.jpg")
            downloaded_images += 1
        except Exception as e:
            print(f"Could not download image {counter + 1} for {mountain_name}: {e}")
        finally:
            counter += 1

    # for i, url in enumerate(image_urls[:max_images]):
    #     try:
    #         img_response = requests.get(url)
    #         img = Image.open(BytesIO(img_response.content))
    #         img.save(f"data/temp/{mountain_name}/{mountain_name}_{i + 1}.jpg")
    #     except Exception as e:
    #         print(f"Could not download image {i + 1} for {mountain_name}: {e}")


def download_and_prepare_images():
    # Create directories for train and test datasets
    for mountain in mountains:
        os.makedirs(f"data/train/{mountain}", exist_ok=True)
        os.makedirs(f"data/test/{mountain}", exist_ok=True)
        os.makedirs(f"data/temp/{mountain}", exist_ok=True)
        download_images(mountain)  # Download images for each mountain
    print("image download complete")


def visualize_random_images(folder_path, images_per_subfolder=3):
    # Iterate through each subfolder in the main folder
    for subfolder_name in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder_name)
        
        # Check if the current path is a folder (and not a file)
        if os.path.isdir(subfolder_path):
            # Get a list of image files in the subfolder
            image_files = [f for f in os.listdir(subfolder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'))]
            
            # If there are fewer images than requested, use all of them
            images_to_display = min(images_per_subfolder, len(image_files))
            selected_images = random.sample(image_files, images_to_display)

            # Set up the matplotlib figure to display the images
            fig, axes = plt.subplots(1, images_to_display, figsize=(15, 5))
            fig.suptitle(f'Random Images from "{subfolder_name}"', fontsize=16)

        # Plot each selected image in the row
        for i, image_name in enumerate(selected_images):
            image_path = os.path.join(subfolder_path, image_name)
            image = mpimg.imread(image_path)
            axes[i].imshow(image)
            axes[i].axis('off')  # Hide axes for cleaner look
            axes[i].set_title(image_name, fontsize=10)

    # Display the row of images
    plt.tight_layout()
    plt.show()


def split_images_into_train_test_sets():
    # Split images into train and test sets
    # Assuming images are downloaded into a temporary folder
    for mountain in mountains:
        images = os.listdir(f"data/temp/{mountain}")  # List of downloaded images
        train_images, test_images = train_test_split(images, test_size=0.2)

        for img in train_images:
            shutil.move(f"data/temp/{mountain}/{img}", f"data/train/{mountain}/{img}")

        for img in test_images:
            shutil.move(f"data/temp/{mountain}/{img}", f"data/test/{mountain}/{img}")
    print("image split complete")


# download_and_prepare_images()
# visualize_random_images('data/temp')
split_images_into_train_test_sets()
