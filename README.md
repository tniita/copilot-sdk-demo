# GitHub Copilot SDK Demo with MCP Protocol

This repository demonstrates how to build a GitHub Copilot SDK integration using the Model Context Protocol (MCP). The implementation provides a weather tool that can be accessed by AI assistants through the standard MCP interface.

## Overview

The demo includes:
- **MCP Server** (`mcp_server.py`): Implements the Model Context Protocol with a weather tool
- **MCP Client** (`mcp_client.py`): Example client for testing the MCP server
- **Legacy Demo** (`gh.py`): Original Copilot SDK implementation (for reference)

## Model Context Protocol (MCP)

MCP is a standardized protocol for connecting AI assistants to different data sources and tools. This implementation follows the MCP specification and provides:

- JSON-RPC 2.0 communication over stdio transport
- Standard MCP methods: `initialize`, `tools/list`, `tools/call`
- Weather tool with dynamic city-based queries

## Setup

No external dependencies required! The implementation uses only Python standard library.

```bash
# Clone the repository
git clone https://github.com/tniita/copilot-sdk-demo.git
cd copilot-sdk-demo

# Optional: Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Usage

### Running the MCP Server

The MCP server communicates via stdin/stdout using JSON-RPC 2.0:

```bash
python3 mcp_server.py
```

The server will start and listen for MCP requests on stdin.

### Testing with the MCP Client

Run the test client to see the server in action:

```bash
python3 mcp_client.py
```

Expected output:
```
🌤️  MCP Weather Demo Client

Initializing MCP session...
✓ Server: github-copilot-demo-server v1.0.0
✓ Protocol: 2024-11-05

Listing available tools...
✓ Found 1 tool(s):
  - get_weather: Get the current weather for a city

Testing weather tool with various cities:

🌍 Calling get_weather for Paris...
   Temperature: 67°F
   Condition: sunny

...
```

### Using with GitHub Copilot

To use this MCP server with GitHub Copilot or other MCP-compatible clients:

1. Configure your MCP client with the server command:
   ```json
   {
     "mcpServers": {
       "github-copilot-demo": {
         "command": "python3",
         "args": ["path/to/mcp_server.py"]
       }
     }
   }
   ```

2. The server will be automatically started by the client when needed.

3. Available tools:
   - `get_weather`: Get current weather for any city

## MCP Protocol Implementation

### Request Format

All requests follow JSON-RPC 2.0 format:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": "Paris"
    }
  }
}
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"city\": \"Paris\", \"temperature\": \"67°F\", \"condition\": \"sunny\"}"
      }
    ]
  }
}
```

## Architecture

```
┌─────────────────┐
│   AI Assistant  │
│  (Copilot/LLM)  │
└────────┬────────┘
         │ MCP Protocol
         │ (JSON-RPC 2.0)
         │
┌────────▼────────┐
│   MCP Server    │
│  (mcp_server.py)│
├─────────────────┤
│  ┌───────────┐  │
│  │   Tools   │  │
│  ├───────────┤  │
│  │ get_weather│ │
│  └───────────┘  │
└─────────────────┘
```

## Extending the Demo

To add more tools to the MCP server:

1. Define the tool in `_register_tools()`:
```python
self.tools.append(Tool(
    name="your_tool",
    description="Description of your tool",
    input_schema={
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"]
    }
))
```

2. Implement the tool handler in `handle_tools_call()`:
```python
if tool_name == "your_tool":
    return await self._your_tool(arguments)
```

3. Add the tool implementation:
```python
async def _your_tool(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
    # Your implementation here
    return {
        "content": [
            {"type": "text", "text": "Result"}
        ]
    }
```

## Files

- `mcp_server.py`: MCP server implementation
- `mcp_client.py`: Test client for the MCP server
- `mcp_config.json`: Example MCP configuration
- `gh.py`: Original Copilot SDK demo (legacy)
- `requirements.txt`: Python dependencies (none required for MCP)

## License

See LICENSE file for details.