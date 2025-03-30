
This tool generates Model Context Protocol (MCP) servers from OpenAPI specifications. It parses OpenAPI YAML/JSON files and creates a FastAPI server that provides model validation and context endpoints.


## Directory Structure

```
mcp-generator/
├── generator.py              # Main generator script
├── templates/                # Jinja2 templates
│   └── mcp_server.py.j2      # MCP server template
├── examples/                 # Example OpenAPI specifications
│   └── openweather.yaml      # OpenWeather API specification
├── test_mcp_with_claude.py   # Testing script using Claude
└── README.md                 # This file
```



## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/mcp-generator.git
   cd mcp-generator
   ```

2. (optional) Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn pydantic httpx pyyaml jinja2 anthropic requests
   ```



## Usage

### Adding OpenAPI Specifications

Place your OpenAPI specification YAML or JSON files in the `examples/` directory:
`cp path/to/your/api-spec.yaml examples/`


### Generating an MCP Server
To generate an MCP server from an OpenAPI specification:
`python generator.py examples/your-api-spec.yaml`


This will create a file named `mcp_server_your-api-spec.py` based on the API name.
You can also specify a custom output filename:
`python generator.py examples/your-api-spec.yaml custom_server_name.py`



### Running the Generated Server

To run the generated MCP server:
`python mcp_server_your-api-spec.py`


The server will start on http://localhost:8000

### Configuring the Server

Configure the server with your API key and base URL:
curl -X POST http://localhost:8000/config \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "base_url": "https://api.example.com"
  }'


The base url could look like this:
"base_url": "https://petstore.swagger.io/v2"

or

"base_url": "https://api.openweathermap.org/data/2.5"



### Testing the Server

#### Using the Claude Testing Script

1. Set your Clause API key:
   ```bash
   export CLAUDE_API_KEY=your_anthropic_api_key
   ```

   Or set it in the .env  file


2. Run the testing script:
   ```bash
   python test_mcp_with_claude.py
   ```
