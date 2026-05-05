"""
Basic usage example for the agents library.

Set your API key before running:
    export ANTHROPIC_API_KEY="sk-ant-..."
"""

from agents import PromptEngineer


def main():
    agent = PromptEngineer()

    print(f"Agent: {agent.name}")
    print(f"Description: {agent.description}")
    print(f"Model: {agent.config.model}")
    print(f"Temperature: {agent.config.temperature}")
    print()

    # Example: generate a prompt for code review
    user_request = "Write an AI prompt for code review that outputs structured feedback with severity levels and fix suggestions"

    print(f"Input: {user_request}")
    print("\n" + "=" * 60 + "\n")

    result = agent.run(user_request)
    print(result)


if __name__ == "__main__":
    main()
