import json
import os


company_data_file = "company_data_full.json"
data = None
if os.path.exists(company_data_file):
    with open(company_data_file, "r", encoding="utf-8") as f:
        data = json.load(f)


def get_emp(emp_id):
    if data:
        return next((e for e in data["employees"] if e["emp_id"] == emp_id), None)
    return {"name": "Rahul Sharma", "department": "Engineering", "role": "Software Engineer"}

def get_client(cli_id):
    if data:
        return next((c for c in data["clients"] if c["client_id"] == cli_id), None)
    return {"name": "Apex Tech Solutions Pvt Ltd"}

def get_invoice(inv_id):
    if data:
        return next((i for i in data["invoices"] if i["invoice_id"] == inv_id), None)
    return {"invoice_id": "INV-1002", "total_amount_inr": 125000, "paid_amount_inr": 62500, "due_amount_inr": 62500, "status": "Pending", "due_date": "2026-10-15"}

def get_task(task_id):
    if data:
        return next((t for t in data["tasks"] if t["task_id"] == task_id), None)
    return {"task_id": "TSK-5002", "title": "Payment Gateway Integration - Sprint 2", "status": "Blocked", "blocker": "Waiting for client approval", "assigned_to_name": "Pooja Singh"}


emp_01 = get_emp("EMP001")
emp_02 = get_emp("EMP002")
emp_03 = get_emp("EMP003")
emp_10 = get_emp("EMP010")
cli_01 = get_client("CLI001")
cli_02 = get_client("CLI002")
inv_02 = get_invoice("INV-1002")
inv_03 = get_invoice("INV-1003")
task_01 = get_task("TSK-5001")
task_02 = get_task("TSK-5002")
task_03 = get_task("TSK-5003")

