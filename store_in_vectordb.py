import json

import chromadb


def build_vector_database(json_file="company_data_full.json", persist_dir="./chroma_db"):
    if chromadb is None:
        raise ImportError("chromadb is required. Install it with: pip install chromadb")

    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(name="company_records")

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    metadatas = []
    ids = []

    # 1. Employees
    for e in data["employees"]:
        doc = f"Employee {e['emp_id']}: {e['name']} works in {e['department']} department as {e['role']}. Telegram Chat ID is {e['telegram_chat_id']}."
        documents.append(doc)
        metadatas.append({
            "entity_type": "employee",
            "emp_id": e["emp_id"],
            "name": e["name"],
            "department": e["department"],
            "role": e["role"],
            "telegram_chat_id": e["telegram_chat_id"]
        })
        ids.append(f"emp_{e['emp_id']}")

    # 2. Clients
    for c in data["clients"]:
        doc = f"Client {c['client_id']}: {c['name']}. Primary contact person is {c['contact_person']}."
        documents.append(doc)
        metadatas.append({
            "entity_type": "client",
            "client_id": c["client_id"],
            "name": c["name"],
            "contact_person": c["contact_person"]
        })
        ids.append(f"cli_{c['client_id']}")

    # 3. Invoices
    for i in data["invoices"]:
        doc = f"Invoice {i['invoice_id']} for client {i['client_name']}. Total: ₹{i['total_amount_inr']:,}, Paid: ₹{i['paid_amount_inr']:,}, Due amount: ₹{i['due_amount_inr']:,}, Due date: {i['due_date']}, Status: '{i['status']}'."
        documents.append(doc)
        metadatas.append({
            "entity_type": "invoice",
            "invoice_id": i["invoice_id"],
            "client_name": i["client_name"],
            "total_amount_inr": i["total_amount_inr"],
            "paid_amount_inr": i["paid_amount_inr"],
            "due_amount_inr": i["due_amount_inr"],
            "due_date": i["due_date"],
            "status": i["status"]
        })
        ids.append(f"inv_{i['invoice_id']}")

    # 4. Tasks
    for t in data["tasks"]:
        blocker_text = f" Blocker reason: '{t['blocker']}'." if t.get("blocker") else ""
        doc = f"Task {t['task_id']}: '{t['title']}'. Status: '{t['status']}'.{blocker_text} Assigned to {t['assigned_to_name']} ({t['assigned_to_emp_id']}) in {t['department']}. Deadline is {t['deadline']}, last updated at {t['last_updated_at']}."
        documents.append(doc)
        metadatas.append({
            "entity_type": "task",
            "task_id": t["task_id"],
            "title": t["title"],
            "assigned_to_name": t["assigned_to_name"],
            "assigned_to_emp_id": t["assigned_to_emp_id"],
            "department": t["department"],
            "deadline": t["deadline"],
            "status": t["status"],
            "blocker": t.get("blocker") or "None",
            "last_updated_at": t["last_updated_at"]
        })
        ids.append(f"task_{t['task_id']}")

    # Add all documents (Chroma automatically computes embeddings)
    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    print(f"Ingested {len(documents)} records into ChromaDB collection 'company_records'.")

if __name__ == "__main__":
    build_vector_database()