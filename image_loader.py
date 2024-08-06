import streamlit as st
import base64
from pexels_api import API
import os
from dotenv import load_dotenv

def render_image(filepath: str):
    """
    filepath: path to the image. Must have a valid file extension.
    """
    mime_type = filepath.split('.')[-1:][0].lower()
    with open(filepath, "rb") as f:
       content_bytes = f.read()
    content_b64encoded = base64.b64encode(content_bytes).decode()
    image_string = f'data:image/{mime_type};base64,{content_b64encoded}'
    st.image(image_string)

def get_image_from_pexel(prompt: str):
    """
    gets image url from pexel through pexel api
    """

    load_dotenv()
    # Type your Pexels API
    PEXELS_API_KEY = st.secrets['PEXEL_API_KEY']

    # Create API object
    api = API(PEXELS_API_KEY)

    # Search five 'kitten' photos
    api.search(prompt, page=1, results_per_page=1)
    # Get photo entries
    photos = api.get_entries()

    for photo in photos:
        # Print photographer
        # print('Photographer: ', photo.photographer)
        # Print url
        # print('Photo url: ', photo.url)
        # Print original size url
        # print('Photo original size: ', photo.original)

        image_data = {'url':photo.medium, 'photographer':photo.photographer}

    return image_data

import urllib.request
import requests
def download_image(url, save_as):
    """
    downloads an image from a URL
    """
    # urllib.request.urlretrieve(url, save_as)
    response = requests.get(url)
    with open(save_as, 'wb') as file:
        file.write(response.content)

if __name__ == "__main__":
    url = 'https://images.pexels.com/photos/357756/pexels-photo-357756.jpeg?auto=compress&cs=tinysrgb&h=130'
    image_name = 'test_image.jpg'
    download_image(url=url, save_as=image_name)

