import streamlit as st
import base64

def display_matches(matching_ids, css0, css1):
    divs = [
        f"""
        <div class="brick">
        <img src="https://source.unsplash.com/{idx}">
        </div>
        """
        for idx in matching_ids
    ]
    divs = "\n".join(divs)

    html = """
    <html>
      <base target="_blank" />
      <head>
        <style> %s </style>
        <style> %s </style>
      </head>
      <body>
      <div class="masonry">
      %s
      </div>
      </body>
    </html>
    """ % (
        css0,
        css1,
        divs,
    )

    st.components.v1.html(html, height=2400, scrolling=True)


# LOGO_IMAGE = "logo.png"
#
# def display_text_head():
#     st.markdown(
#         """
#         <style>
#         .container {
#             display: flex;
#             position: relative;
#         }
#         .logo-text {
#             font-family: "Source Sans Pro", sans-serif;
#             font-weight:700 !important;
#             font-size:50px !important;
#             # color: #f9a01b !important;
#             # padding-bottom: 75px !important;
#         }
#         .logo-img {
#             float:right;
#             width:60px !important;
#             height:60px !important;
#             # padding-top: 40px !important;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

#     st.markdown(
#         f"""
#         <div class="container">
#             <p class="logo-text">Search Images with Text&nbsp;</p>
#             <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
