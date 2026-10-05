import os
from ai_agent_query_engine import CompanyAIAssistant

def start_interactive_session():
    persist_dir = "./chroma_db"
    assistant = CompanyAIAssistant(persist_dir=persist_dir)
    
    print("=" * 65)
    print("Operations AI Assistant (VectorDB Powered - Hindi & Hinglish)")
    print("Type your questions below. Enter 'exit' or 'quit' to stop.")
    print("=" * 65)

    turn_1_user = None
    turn_1_assistant = None

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            response = assistant.answer_query(
                question=user_input,
                turn_1_user=turn_1_user,
                turn_1_assistant=turn_1_assistant
            )
            print(f"AI:  {response}")

            turn_1_user = user_input
            turn_1_assistant = response
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break

if __name__ == "__main__":
    start_interactive_session()