import anthropic
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY", "")  # Get API key from .env file
MCP_SERVER_URL = "http://localhost:8000"

# Initialize Claude client
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def configure_mcp_server():
    """Configure the MCP server """
    response = requests.post(
        f"{MCP_SERVER_URL}/config",
        json={
            "base_url": "https://api.openweathermap.org/data/2.5"
        }
    )
    return response.json()

def get_mcp_context():
    """Get the context (available models) from the MCP server."""
    response = requests.get(f"{MCP_SERVER_URL}/context")
    return response.json()

def validate_with_claude(model_name, context_data):
    """Use Claude to generate test data for a specific model and validate it."""
    # Extract model fields from context
    model_fields = context_data["models"][model_name]["fields"]
    
    # Create a prompt for Claude to generate test data
    prompt = f"""
    I need you to create a valid JSON object for the "{model_name}" model with the following fields:
    
    {json.dumps(model_fields, indent=2)}
    
    Please generate realistic sample data that matches these field types. 
    Return ONLY the JSON object without any explanation or markdown formatting.
    """
    
    # Get Claude's response
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",  # This is the issue - using outdated model name
        max_tokens=1000,
        temperature=0.2,
        system="You are a helpful assistant that generates valid test data in JSON format.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the JSON data from Claude's response
    claude_data = message.content[0].text.strip()
    
    # Parse the JSON data
    try:
        test_data = json.loads(claude_data)
        print(f"\n✅ Claude generated valid JSON for {model_name}:")
        print(json.dumps(test_data, indent=2))
    except json.JSONDecodeError as e:
        print(f"\n❌ Claude generated invalid JSON for {model_name}:")
        print(claude_data)
        print(f"Error: {e}")
        return {"error": "Invalid JSON from Claude"}
    
    # Validate the data with the MCP server
    validation_response = requests.post(
        f"{MCP_SERVER_URL}/validate",
        json={
            "model_name": model_name,
            "data": test_data
        }
    )
    
    return validation_response.json()

def main():
    # Step 1: Configure the MCP server
    print("Configuring MCP server...")
    config_result = configure_mcp_server()
    print(f"Configuration result: {config_result}")
    
    # Step 2: Get the context from the MCP server
    print("\nGetting context from MCP server...")
    context_data = get_mcp_context()
    available_models = list(context_data["models"].keys())
    print(f"Available models: {', '.join(available_models)}")
    
    # Step 3: Test each model with Claude
    for model_name in available_models:
        print(f"\n{'=' * 50}")
        print(f"Testing model: {model_name}")
        print(f"{'=' * 50}")
        
        validation_result = validate_with_claude(model_name, context_data)
        
        print(f"\nValidation result for {model_name}:")
        print(json.dumps(validation_result, indent=2))

if __name__ == "__main__":
    main()
