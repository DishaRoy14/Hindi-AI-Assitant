import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="company_records")

print("ChromaDB total indexed records:", collection.count())

# Test a semantic search
query = "Rahul Sharma ka department aur designation kya hai?"
results = collection.query(query_texts=[query], n_results=1)

print("\nQuery:", query)
print("Top Matched Document:", results["documents"][0][0])