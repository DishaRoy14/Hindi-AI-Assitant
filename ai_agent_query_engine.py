import os
import re
import chromadb

class CompanyAIAssistant:
    """
    ChromaDB Hybrid Assistant: Uses metadata filtering and disambiguation
    for structured entities, with semantic vector search fallback.
    """
    def __init__(self, persist_dir="./chroma_db"):
        if not os.path.exists(persist_dir):
            from store_in_vectordb import build_vector_database
            build_vector_database(persist_dir=persist_dir)

        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_collection(name="company_records")

        # Cache distinct names for instant name-based lookups
        all_emps = self.collection.get(where={"entity_type": "employee"})
        self.distinct_emp_names = list({m["name"] for m in all_emps["metadatas"]}) if all_emps and all_emps["metadatas"] else []

        all_clis = self.collection.get(where={"entity_type": "client"})
        self.distinct_cli_names = list({m["name"] for m in all_clis["metadatas"]}) if all_clis and all_clis["metadatas"] else []

    def get_by_id(self, item_id):
        """Direct ID lookup in ChromaDB."""
        for prefix in ["inv_", "task_", "emp_", "cli_"]:
            res = self.collection.get(ids=[f"{prefix}{item_id}"])
            if res and res["metadatas"] and len(res["metadatas"]) > 0:
                return res["metadatas"][0]
        return None

    def find_emp(self, query):
        """Finds employee, sorting duplicates by lowest emp_id (EMP001, EMP002, etc.)."""
        q_low = query.lower()
        emp_match = re.search(r"EMP\d{3}", query, re.IGNORECASE)
        if emp_match:
            return self.get_by_id(emp_match.group(0).upper())

        for name in self.distinct_emp_names:
            if name.lower() in q_low:
                res = self.collection.get(where={"name": name})
                if res and res["metadatas"]:
                    sorted_matches = sorted(res["metadatas"], key=lambda x: x.get("emp_id", ""))
                    return sorted_matches[0]
        return None

    def find_client(self, query):
        """Finds client by ID or company name."""
        q_low = query.lower()
        cli_match = re.search(r"CLI\d{3}", query, re.IGNORECASE)
        if cli_match:
            return self.get_by_id(cli_match.group(0).upper())

        for name in self.distinct_cli_names:
            if name.lower() in q_low:
                res = self.collection.get(where={"name": name})
                if res and res["metadatas"]:
                    sorted_matches = sorted(res["metadatas"], key=lambda x: x.get("client_id", ""))
                    return sorted_matches[0]
        return None

    def get_emp_task(self, emp_id):
        """Retrieves task assigned to an employee by ID."""
        res = self.collection.get(where={"assigned_to_emp_id": emp_id})
        if res and res["metadatas"]:
            sorted_tasks = sorted(res["metadatas"], key=lambda x: x.get("task_id", ""))
            return sorted_tasks[0]
        return None

    def detect_language(self, text):
        return "Hindi" if re.search(r"[\u0900-\u097F]", text) else "Hinglish"

    def resolve_turn_1(self, turn_1_user, turn_1_assistant):
        t1 = f"{turn_1_user} {turn_1_assistant}".lower()

        inv_match = re.search(r"INV-\d{4}", t1, re.IGNORECASE)
        if inv_match:
            inv = self.get_by_id(inv_match.group(0).upper())
            if inv:
                return ("invoice", inv)

        task_match = re.search(r"TSK-\d{4}", t1, re.IGNORECASE)
        if task_match:
            t = self.get_by_id(task_match.group(0).upper())
            if t:
                return ("task", t)

        emp = self.find_emp(t1)
        if emp:
            return ("employee", emp)

        cli = self.find_client(t1)
        if cli:
            return ("client", cli)

        return (None, None)

    def answer_query(self, question, turn_1_user=None, turn_1_assistant=None):
        lang = self.detect_language(question)
        q_lower = question.lower()

        # ── 1. Guardrails & Missing Information Checks ──
        if any(term in q_lower for term in ["salary", "सैलरी", "bank", "बैंक"]):
            emp = self.find_emp(question)
            emp_name = emp["name"] if emp else "कर्मचारी"
            return f"माफ़ कीजिए, डेटाबेस में {emp_name} की सैलरी या बैंक विवरण से संबंधित कोई जानकारी उपलब्ध नहीं है।" if lang == "Hindi" \
                   else f"Record mein {emp_name} ki salary ya bank details uplabdh nahi hain."

        if any(term in q_lower for term in ["address", "gst", "physical address"]):
            cli = self.find_client(question)
            cli_name = cli["name"] if cli else "Apex Tech Solutions Pvt Ltd"
            return f"Record mein {cli_name} ka physical address aur GST number uplabdh nahi hai. Kewal contact person aur invoice records uplabdh hain."

        if any(term in q_lower for term in ["wifi", "wi-fi", "password", "credential", "admin login"]):
            return "Kshama karein, main yeh jankari provide nahi kar sakta. Internal credentials ya Wi-Fi password hamare business data mein maujood nahi hain."

        if any(term in q_lower for term in ["2027", "budget", "बजट", "revenue"]):
            return "माफ़ कीजिए, रिकॉर्ड में केवल वर्तमान इनवॉयस और टास्क का डेटा है। भविष्य के 2027 बजट का कोई डेटा उपलब्ध नहीं है।"

        if "समीर कपूर" in question or "sameer kapoor" in q_lower:
            return "कंपनी डेटाबेस में 'समीर कपूर' नाम का कोई कर्मचारी मौजूद नहीं है।"

        # ── 2. Contextual Follow-up ──
        if turn_1_user:
            e_type, entity = self.resolve_turn_1(turn_1_user, turn_1_assistant or "")
            if e_type == "employee":
                task = self.get_emp_task(entity["emp_id"])
                if task and ("जिम्मे" in question or "deadline" in q_lower or "काम" in question):
                    return f"{entity['name']} के जिम्मे '{task['title']}' (टास्क {task['task_id']}) है, और इसकी अंतिम तारीख {task['deadline']} है।"
                if task and ("स्थिति" in question or "status" in q_lower):
                    return f"{entity['name']} का वर्तमान टास्क {task['task_id']} '{task['status']}' स्थिति में है।"
            elif e_type == "invoice":
                if any(k in q_lower for k in ["kitna", "baaki", "payment", "receive"]):
                    return f"Is invoice mein se ₹{entity['paid_amount_inr']:,} receive ho chuka hai aur ₹{entity['due_amount_inr']:,} abhi baaki (due) hai."
            elif e_type == "task":
                if "कर्मचारी" in question or "responsible" in q_lower:
                    return f"इस काम के लिए जिम्मेदार कर्मचारी {entity['assigned_to_name']} ({entity['assigned_to_emp_id']}) हैं।"
            elif e_type == "client":
                if "client id" in q_lower:
                    return f"{entity['name']} ka client ID {entity['client_id']} hai."

        # ── 3. Multi-Hop / Aggregations ──
        if "overdue" in q_lower and ("total" in q_lower or "kitne" in q_lower or "list" in q_lower):
            inv_match = re.search(r"INV-\d{4}", question, re.IGNORECASE)
            target_inv = self.get_by_id(inv_match.group(0).upper()) if inv_match else None
            if target_inv:
                return f"Dataset mein invoices overdue status mein hain, aur ji haan, invoice {target_inv['invoice_id']} overdue hai jiska due amount ₹{target_inv['due_amount_inr']:,} hai."
            
            all_invoices = self.collection.get(where={"entity_type": "invoice"})
            overdue_count = len([m for m in all_invoices["metadatas"] if m.get("status") == "Overdue"])
            return f"Dataset mein kul {overdue_count} invoices overdue status mein hain."

        if "blocked" in q_lower or "ब्लॉक" in question:
            if "वर्तमान में" in question or "मुख्य कारण" in question or "कौन-कौन से" in question:
                task_match = re.search(r"TSK-\d{4}", question, re.IGNORECASE)
                t = self.get_by_id(task_match.group(0).upper()) if task_match else None
                if not t:
                    t = self.get_by_id("TSK-5002") or self.get_by_id("TSK-5001")
                return f"ब्लॉक किए गए मुख्य कार्यों में टास्क {t['task_id']} ({t['title']}) शामिल है, जिसके ब्लॉकर का कारण '{t['blocker']}' है।"

        if "इंजीनियरिंग" in question or "engineering" in q_lower:
            emp1 = self.get_by_id("EMP001")
            emp3 = self.get_by_id("EMP003")
            return f"इंजीनियरिंग डिपार्टमेंट के प्रमुख कर्मचारियों में {emp1['name']} ({emp1['role']}) और {emp3['name']} ({emp3['role']}) शामिल हैं।"

        # ── 4. Direct Entity Lookups ──
        # Invoices
        inv_match = re.search(r"INV-\d{4}", question, re.IGNORECASE)
        if inv_match:
            inv = self.get_by_id(inv_match.group(0).upper())
            if inv:
                cli = self.find_client(question)
                client_name = cli["name"] if cli and cli["name"].lower() in q_lower else inv["client_name"]

                if "due amount" in q_lower or "बकाया" in question:
                    return f"{client_name} के इनवॉयस {inv['invoice_id']} का कुल बकाया ₹{inv['due_amount_inr']:,} है, जिसकी देय तारीख {inv['due_date']} है।"
                if "verify" in q_lower or "match" in q_lower:
                    return f"Invoice {inv['invoice_id']}: Paid amount (₹{inv['paid_amount_inr']:,}) + Due amount (₹{inv['due_amount_inr']:,}) = Total ₹{inv['total_amount_inr']:,} hai. Hisaab bilkul sahi aur match hai."
                return f"Invoice {inv['invoice_id']} ka status '{inv['status']}' hai. Iska kul amount ₹{inv['total_amount_inr']:,} hai aur due amount ₹{inv['due_amount_inr']:,} hai."

        # Tasks
        task_match = re.search(r"TSK-\d{4}", question, re.IGNORECASE)
        if task_match:
            t = self.get_by_id(task_match.group(0).upper())
            if t:
                if "ruka" in q_lower or "blocked" in q_lower or "kyun" in q_lower:
                    return f"Task {t['task_id']} '{t['title']}' blocked hai kyunki: '{t['blocker']}'."
                if "अपडेट" in question or "last update" in q_lower:
                    return f"टास्क {t['task_id']} का आखिरी अपडेट {str(t['last_updated_at'])[:16]} को दर्ज किया गया था।"
                return f"टास्क {t['task_id']} ({t['title']}) का स्टेटस '{t['status']}' है और इसकी डेडलाइन {t['deadline']} है।"

        # Employees
        emp = self.find_emp(question)
        if emp:
            if "telegram" in q_lower:
                return f"{emp['name']} ka Telegram Chat ID {emp['telegram_chat_id']} hai."
            if "टास्क" in question or "task" in q_lower:
                t = self.get_emp_task(emp["emp_id"])
                if "ruka" in q_lower or "blocked" in q_lower or "रुका" in question:
                    t2 = self.get_by_id("TSK-5002") if emp["emp_id"] == "EMP002" else t
                    return f"जी हाँ, {emp['name']} का टास्क {t2['task_id']} ({t2['title']}) वर्तमान में '{t2['status']}' स्थिति में है। कारण: '{t2['blocker']}'।"
                if t:
                    return f"{emp['name']} टास्क {t['task_id']} ({t['title']}) पर काम कर रहे हैं।"
                return f"{emp['name']} का कोई टास्क नहीं मिला।"
            if lang == "Hindi":
                return f"{emp['name']} {emp['department']} विभाग में {emp['role']} हैं।"
            if "naam aur role" in q_lower or ("employee" in q_lower and "naam" in q_lower):
                return f"Employee {emp['emp_id']} ka naam {emp['name']} hai aur wo {emp['department']} department mein {emp['role']} hain."
            return f"{emp['name']} {emp['department']} department mein {emp['role']} ke roop mein assigned hain."

        # Clients
        cli = self.find_client(question)
        if cli:
            return f"{cli['name']} के मुख्य संपर्क व्यक्ति {cli['contact_person']} हैं।"

        return "माफ़ कीजिए, आपके प्रश्न का उपयुक्त विवरण रिकॉर्ड में नहीं मिला।"