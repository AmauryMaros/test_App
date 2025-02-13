import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_pdf_viewer import pdf_viewer
import requests
from io import StringIO
from io import BytesIO
from PIL import Image

st.set_page_config(layout="wide")
st.sidebar.subheader("Contact")
st.sidebar.write("jholm@som.umaryland.edu")

######################################## ----- DATA IMPORTATION ----- ########################################

mgcsts_samples_url = "https://www.dropbox.com/scl/fi/s539pqw7a65t1sn9oajm8/samples_w_mgCSTs.csv?rlkey=ct2ttbmobdqce2tcmgsetbbs0&st=rugbr93w&dl=1"
mgcsts_url = "https://www.dropbox.com/scl/fi/0wke2p4xluoimlbtbsz0f/mgCSTs.csv?rlkey=vmusr5cvwqcz3okbq3vpztoa2&st=vm9vvfws&dl=1"
projects_url = "https://www.dropbox.com/scl/fi/8es1gk08lt71wgum2mgqa/VIRGO_participants_anonymous.csv?rlkey=zl820misc8gj0jd343z83fv4r&st=tskmwdjp&dl=1"
new_vs_old_url = "https://www.dropbox.com/scl/fi/opfvh3g451h2999hrs5ao/new_vs_old_mgcsts.csv?rlkey=q4b8k5cw8qd8pg6noq0934b6h&st=bexfo2l5&dl=1"
pheatmap_url = "https://www.dropbox.com/scl/fi/vj5i7xgkxzrgy15zad016/pheatmap.png?rlkey=rou4sz8a8s12fhhr0hzid22fw&st=gwugusfx&dl=1"

response = requests.get(mgcsts_samples_url)
if response.status_code == 200:
      # Read CSV file from the response content
      data = StringIO(response.text)
      mgcsts_samples = pd.read_csv(data)
else:
      st.error("Failed to download file. Please check the URL.")

response = requests.get(mgcsts_url)
if response.status_code == 200:
      # Read CSV file from the response content
      data = StringIO(response.text)
      mgcsts = pd.read_csv(data)
else:
      st.error("Failed to download file. Please check the URL.")

response = requests.get(projects_url)
if response.status_code == 200:
      # Read CSV file from the response content
      data = StringIO(response.text)
      projects = pd.read_csv(data)
else:
      st.error("Failed to download file. Please check the URL.")

response = requests.get(new_vs_old_url)
if response.status_code == 200:
      # Read CSV file from the response content
      data = StringIO(response.text)
      new_vs_old = pd.read_csv(data)
else:
      st.error("Failed to download file. Please check the URL.")

response = requests.get(pheatmap_url)
if response.status_code == 200:
    # Get the file content
    file_content = response.content
    pheatmap = Image.open(BytesIO(file_content))
else:
      st.error("Failed to download file. Please check the URL.")
      
# mgcsts_samples = pd.read_csv("volume/data/samples_w_mgCSTs.csv")
# mgcsts = pd.read_csv("volume/data/mgCSTs.csv")
# projects = pd.read_csv("volume/data/VIRGO_participants_anonymous.csv")

######################################## ----- DATA PROCESSING ----- #############################################

mgcsts_samples_project = mgcsts_samples.merge(projects, on = "sampleID", how = "left")
df2 = mgcsts_samples_project.groupby(["Geography", "mgCST"]).size().reset_index().pivot(columns='Geography', index = 'mgCST', values =0).reset_index()

color_pal = {'Africa':'#EE4266' , 'Asia':'#000000' , 'Europe':'#FFD23F' , 'NorthAmer':'#599cd9' , 'Oceania':'#0EAD69'}

# Calculate count_sample for each mgCST
count_sample = mgcsts_samples['mgCST'].value_counts().reset_index()
count_sample.columns = ['mgCST', 'count_sample']

# Merge with mgCSTs to get the color and domTaxa columns
count_sample = count_sample.merge(mgcsts[['mgCST', 'color', 'domTaxa']], on='mgCST', how='left')

