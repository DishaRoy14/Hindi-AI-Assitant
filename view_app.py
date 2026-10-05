import streamlit as st
import chromadb
import pandas as pd

st.set_page_config(page_title="ChromaDB Explorer", layout="wide")
st.title("Company Records (Vector Database)")

# Connect to the local chroma_db folder
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="company_records")

data = collection.get()
df = pd.DataFrame(data["metadatas"])

# Filter dropdown
entity = st.selectbox("Filter by Category:", ["All", "employee", "client", "invoice", "task"])

if entity != "All":
    filtered_df = df[df["entity_type"] == entity]
else:
    filtered_df = df

st.dataframe(filtered_df, use_container_width=True)