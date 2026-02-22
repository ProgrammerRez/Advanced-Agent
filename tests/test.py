from search_agent import create_graph_agent, main as run_research_agent
from langchain_groq import ChatGroq
import asyncio

# =========================
# SETUP
# =========================

# Initialize LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

# Initialize research agent
research_agent = create_graph_agent()

# Store the artifact
artifact: str | None = None

# =========================
# CHAT FUNCTION (minimal)
# =========================

def chat_about_report(user_question: str, artti) -> str:
    """Ask the LLM a question with the artifact attached as context."""
    

    if artifact is None:
        return "No research artifact is available yet. Please run a research query first."

    # Combine the artifact with the question
    prompt = f"Research Artifact:\n{artifact}\n\nQuestion:\n{user_question}"

    response = llm.invoke(prompt)
    return response.content

# =========================
# CONSOLE INTERFACE
# =========================

def run_console_chat():
    global artifact

    while True:
        print("\nOptions:")
        print("1. Run new research")
        print("2. Ask question about artifact")
        print("3. Exit")

        choice = input("Enter choice (1/2/3): ").strip()
        if choice not in {"1", "2", "3"}:
            print("Invalid choice. Try again.")
            continue

        if choice == "1":
            topic = input("Enter research topic: ").strip()
            mode_input = input("Enter mode (shallow/deep): ").strip().lower()
            if mode_input not in ("shallow", "deep"):
                print("Invalid mode! Using 'shallow'.")
                mode_input = "shallow"

            print(f"\nRunning research agent on '{topic}' in {mode_input} mode...")
            try:
                artifact_result = asyncio.run(run_research_agent(query=topic, mode=mode_input))
            except Exception as e:
                print(f"Error running research agent: {e}")
                continue

            artifact = artifact_result.final_report
            print("Research completed and artifact stored.")

        elif choice == "2":
            if artifact is None:
                print("No artifact available. Run research first.")
                continue
            user_question = input("Enter your question: ").strip()
            answer = chat_about_report(user_question)
            print(f"\nAnswer:\n{answer}")

        elif choice == "3":
            print("Exiting...")
            break

# =========================
# RUN CONSOLE CHAT
# =========================

if __name__ == "__main__":
    try:
        run_console_chat()
    except KeyboardInterrupt:
        print("\nExiting...")
