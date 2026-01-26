# GitHub Copilot SDK Demo with MCP Protocol

This repository demonstrates how to build a GitHub Copilot SDK integration using the Model Context Protocol (MCP). The implementation provides a weather tool that can be accessed by AI assistants through the standard MCP interface.

## Overview

The demo includes:
- **MCP Server** (`mcp_server.py`): Implements the Model Context Protocol with a weather tool
- **MCP Client** (`mcp_client.py`): Example client for testing the MCP server
- **Copilot SDK + MCP Integration** (`gh.py`): GitHub Copilot SDK that loads tools dynamically from MCP server

## Model Context Protocol (MCP)

MCP is a standardized protocol for connecting AI assistants to different data sources and tools. This implementation follows the MCP specification and provides:

- JSON-RPC 2.0 communication over stdio transport
- Standard MCP methods: `initialize`, `tools/list`, `tools/call`
- Weather tool with dynamic city-based queries

### Key Features of the Integration

The `gh.py` implementation provides a **bridge** between GitHub Copilot SDK and MCP servers:

1. **Dynamic Tool Loading**: Automatically discovers and loads tools from any MCP server
2. **Schema Translation**: Converts MCP tool schemas to Copilot SDK tool definitions
3. **Bidirectional Communication**: Translates between Copilot SDK calls and MCP protocol
4. **Type Safety**: Uses Pydantic models for parameter validation
5. **Extensibility**: Works with any MCP-compliant server without code changes

## Setup

### Prerequisites

1. **Python 3.8+** - Required for async support
2. **GitHub Copilot SDK** - Required for `gh.py` integration (optional for standalone MCP)

### Installation

```bash
# Clone the repository
git clone https://github.com/tniita/copilot-sdk-demo.git
cd copilot-sdk-demo

# Optional: Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Copilot SDK (required for gh.py)
pip install github-copilot-sdk

# Or install from requirements.txt
pip install -r requirements.txt
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

### Using with GitHub Copilot SDK

Run the integrated Copilot assistant that loads tools from the MCP server:

```bash
python3 gh.py
```

This will:
1. Start the MCP server automatically
2. Load all available tools from the MCP server
3. Create a Copilot session with those tools
4. Allow you to interact with the assistant

Expected output:
```
🚀 Starting GitHub Copilot with MCP Protocol Integration

✓ Loaded 1 tool(s) from MCP server
🌤️  Weather Assistant with MCP (type 'exit' to quit)
   Try: 'What's the weather in Paris?' or 'Compare weather in NYC and LA'

You: What's the weather in Paris?
Assistant: Let me check the weather for you...
```

### Standalone MCP Server

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

### Copilot SDK + MCP Integration

```
┌─────────────────────┐
│  GitHub Copilot SDK │
│    (gh.py)          │
├─────────────────────┤
│  ┌───────────────┐  │
│  │ MCPToolBridge │  │  ← Dynamically loads tools from MCP
│  └───────┬───────┘  │
└──────────┼──────────┘
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
  │  │get_weather│  │
  │  └───────────┘  │
  └─────────────────┘
```

### Standalone MCP Server

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

- `gh.py`: **GitHub Copilot SDK with MCP integration** - Dynamically loads tools from MCP server
- `mcp_server.py`: **MCP server implementation** - Provides tools via MCP protocol
- `mcp_client.py`: **Test client** for the MCP server
- `mcp_config.json`: Example MCP configuration for external clients
- `requirements.txt`: Python dependencies

## License

See LICENSE file for details.