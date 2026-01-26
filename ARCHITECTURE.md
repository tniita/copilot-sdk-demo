# GitHub Copilot SDK Demo - MCP Protocol Flow

## Communication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI Assistant (Client)                       │
│              (GitHub Copilot, Claude, ChatGPT, etc.)            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ JSON-RPC 2.0 over stdio
                            │
        ┌───────────────────▼───────────────────┐
        │      1. initialize                     │
        │   ┌─────────────────────────────────┐ │
        │   │ Client sends capabilities       │ │
        │   │ Server responds with protocol   │ │
        │   └─────────────────────────────────┘ │
        └───────────────────┬───────────────────┘
                            │
        ┌───────────────────▼───────────────────┐
        │      2. tools/list                     │
        │   ┌─────────────────────────────────┐ │
        │   │ Client requests tool list       │ │
        │   │ Server returns available tools  │ │
        │   └─────────────────────────────────┘ │
        └───────────────────┬───────────────────┘
                            │
        ┌───────────────────▼───────────────────┐
        │      3. tools/call                     │
        │   ┌─────────────────────────────────┐ │
        │   │ Client calls tool with args     │ │
        │   │ Server executes and returns     │ │
        │   └─────────────────────────────────┘ │
        └───────────────────┬───────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                     MCP Server                                 │
│                   (mcp_server.py)                              │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              Request Handler                          │    │
│  │  • Parses JSON-RPC requests                          │    │
│  │  • Routes to appropriate method                      │    │
│  │  • Returns JSON-RPC responses                        │    │
│  └──────────────────────────────────────────────────────┘    │
│                          │                                     │
│  ┌───────────────────────┼───────────────────────────────┐   │
│  │                       │                               │   │
│  │  ┌──────────────┐    │    ┌────────────────────┐    │   │
│  │  │ initialize   │    │    │   tools/list       │    │   │
│  │  │  handler     │    │    │     handler        │    │   │
│  │  └──────────────┘    │    └────────────────────┘    │   │
│  │                       │                               │   │
│  │                       ▼                               │   │
│  │                ┌────────────┐                         │   │
│  │                │ tools/call │                         │   │
│  │                │  handler   │                         │   │
│  │                └──────┬─────┘                         │   │
│  └───────────────────────┼───────────────────────────────┘   │
│                          │                                     │
│  ┌───────────────────────▼───────────────────────────────┐   │
│  │                    Tool Registry                       │   │
│  │  ┌────────────────────────────────────────────────┐   │   │
│  │  │  get_weather(city: str) -> WeatherData        │   │   │
│  │  │  • Simulates weather API                       │   │   │
│  │  │  • Returns temperature and conditions          │   │   │
│  │  └────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │  [Add more tools here]                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

## Request/Response Examples

### 1. Initialize

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "my-client",
      "version": "1.0.0"
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "github-copilot-demo-server",
      "version": "1.0.0"
    }
  }
}
```

### 2. List Tools

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "inputSchema": {
          "type": "object",
          "properties": {
            "city": {
              "type": "string",
              "description": "The name of the city to get weather for"
            }
          },
          "required": ["city"]
        }
      }
    ]
  }
}
```

### 3. Call Tool

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": "Paris"
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
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

## Key Features

### Standards-Based
- ✅ JSON-RPC 2.0 protocol
- ✅ MCP specification 2024-11-05
- ✅ Stdio transport (stdin/stdout)

### Asynchronous
- ✅ Full async/await support
- ✅ Non-blocking I/O
- ✅ Efficient stream handling

### Extensible
- ✅ Easy to add new tools
- ✅ Type-safe with input schemas
- ✅ Clean separation of concerns

### Production Ready
- ✅ Error handling
- ✅ Security scanned
- ✅ Well tested
- ✅ Zero dependencies
