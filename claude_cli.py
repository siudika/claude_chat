import os
import sys
import json
from pathlib import Path
from datetime import datetime

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed")
    print("Install it with: pip install anthropic")
    sys.exit(1)

class ClaudeCLI:
    def __init__(self):
        # Initialize API client
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: ANTHROPIC_API_KEY environment variable not set")
            print("Set it with: export ANTHROPIC_API_KEY='your-api-key' (Linux/macOS) or")
            print("setx ANTHROPIC_API_KEY \"your-api-key\" (Windows PowerShell)")
            sys.exit(1)
        self.client = Anthropic(api_key=api_key)

        # Configuration
        # NOTE: Update model based on your account's available models
        self.model = "claude-3-sonnet-20240229"
        self.max_tokens = 4096
        self.temperature = 1.0

        # Conversation state
        self.conversation_history = []
        self.thread_name = None
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        # System prompt for assistant behavior
        self.system_prompt = "You are a helpful AI assistant. Provide clear, concise, and accurate responses."

    def save_thread(self):
        if not self.thread_name:
            return
        file_path = self.data_dir / f"{self.thread_name}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.conversation_history, f, indent=2)
        print(f"Conversation saved to {file_path}")

    def load_thread(self, thread_name):
        file_path = self.data_dir / f"{thread_name}.json"
        if not file_path.exists():
            print(f"No saved thread found for '{thread_name}'. Starting a new one.")
            self.conversation_history = []
            return
        with open(file_path, "r", encoding="utf-8") as f:
            self.conversation_history = json.load(f)
        print(f"Loaded conversation from {file_path}")

    def list_threads(self):
        # List all saved threads
        files = list(self.data_dir.glob("*.json"))
        threads = [f.stem for f in files]
        if not threads:
            print("No saved threads found.")
            return []
        print("Your chat threads:")
        for idx, name in enumerate(threads, start=1):
            print(f"  {idx}. {name}")
        return threads

    def prompt_thread_choice(self):
        threads = self.list_threads()
        choice = input("\nEnter thread number to continue, or new thread name to start: ").strip()
        if choice.isdigit() and threads:
            idx = int(choice) - 1
            if 0 <= idx < len(threads):
                self.thread_name = threads[idx]
                self.load_thread(self.thread_name)
                return
            else:
                print("Invalid choice number.")
        # Assume new thread name
        if choice == "":
            choice = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            print(f"Starting a new thread: {choice}")
        else:
            print(f"Starting a new thread: {choice}")
        self.thread_name = choice
        self.conversation_history = []

    def send_message(self, user_message: str) -> str:
        # Compose the full message array with system prompt + history + new message
        messages = [{"role": "system", "content": self.system_prompt}]

        # Include conversation history
        for msg in self.conversation_history:
            messages.append(msg)

        # Append current user message
        messages.append({"role": "user", "content": user_message})

        # Call Claude API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages
        )

        answer = response.content[0].text

        # Append the new messages to conversation history and save
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": answer})

        self.save_thread()

        return answer

def main():
    cli = ClaudeCLI()
    cli.prompt_thread_choice()
    print(f"\nThread '{cli.thread_name}' is active. Type your questions below.")
    print("Type 'exit' or 'quit' to exit, 'list' to show threads, or 'switch' to change thread.\n")

    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            elif user_input.lower() == "list":
                cli.list_threads()
            elif user_input.lower() == "switch":
                cli.prompt_thread_choice()
                print(f"Switched to thread '{cli.thread_name}'.")
            elif user_input == "":
                continue
            else:
                response = cli.send_message(user_input)
                print(f"\nClaude: {response}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError during API call: {e}")
            print("Try again or switch threads.\n")

if __name__ == "__main__":
    main()
