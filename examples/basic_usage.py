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

    # Example: generate a prompt
    user_request = "帮我写一个用于代码审查的 AI 提示词，要求输出结构化审查意见，包含问题等级和修复建议"

    print(f"Input: {user_request}")
    print("\n" + "=" * 60 + "\n")

    result = agent.run(user_request)
    print(result)


if __name__ == "__main__":
    main()
