import streamlit as st
import PIL.Image

import os

from interface import display_matches, display_text_head
from helpers import load_image, resize, get_random_image_file, cache_on_button_press
from call_api import call_text_endpoint, call_photo_endpoint, call_hybrid_endpoint, call_greetings_endpoint

app_formal_name = "Image Search Engine"

# Set default endpoint. Usually this would be passed to a function via a parameter
DEFAULT_ENDPOINT = "http://127.0.0.1:8080"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    global DEFAULT_ENDPOINT
    selected_box = st.sidebar.selectbox(
        "Choose one of the following",
        (
            "Text Query",
            "Image Query",
            "Hybrid Query [Experimental]",
            "API Testing",
        ),
    )

    st.sidebar.markdown(f"{app_formal_name}")
    # st.sidebar.markdown(
    #     f"Images are sourced from the [Unsplash dataset](https://github.com/unsplash/datasets)"
    # )

    DEFAULT_ENDPOINT = st.text_input("Endpoint", DEFAULT_ENDPOINT)

    if selected_box == "Text Query":
        textq_search()
    if selected_box == "Image Query":
        imageq_search()
    if selected_box == "Hybrid Query [Experimental]":
        hybridq_search()
    if selected_box == "API Testing":
        api_test()


def textq_search():
    st.title("Search Images with Text 📝")

    # display_text_head()

    submitted = False
    matching_ids = []

    with st.form("text_search_form"):
        text_query = st.text_input(label='Enter the query', max_chars=70)
        k = st.slider("Number of Images to retrieve",
                      min_value=1, max_value=20, value=6)
        submitted = st.form_submit_button("Search")
        if submitted:
            with st.spinner('Calling API Endpoint'):
                response = call_text_endpoint(text_query, DEFAULT_ENDPOINT)

            if response.ok:
                matching_ids = response.json()['image_ids'][:k]

            else:
                st.error(
                    f'Requests Not Successful, Code: {response.status_code}, Reason: {response.reason}')

    if submitted:
        st.markdown("***")
        st.balloons()
        display_matches(matching_ids, css0, css1)


def imageq_search():
    st.title("Search Images with photo 🖼️")

    submitted = False
    matching_ids = []

    with st.form("my_form"):
        col1, col2 = st.columns(2)

        with col1:
            image = load_image(
                ROOT_DIR + get_random_image_file("./cached_images"))

            uploaded_image = st.file_uploader(
                "or upload an image", type=["jpg", "jpeg", "png"])
            if uploaded_image is not None:
                image = load_image(uploaded_image)

        with col2:
            st.image(resize(image, 400))

        k = st.slider("Number of Images to retrieve",
                      min_value=1, max_value=20, value=6)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Search")
        if submitted:
            with st.spinner('Calling API Endpoint'):
                response = call_photo_endpoint(image, DEFAULT_ENDPOINT)

            if response.ok:
                matching_ids = response.json()['image_ids'][:k]

            else:
                st.error(
                    f'Requests Not Successful, Code: {response.status_code}, Reason: {response.reason}')

    if submitted:
        st.markdown("***")
        st.balloons()
        display_matches(matching_ids, css0, css1)


def hybridq_search():
    st.title("Search Images with Text 📝 and Photo 🖼️")

    submitted = False
    matching_ids = []

    with st.form("my_form"):
        col1, col2 = st.columns(2)

        with col1:
            image = load_image(
                ROOT_DIR + get_random_image_file("./cached_images"))

            uploaded_image = st.file_uploader(
                "or upload an image", type=["jpg", "jpeg", "png"])
            if uploaded_image is not None:
                image = load_image(uploaded_image)

        with col2:
            st.image(resize(image, 400))

        text_query = st.text_input(label='Enter the query', max_chars=70)
        col3, col4 = st.columns(2)

        with col3:
            k = st.slider("Number of Images to retrieve",
                          min_value=1, max_value=3, value=3)

        with col4:
            image_weight = st.slider("Photo Weight",
                                     min_value=0.0, max_value=1.0, value=0.5, step=0.01)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Search")
        if submitted:
            with st.spinner('Calling API Endpoint'):
                response = call_hybrid_endpoint(
                    text_query, image, image_weight, DEFAULT_ENDPOINT)

            if response.ok:
                matching_ids = response.json()['image_ids'][:k]

            else:
                st.error(
                    f'Requests Not Successful, Code: {response.status_code}, Reason: {response.reason}')

    if submitted:
        st.markdown("***")
        st.balloons()
        display_matches(matching_ids, css0, css1)


def api_test():
    if st.button("Touch Me!"):
        response = call_greetings_endpoint(DEFAULT_ENDPOINT)
        if response.ok:
            st.success("heYY!! Greetings from the API")
        else:
            st.error(
                f'Awww the api is unavailable right now, Code: {response.status_code}, Reason: {response.reason}')


if __name__ == "__main__":

    with open("css/labs.css") as FIN:
        css0 = FIN.read()
    with open("css/masonry.css") as FIN:
        css1 = FIN.read()

    st.set_page_config(
        page_title=app_formal_name,
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    main()
