import json
import os
from ai_agent_query_engine import CompanyAIAssistant

def normalize(text):
    if not text:
        return ""
    return text.replace("。", "।").strip()

def evaluate():
    benchmark_file = "benchmark_qa.json"
    if not os.path.exists(benchmark_file):
        raise FileNotFoundError(f"File '{benchmark_file}' not found.")

    with open(benchmark_file, "r", encoding="utf-8") as f:
        benchmarks = json.load(f)

    # Initialize ChromaDB-backed assistant
    assistant = CompanyAIAssistant(persist_dir="./chroma_db")
    passed = 0
    results = []

    print("=" * 70)
    print(f"EVALUATING {len(benchmarks)} BENCHMARK QUESTIONS (VECTOR DB ENGINE)")
    print("=" * 70)

    for item in benchmarks:
        q_id = item["id"]
        category = item["category"]
        lang = item["language"]
        question = item["question"]
        expected = item["expected_answer"]

        turn_1_user = item.get("turn_1_user")
        turn_1_assistant = item.get("turn_1_assistant")

        predicted = assistant.answer_query(
            question=question,
            turn_1_user=turn_1_user,
            turn_1_assistant=turn_1_assistant
        )

        is_match = normalize(predicted) == normalize(expected)
        if is_match:
            passed += 1

        results.append({
            "id": q_id,
            "category": category,
            "language": lang,
            "question": question,
            "expected": expected,
            "predicted": predicted,
            "passed": is_match
        })

        status = "MATCH" if is_match else "MISMATCH"
        print(f"[{status}] Q{q_id:02d} [{category}] ({lang})")
        if not is_match:
            print(f"   Expected:  {expected}")
            print(f"   Predicted: {predicted}")

    acc = (passed / len(benchmarks)) * 100
    print("=" * 70)
    print(f"RESULT: {passed}/{len(benchmarks)} questions matched ({acc:.1f}% accuracy)")
    print("=" * 70)

    with open("evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump({"accuracy": acc, "passed": passed, "total": len(benchmarks), "results": results}, f, indent=2, ensure_ascii=False)
    print("• Evaluation details saved to 'evaluation_report.json'.")

if __name__ == "__main__":
    evaluate()