import streamlit as st
import requests

import json

import base64
from io import BytesIO

HEADERS = {"Content-Type": "application/json", "accept": "application/json"}


def encode_image(image_query):
    buffered = BytesIO()
    image_query.save(buffered, format=image_query.format)
    return base64.b64encode(buffered.getvalue())


@st.cache(ttl=3600)
def call_text_endpoint(text_query: str, endpoint: str):
    data = json.dumps({"text_query": text_query})
    endpoint += "/api/v1/text"
    response = requests.post(endpoint, data=data, headers=HEADERS)

    return response


@st.cache(ttl=3600)
def call_photo_endpoint(image_query, endpoint: str):
    enc_image = encode_image(image_query)

    data = json.dumps({"image_query": str(enc_image)[2:-1]})
    endpoint += "/api/v1/photo"
    response = requests.post(endpoint, data=data, headers=HEADERS)

    return response


@st.cache(ttl=3600)
def call_hybrid_endpoint(text_query, image_query, image_weight, endpoint: str):
    enc_image = encode_image(image_query)

    data = json.dumps({"text_query": text_query, "image_query": str(
        enc_image)[2:-1], "image_weight": image_weight})
    endpoint += "/api/v1/hybrid"
    response = requests.post(endpoint, data=data, headers=HEADERS)

    return response


async def call_recommender_api(text_query: str):
    data = json.dumps({"query": text_query})
    endpoint = st.secrets["RECOMMENDER_ENDPOINT"]
    response = requests.post(endpoint, data, headers=HEADERS)

    print()

    if response.ok:
        if len(response.json()) >= 3:
            return response.json()[:3]
        return response.json()
    return []


def call_greetings_endpoint(endpoint: str):
    endpoint += "/api/v1/hello"
    response = requests.get(endpoint, headers={"accept": "application/json"})

    return response