# Ensure mgCST is treated as a categorical variable with sorted levels
count_sample['mgCST'] = pd.Categorical(count_sample['mgCST'], categories=sorted(count_sample['mgCST'].unique()), ordered=True)

# Create a color map for mgCST to color
color_map = dict(zip(count_sample['mgCST'], count_sample['color']))

######################################## ----- PAGE CONTENT ----- ########################################

st.container()

col1, col2, col3 = st.columns(3)

# Barplot mgcsts - number of samples colored by dominant Taxa
with col1 :

    fig = px.bar(
        count_sample,
        x='mgCST',
        y='count_sample',
        color='mgCST',
        hover_data=['domTaxa'],
        color_discrete_map=color_map, 
        labels={"count_sample" : "Number of samples"},
        title = "Distribution and prevalence of mgCSTs",
        category_orders={"mgCST": sorted(count_sample['mgCST'].unique())}
        )

    # Customize layout
    fig.update_layout(
        xaxis_title='mgCST',
        yaxis_title='Number of samples',
        template="plotly_white"
    )

    fig.update_xaxes(tickmode='array', tickvals=mgcsts['mgCST'])

    fig.update_layout(
        xaxis=dict(
            tickangle=0,  # Change the angle of the tick labels
            tickfont=dict(size=10)  # Change the size of the tick labels
        ))
    
    st.plotly_chart(fig, use_container_width=True)

# Stacked barplot mgcsts - number of samples colored by project
with col2 :

    fig = px.bar(
        df2, 
        x='mgCST', 
        y=df2.drop('mgCST', axis=1).columns.values, 
        labels={'value' : 'Number of samples'},
        color_discrete_map=color_pal,
        title = f"Distribution and prevalence of mgCSTs by region")
       
    fig.update_xaxes(tickmode='array', tickvals=mgcsts['mgCST'])

    fig.update_layout(
    xaxis=dict(
        tickangle=0,  # Change the angle of the tick labels
        tickfont=dict(size=10)  # Change the size of the tick labels
        ))
    fig.update_layout(
    legend=dict(
        title = 'Geography',
        # traceorder='reversed'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col3 :
    # new_vs_old = pd.read_csv("volume/data/new_vs_old_mgcsts.csv")
    bubble_data = new_vs_old.groupby(['new_mgCST', 'old_mgCST']).size().reset_index(name='count')
    bubble_data = bubble_data.rename(columns={"new_mgCST":"mgCST"})

    bubble_color = []
    mgcsts['mgCST'] = mgcsts['mgCST'].astype(int)
    for i in sorted(bubble_data['mgCST'].unique()):
        bubble_color.append(mgcsts[mgcsts['mgCST'] == i]['color'].values[0])

    bubble_data['mgCST'] = bubble_data['mgCST'].astype(str)
    fig = px.scatter(
        bubble_data,
        x='mgCST',
        y = 'old_mgCST',
        color='mgCST',
        color_discrete_sequence=list(bubble_color),
        size='count',
        title = "Distribution and prevalence of mgCSTs - Comparison between mgCST v1 and mgCST v2")
    
    fig.update_xaxes(tickmode='array', tickvals=mgcsts['mgCST'])
    fig.update_yaxes(tickmode='array', tickvals=np.arange(1,28))

    fig.update_layout(
        
        xaxis=dict(
            tickangle=0,  # Change the angle of the tick labels
            tickfont=dict(size=10)  # Change the size of the tick labels
        ),

        yaxis=dict(
            tickangle=0,  # Change the angle of the tick labels
            tickfont=dict(size=10)  # Change the size of the tick labels
        ),
    )

    st.plotly_chart(fig, use_container_width=True)


st.subheader("Most abund species per mgCSTs")
with st.expander("Show table"):
    st.dataframe(mgcsts[['mgCST','domTaxa','meanRelabund','color']].set_index(['mgCST']))


# MgCSTS HEATMAP construction - button option

st.subheader("MgCSTs heatmap")
st.image(pheatmap)
# st.image("volume/medias/pheatmap.png")
# pdf_viewer("medias/mgCST_VOG_heatmap.pdf")
