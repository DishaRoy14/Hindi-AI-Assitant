import chromadb
import pandas as pd

# Connect to local ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="company_records")

# Fetch all records
data = collection.get()

# Convert metadata to a pandas DataFrame
df = pd.DataFrame(data["metadatas"])

print(f"Total Records in Vector DB: {len(df)}\n")

# Preview by category:
print("--- EMPLOYEES (First 5) ---")
print(df[df["entity_type"] == "employee"][["emp_id", "name", "department", "role"]].head())

print("\n--- INVOICES (First 5) ---")
print(df[df["entity_type"] == "invoice"][["invoice_id", "client_name", "total_amount_inr", "due_amount_inr", "status"]].head())

print("\n--- TASKS (First 5) ---")
print(df[df["entity_type"] == "task"][["task_id", "title", "assigned_to_name", "status", "deadline"]].head())