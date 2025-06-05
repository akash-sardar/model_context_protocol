from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
import asyncio
from mcp_use import MCPAgent, MCPClient
import os

async def chat_with_memory_using_mcp():
    """Chat service using MCPAgent's built-in conversation memory"""
    # Load environment for API keys
    load_dotenv()
    os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

    # MCP Server Config
    config_file  = "C:\\Akash\\Project Work\\AI\\Projects\\model_context_protocol_demo\\mcp_servers_config.json"

    print("Initializing chat using Claude..")

    # Create MCP Client and agent with memory enabled
    client = MCPClient.from_config_file(config_file)
    llm = ChatAnthropic(model = "claude-opus-4-20250514")

    # Create agent with memory enabled = True
    agent = MCPAgent(
        llm = llm,
        client = client,
        max_steps=15,
        memory_enabled= True, # Enable built-in conversation memory
    )

    print("\n==== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end conversation")
    print("Type 'clear' to clear conversation history")
    print("=================================\n")

    try:
        # main chat loop
        while True:
            # get user input
            user_input = input("\nYou: ")

            # check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            # Check for clear history command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared")
                continue

            # Get response from agent
            print("\nAssistant: ", end = "", flush = True)

            try:
                # Run thr agent with user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)
            
            except Exception as e:
                print(f"\nError: {e}")
    except Exception as e:
            print(f"\nError: {e}")
        
    finally:
        # Clean up resources
        if client and client.sessions:
            await client.close_all_sessions()




# def main():
#     print("Hello from custom-mcp-project!")


if __name__ == "__main__":
    asyncio.run(chat_with_memory_using_mcp())