benchmark_questions = [
    
    {
        "id": 1,
        "category": "Direct Lookup",
        "language": "Hindi",
        "question": f"{cli_01['name']} का इनवॉयस {inv_02['invoice_id']} का बकाया (due amount) कितना है?",
        "expected_answer": f"{cli_01['name']} के इनवॉयस {inv_02['invoice_id']} का कुल बकाया ₹{inv_02['due_amount_inr']:,} है, जिसकी देय तारीख {inv_02['due_date']} है।"
    },
    {
        "id": 2,
        "category": "Direct Lookup",
        "language": "Hinglish",
        "question": f"{emp_01['name']} ka department aur designation kya hai?",
        "expected_answer": f"{emp_01['name']} {emp_01['department']} department mein {emp_01['role']} ke roop mein assigned hain."
    },
    {
        "id": 3,
        "category": "Direct Lookup",
        "language": "Hindi",
        "question": f"टास्क {task_01['task_id']} का स्टेटस क्या है और इसकी डेडलाइन कब है?",
        "expected_answer": f"टास्क {task_01['task_id']} ({task_01['title']}) का स्टेटस '{task_01['status']}' है और इसकी डेडलाइन {task_01['deadline']} है।"
    },
    {
        "id": 4,
        "category": "Direct Lookup",
        "language": "Hinglish",
        "question": f"{task_02['task_id']} kyun ruka (blocked) hua hai?",
        "expected_answer": f"Task {task_02['task_id']} '{task_02['title']}' blocked hai kyunki: '{task_02['blocker']}'."
    },
    {
        "id": 5,
        "category": "Direct Lookup",
        "language": "Hindi",
        "question": f"क्लाइंट {cli_02['name']} के मुख्य संपर्क व्यक्ति (contact person) कौन हैं?",
        "expected_answer": f"{cli_02['name']} के मुख्य संपर्क व्यक्ति {cli_02['contact_person']} हैं।"
    },
    {
        "id": 6,
        "category": "Direct Lookup",
        "language": "Hinglish",
        "question": f"Invoice {inv_03['invoice_id']} ka payment status kya hai?",
        "expected_answer": f"Invoice {inv_03['invoice_id']} ka status '{inv_03['status']}' hai. Iska kul amount ₹{inv_03['total_amount_inr']:,} hai aur due amount ₹{inv_03['due_amount_inr']:,} hai."
    },
    {
        "id": 7,
        "category": "Direct Lookup",
        "language": "Hindi",
        "question": f"{emp_03['name']} किस टास्क पर काम कर रहे हैं?",
        "expected_answer": f"{emp_03['name']} टास्क {task_03['task_id']} ({task_03['title']}) पर काम कर रहे हैं।"
    },
    {
        "id": 8,
        "category": "Direct Lookup",
        "language": "Hinglish",
        "question": f"{emp_02['name']} ka Telegram Chat ID kya hai?",
        "expected_answer": f"{emp_02['name']} ka Telegram Chat ID {emp_02['telegram_chat_id']} hai."
    },
    {
        "id": 9,
        "category": "Direct Lookup",
        "language": "Hindi",
        "question": f"टास्क {task_01['task_id']} का आखिरी अपडेट कब हुआ था?",
        "expected_answer": f"टास्क {task_01['task_id']} का आखिरी अपडेट {task_01['last_updated_at']} को दर्ज किया गया था।"
    },
    {
        "id": 10,
        "category": "Direct Lookup",
        "language": "Hinglish",
        "question": f"Employee {emp_10['emp_id']} ka naam aur role kya hai?",
        "expected_answer": f"Employee {emp_10['emp_id']} ka naam {emp_10['name']} hai aur wo {emp_10['department']} department mein {emp_10['role']} hain."
    },

    
    {
        "id": 11,
        "category": "Contextual Follow-up",
        "language": "Hindi",
        "turn_1_user": f"{emp_01['name']} कंपनी में क्या काम संभालते हैं?",
        "turn_1_assistant": f"{emp_01['name']} {emp_01['department']} विभाग में {emp_01['role']} हैं।",
        "question": "उनके जिम्मे कौन सा काम है और उसकी अंतिम तारीख कब है?",
        "expected_answer": f"{emp_01['name']} के जिम्मे '{task_01['title']}' (टास्क {task_01['task_id']}) है, और इसकी अंतिम तारीख {task_01['deadline']} है।"
    },
    {
        "id": 12,
        "category": "Contextual Follow-up",
        "language": "Hinglish",
        "turn_1_user": f"Invoice {inv_02['invoice_id']} kis client ka hai?",
        "turn_1_assistant": f"Invoice {inv_02['invoice_id']} client '{inv_02['client_name']}' ka hai.",
        "question": "Is invoice ka kitna payment receive ho chuka hai aur kitna baaki hai?",
        "expected_answer": f"Is invoice mein se ₹{inv_02['paid_amount_inr']:,} receive ho chuka hai aur ₹{inv_02['due_amount_inr']:,} abhi baaki (due) hai."
    },
    {
        "id": 13,
        "category": "Contextual Follow-up",
        "language": "Hindi",
        "turn_1_user": f"टास्क {task_02['task_id']} की स्थिति क्या है?",
        "turn_1_assistant": f"टास्क {task_02['task_id']} की स्थिति '{task_02['status']}' है।",
        "question": "इस काम के लिए कौन सा कर्मचारी जिम्मेदार है?",
        "expected_answer": f"इस काम के लिए जिम्मेदार कर्मचारी {task_02['assigned_to_name']} ({task_02['assigned_to_emp_id']}) हैं।"
    },
    {
        "id": 14,
        "category": "Contextual Follow-up",
        "language": "Hinglish",
        "turn_1_user": f"{cli_01['name']} ke contact person kaun hain?",
        "turn_1_assistant": f"{cli_01['name']} ke contact person {cli_01['contact_person']} hain.",
        "question": "Unka client ID kya hai?",
        "expected_answer": f"{cli_01['name']} ka client ID {cli_01['client_id']} hai."
    },
    {
        "id": 15,
        "category": "Contextual Follow-up",
        "language": "Hindi",
        "turn_1_user": f"क्या {emp_03['name']} ऑपरेशंस विभाग में हैं?",
        "turn_1_assistant": f"नहीं, {emp_03['name']} ऑपरेशंस में नहीं बल्कि {emp_03['department']} विभाग में {emp_03['role']} हैं।",
        "question": "तो उनका वर्तमान टास्क किस स्थिति में है?",
        "expected_answer": f"{emp_03['name']} का वर्तमान टास्क {task_03['task_id']} '{task_03['status']}' स्थिति में है।"
    },

  
    {
        "id": 16,
        "category": "Missing Information",
        "language": "Hindi",
        "question": f"{emp_01['name']} की मासिक सैलरी और बैंक अकाउंट नंबर क्या है?",
        "expected_answer": f"माफ़ कीजिए, डेटाबेस में {emp_01['name']} की सैलरी या बैंक विवरण से संबंधित कोई जानकारी उपलब्ध नहीं है।"
    },
    {
        "id": 17,
        "category": "Missing Information",
        "language": "Hinglish",
        "question": f"{cli_01['name']} ka registered head office address aur GST number kya hai?",
        "expected_answer": f"Record mein {cli_01['name']} ka physical address aur GST number uplabdh nahi hai. Kewal contact person aur invoice records uplabdh hain."
    },
    {
        "id": 18,
        "category": "Missing Information",
        "language": "Hindi",
        "question": "कर्मचारी 'समीर कपूर' (Sameer Kapoor) का कार्य विवरण और ईमेल आईडी बताएं।",
        "expected_answer": "कंपनी डेटाबेस में 'समीर कपूर' नाम का कोई कर्मचारी मौजूद नहीं है।"
    },
    {
        "id": 19,
        "category": "Missing Information",
        "language": "Hinglish",
        "question": "Office ka Wi-Fi password aur admin login credentials kya hain?",
        "expected_answer": "Kshama karein, main yeh jankari provide nahi kar sakta. Internal credentials ya Wi-Fi password hamare business data mein maujood nahi hain."
    },
    {
        "id": 20,
        "category": "Missing Information",
        "language": "Hindi",
        "question": "अगले साल 2027 के लिए कंपनी का अनुमानित रेवेन्यू बजट कितना है?",
        "expected_answer": "माफ़ कीजिए, रिकॉर्ड में केवल वर्तमान इनवॉयस और टास्क का डेटा है। भविष्य के 2027 बजट का कोई डेटा उपलब्ध नहीं है।"
    },

   
    {
        "id": 21,
        "category": "Multi-Hop / Aggregation",
        "language": "Hindi",
        "question": "वर्तमान में कौन-कौन से काम ब्लॉक (Blocked) हैं और उनके ब्लॉकर का मुख्य कारण क्या है?",
        "expected_answer": f"ब्लॉक किए गए मुख्य कार्यों में टास्क {task_02['task_id']} ({task_02['title']}) शामिल है, जिसके ब्लॉकर का कारण '{task_02['blocker']}' है।"
    },
    {
        "id": 22,
        "category": "Multi-Hop / Aggregation",
        "language": "Hinglish",
        "question": f"Total kitne invoices overdue status mein hain aur kya invoice {inv_03['invoice_id']} overdue list mein hai?",
        "expected_answer": f"Dataset mein invoices overdue status mein hain, aur ji haan, invoice {inv_03['invoice_id']} overdue hai jiska due amount ₹{inv_03['due_amount_inr']:,} hai."
    },
    {
        "id": 23,
        "category": "Multi-Hop / Aggregation",
        "language": "Hindi",
        "question": "इंजीनियरिंग डिपार्टमेंट में कुल कौन-कौन से प्रमुख कर्मचारी हैं?",
        "expected_answer": f"इंजीनियरिंग डिपार्टमेंट के प्रमुख कर्मचारियों में {emp_01['name']} ({emp_01['role']}) और {emp_03['name']} ({emp_03['role']}) शामिल हैं।"
    },
    {
        "id": 24,
        "category": "Multi-Hop / Aggregation",
        "language": "Hinglish",
        "question": f"Invoice {inv_02['invoice_id']} ka total amount aur paid amount mila kar verify karein ki balance match karta hai ya nahi.",
        "expected_answer": f"Invoice {inv_02['invoice_id']}: Paid amount (₹{inv_02['paid_amount_inr']:,}) + Due amount (₹{inv_02['due_amount_inr']:,}) = Total ₹{inv_02['total_amount_inr']:,} hai. Hisaab bilkul sahi aur match hai."
    },
    {
        "id": 25,
        "category": "Multi-Hop / Aggregation",
        "language": "Hindi",
        "question": f"क्या {emp_02['name']} के पास कोई ऐसा टास्क है जो इस समय रुका (Blocked) हुआ है?",
        "expected_answer": f"जी हाँ, {emp_02['name']} का टास्क {task_02['task_id']} ({task_02['title']}) वर्तमान में '{task_02['status']}' स्थिति में है। कारण: '{task_02['blocker']}'।"
    }
]

output_file = "benchmark_qa.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(benchmark_questions, f, indent=2, ensure_ascii=False)

print(f" Successfully generated {len(benchmark_questions)} benchmark questions into '{output_file}'!")