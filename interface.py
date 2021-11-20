import streamlit as st


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
