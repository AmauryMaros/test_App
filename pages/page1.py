import streamlit as st
import requests
from io import BytesIO
from PIL import Image

st.set_page_config(page_title='Home', layout="centered")

st.sidebar.subheader("Contact")
st.sidebar.write("jholm@som.umaryland.edu")

# st.image("volume/medias/Holm_Lab_Logo.png")

st.title("Metagenomic Community State Types version 2")


url = 'https://www.dropbox.com/scl/fi/kirucs458wj9aoqbws5n9/Holm_Lab_Logo.png?rlkey=gm07ttdc28qe9wsptinpyeokg&st=p9c844w4&dl=0'  # Replace with your shareable file link

direct_download_url = url.replace('dl=0', 'dl=1')

response = requests.get(direct_download_url)

# Check if the request is successful
if response.status_code == 200:
    # Print the content type to verify it's an image
    # st.write(f"Content-Type: {response.headers['Content-Type']}")

    # Get the file content
    file_content = response.content

    # Check if the content looks like an image (optional)
    try:
        image = Image.open(BytesIO(file_content))
        st.image(image, caption="Uploaded Image", use_container_width=True)
        # st.header("Version 2")

        st.markdown('''<div style="text-align: justify;">Metagenomic CSTs (mgCSTs) were developed to explore functionally distinct vaginal microbiomes using the genetic underpinnings of the constituent vaginal bacteria. \
                    Recently, the genetic repertoire of the vaginal microbiome has been substantially expanded through VIRGO2.0, necessitating an overhaul of the original metagenomic subspecies and mgCSTs. \
                    Together, VIRGO2.0 with mgSs and mgCSTs assignment provides a streamlined tool for quantifying the relationships between the vaginal microbiome and urogenital health outcomes</div>''', unsafe_allow_html = True)

        st.write("https://www.jbholmlab.org/")

    

    except Exception as e:
        st.error(f"Error opening image: {e}")
        st.write(file_content[:500])  # Optionally show part of the response content to debug
else:
    st.error("Failed to download the image. Please check the link.")
