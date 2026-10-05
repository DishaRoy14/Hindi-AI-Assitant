import json
import random
from datetime import datetime, timedelta

random.seed(42)

first_names = [
    "Rahul", "Pooja", "Amit", "Neha", "Vikram", "Sneha", "Karan", "Ananya", "Rohan", "Priya",
    "Manish", "Kavita", "Siddharth", "Ritu", "Deepak", "Swati", "Arjun", "Divya", "Gaurav", "Megha",
    "Sanjay", "Anjali", "Varun", "Sunita", "Rajesh", "Tanvi", "Naveen", "Shreya", "Aditya", "Preeti",
    "Abhishek", "Aparna", "Harish", "Isha", "Manoj", "Kiran", "Sachin", "Bhavna", "Alok", "Rashmi"
]
last_names = [
    "Sharma", "Verma", "Patel", "Singh", "Gupta", "Mehta", "Kumar", "Iyer", "Nair", "Reddy",
    "Chopra", "Joshi", "Bose", "Dutta", "Mukherjee", "Malhotra", "Kapoor", "Chatterjee", "Mishra", "Pandey"
]
departments = [
    ("Engineering", "Software Engineer"),
    ("Engineering", "DevOps Engineer"),
    ("Engineering", "Backend Developer"),
    ("Design", "UI/UX Designer"),
    ("Design", "Product Designer"),
    ("Accounts", "Finance Executive"),
    ("Accounts", "Senior Accountant"),
    ("Sales", "Account Manager"),
    ("Sales", "Business Development Executive"),
    ("Operations", "Operations Lead")
]

employees = []
for i in range(1, 101):
    emp_id = f"EMP{i:03d}"
    fname = first_names[(i - 1) % len(first_names)]
    lname = last_names[((i - 1) * 3) % len(last_names)]
    dept, role = departments[(i - 1) % len(departments)]
    employees.append({
        "emp_id": emp_id,
        "name": f"{fname} {lname}",
        "department": dept,
        "role": role,
        "telegram_chat_id": f"tg_chat_{90000 + i}"
    })


client_prefixes = [
    "Apex", "Zenith", "Bharat", "BlueWave", "Nexus", "GreenEarth", "Vedic", "Nova",
    "Urban", "Metro", "Kavya", "Trident", "Sunrise", "Delta", "Prime", "Summit",
    "Horizon", "Pioneer", "Quantum", "Omega", "Imperial", "Vanguard", "Starlight", "Econ", "Falcon"
]
client_suffixes = ["Tech Solutions", "Enterprises", "Logistics", "Media Works", "FinTech", "Retail", "Systems", "Infotech"]

clients = []
for i in range(1, 101):
    client_id = f"CLI{i:03d}"
    prefix = client_prefixes[(i - 1) % len(client_prefixes)]
    suffix = client_suffixes[(i - 1) % len(client_suffixes)]
    c_name = f"{prefix} {suffix} Pvt Ltd" if i <= 50 else f"{prefix} Group - Unit {i-50}"
    contact = f"{first_names[(i * 2) % len(first_names)]} {last_names[(i * 2) % len(last_names)]}"
    clients.append({
        "client_id": client_id,
        "name": c_name,
        "contact_person": contact
    })


invoices = []
statuses = ["Paid", "Pending", "Overdue"]
base_date = datetime(2026, 10, 1)

for i in range(1, 101):
    inv_id = f"INV-{1000 + i}"
    client = clients[i - 1]  
    
    total = random.choice([25000, 35000, 50000, 75000, 100000, 125000, 150000, 200000, 350000])
    status = statuses[i % 3]  
    
    if status == "Paid":
        paid = total
        due = 0
        due_date = (base_date - timedelta(days=random.randint(5, 30))).strftime("%Y-%m-%d")
    elif status == "Overdue":
        paid = random.choice([0, int(total * 0.25), int(total * 0.5)])
        due = total - paid
        due_date = (base_date - timedelta(days=random.randint(2, 25))).strftime("%Y-%m-%d")
    else:  # Pending
        paid = random.choice([0, int(total * 0.3), int(total * 0.5)])
        due = total - paid
        due_date = (base_date + timedelta(days=random.randint(4, 28))).strftime("%Y-%m-%d")
        
    invoices.append({
        "invoice_id": inv_id,
        "client_id": client["client_id"],
        "client_name": client["name"],
        "total_amount_inr": total,
        "paid_amount_inr": paid,
        "due_amount_inr": due,
        "due_date": due_date,
        "status": status
    })


task_domains = [
    "Q2 Financial Audit", "Payment Gateway Integration", "Mobile App UI Redesign",
    "PostgreSQL Migration", "Vendor Onboarding Review", "Security Compliance Check",
    "Customer Support Automation", "Marketing Funnel Optimization", "Server Backup Pipeline",
    "Employee Payroll Settlement", "Cloud Cost Optimization", "API Rate Limiter Implementation"
]

blockers_pool = [
    "Waiting for client approval",
    "Bank statements pending verification",
    "Third-party API credentials delayed",
    "Server access permissions pending",
    "Vendor SLA documentation missing"
]

tasks = []
task_statuses = ["In Progress", "Blocked", "Completed"]

for i in range(1, 101):
    task_id = f"TSK-{5000 + i}"
    assigned_emp = employees[i - 1]  
    t_status = task_statuses[i % 3]
    blocker = blockers_pool[(i - 1) % len(blockers_pool)] if t_status == "Blocked" else None
    
    deadline = (base_date + timedelta(days=((i % 25) - 5))).strftime("%Y-%m-%d")
    last_update = (base_date - timedelta(hours=random.randint(2, 72))).strftime("%Y-%m-%d %H:%M")

    domain = task_domains[(i - 1) % len(task_domains)]
    tasks.append({
        "task_id": task_id,
        "title": f"{domain} - Sprint {((i - 1) % 4) + 1}",
        "assigned_to_emp_id": assigned_emp["emp_id"],
        "assigned_to_name": assigned_emp["name"],
        "department": assigned_emp["department"],
        "deadline": deadline,
        "status": t_status,
        "blocker": blocker,
        "last_updated_at": last_update
    })


dataset = {
    "metadata": {
        "generated_at": datetime.now().isoformat(),
        "counts": {
            "employees": len(employees),
            "clients": len(clients),
            "invoices": len(invoices),
            "tasks": len(tasks)
        }
    },
    "employees": employees,
    "clients": clients,
    "invoices": invoices,
    "tasks": tasks
}

for inv in dataset["invoices"]:
    assert inv["paid_amount_inr"] + inv["due_amount_inr"] == inv["total_amount_inr"], (
        f"Arithmetic discrepancy in invoice {inv['invoice_id']}"
    )

with open("company_data_full.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print("Verification Succeeded:")
print(f"• Employees: {len(employees)}")
print(f"• Clients:   {len(clients)}")
print(f"• Invoices:  {len(invoices)}")
print(f"• Tasks:     {len(tasks)}")
print("• Output saved to 'company_data_full.json'")