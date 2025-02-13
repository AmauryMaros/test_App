import streamlit as st
import pandas as pd
# import pickle
import plotly.graph_objects as go
import gc  # To manually clear unused objects from memory

st.set_page_config(layout="wide")
st.sidebar.subheader("Contact")
st.sidebar.write("jholm@som.umaryland.edu")

# # Function to lazy load CSV file with chunksize to handle large datasets
# @st.cache_data()
# def load_csv(file_path, usecols=None):
#     return pd.read_csv(file_path, usecols=usecols)
        
######################################## ----- DATA IMPORTATION ----- ########################################

# Optimize CSV loading by selecting only necessary columns
# vog_mgss_coverage = load_csv("volume/data/vog.mgSs.coverage.stats.csv")
vog_mgss_coverage = vog_mgss_coverage.rename(columns={"Unnamed: 0" : "sub_species", "as.factor(sample_cluster)" : "sample_cluster"})  # mgss coverage stats

######################################## ----- DATA PROCESSING ----- ########################################

# Species extraction
species = vog_mgss_coverage[vog_mgss_coverage['sub_species'].str.contains("\.")]['sub_species'].apply(lambda x : x.split(".")[0]).unique()

######################################## ----- PAGE CONTENT ----- ########################################

st.title("Metagenomic Subspecies (VOG-based)")

st.subheader("Visualizations")

option = st.selectbox("Species", species)

# Fetching the gene count DataFrame for the selected species
gene_count_df = pd.read_csv(f"volume/data/gene_pa_count/{option}_gene_pa_count.csv")
# gene_count_df = gene_count[option]
Gene = pd.DataFrame(gene_count_df.set_index('Gene').loc[:,gene_count_df.columns[1]:].sum(axis=1)).rename(columns={0:"Number_of_samples"}).reset_index()
Gene['%_of_samples'] = Gene['Number_of_samples'].apply(lambda x: round((100 * x / (len(gene_count_df.columns) - 1)), 2))

tab1, tab2, tab3 = st.tabs(["Species coverage", "Subspecies stats", "Presence Absence heatmap"])

with tab1:
        col1, col2 = st.columns(2)
        with col1:
                st.image(f"volume/medias/vog_mgss_coverage_png/{option}_subspecies_coverage_boxplot.png")
        with col2:
                st.image(f"volume/medias/vog_mgss_coverage_png/{option}_subspecies_coverage_by_NoVOG.png")

with tab2:
        st.subheader("Subspecies stats")
        st.dataframe(vog_mgss_coverage[vog_mgss_coverage['sub_species'].apply(lambda x: x.split(".")[0]) == option])

with tab3:
        col1, col2 = st.columns(2)
        with col1:
                st.image(f"volume/medias/vog_heatmap_presence_absence/_{option}_heatmap_presence_absence.png")
        with col2:
               df_reorder = pd.read_csv(f"volume/data/reorder_dataframe/{option}_reorder_dataframe.csv", index_col=0)
        #        df_reorder = reorder_dataframe[option]
               hover = pd.read_csv(f"volume/data/hover/{option}_hover.csv", index_col=0)
               heatmap = go.Figure(data=go.Heatmap(
                        z=df_reorder,
                        x=df_reorder.columns,
                        y=df_reorder.index,
                        colorscale=[[0, 'antiquewhite'], [1, 'mediumblue']],
                        showscale=False, 
                        hovertext=hover,
                        # hovertemplate="VOG: %{y}<br>SampleID: %{x}<br>GeneProduct: %{hovertext}<extra></extra>"
                ))
               heatmap.update_layout(
                width=3600,  # Set width in pixels
                height=900
                )
               heatmap.update_xaxes(showticklabels=False)
               heatmap.update_yaxes(showticklabels=False)
               st.plotly_chart(heatmap, use_container_width=True)

# Trigger garbage collection to free up memory
gc.collect()

