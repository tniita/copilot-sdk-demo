#!/usr/bin/env python3
"""
GitHub Copilot SDK with MCP Protocol Integration

This implementation integrates the Model Context Protocol (MCP) with GitHub Copilot SDK,
allowing tools to be loaded dynamically from an MCP server and used by the Copilot assistant.
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

try:
    from copilot import CopilotClient
    from copilot.tools import define_tool
    from copilot.generated.session_events import SessionEventType
    COPILOT_AVAILABLE = True
except ImportError:
    COPILOT_AVAILABLE = False
    print("⚠️  GitHub Copilot SDK not installed. Run: pip install github-copilot-sdk", file=sys.stderr)


class MCPToolBridge:
    """Bridge between MCP server and Copilot SDK tools"""
    
    def __init__(self, server_command: List[str]):
        self.server_command = server_command
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0
        self.tools_metadata: List[Dict[str, Any]] = []
    
    async def start(self):
        """Start the MCP server process"""
        self.process = subprocess.Popen(
            self.server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Initialize the MCP session
        init_result = await self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "copilot-mcp-bridge",
                "version": "1.0.0"
            }
        })
        
        # Load available tools
        tools_result = await self._send_request("tools/list")
        self.tools_metadata = tools_result.get("tools", [])
        
        print(f"✓ Loaded {len(self.tools_metadata)} tool(s) from MCP server", file=sys.stderr)
    
    async def stop(self):
        """Stop the MCP server process"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
    
    def _get_next_id(self) -> int:
        """Get next request ID"""
        self.request_id += 1
        return self.request_id
    
    async def _send_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a JSON-RPC request to the MCP server"""
        if not self.process:
            raise RuntimeError("MCP server not started")
        
        request = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": method
        }
        
        if params:
            request["params"] = params
        
        # Send request
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json)
        self.process.stdin.flush()
        
        # Read response
        response_line = self.process.stdout.readline()
        if not response_line:
            raise RuntimeError("No response from MCP server")
        
        response = json.loads(response_line)
        
        if "error" in response:
            raise RuntimeError(f"MCP server error: {response['error']}")
        
        return response.get("result", {})
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool on the MCP server"""
        result = await self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        
        # Extract text content from MCP response
        content = result.get("content", [])
        if content and len(content) > 0:
            return content[0].get("text", "")
        return ""
    
    def create_copilot_tools(self):
        """Create Copilot SDK tool wrappers for all MCP tools"""
        tools = []
        
        for tool_meta in self.tools_metadata:
            tool_name = tool_meta["name"]
            tool_desc = tool_meta["description"]
            tool_schema = tool_meta["inputSchema"]
            
            # Create a dynamic Pydantic model for the tool parameters
            param_model = self._create_param_model(tool_name, tool_schema)
            
            # Create the tool function
            tool_func = self._create_tool_function(tool_name, param_model)
            
            # Wrap with define_tool decorator
            wrapped_tool = define_tool(description=tool_desc)(tool_func)
            tools.append(wrapped_tool)
        
        return tools
    
    def _create_param_model(self, tool_name: str, schema: Dict[str, Any]) -> type:
        """Create a Pydantic model from JSON schema"""
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        # Build field definitions
        fields = {}
        for prop_name, prop_schema in properties.items():
            prop_type = self._json_type_to_python(prop_schema.get("type", "string"))
            prop_desc = prop_schema.get("description", "")
            
            if prop_name in required:
                fields[prop_name] = (prop_type, Field(description=prop_desc))
            else:
                fields[prop_name] = (Optional[prop_type], Field(default=None, description=prop_desc))
        
        # Create dynamic model
        model_name = f"{tool_name.replace('_', ' ').title().replace(' ', '')}Params"
        return type(model_name, (BaseModel,), {"__annotations__": {k: v[0] for k, v in fields.items()}, 
                                                 **{k: v[1] for k, v in fields.items()}})
    
    def _json_type_to_python(self, json_type: str) -> type:
        """Convert JSON schema type to Python type"""
        type_map = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict
        }
        return type_map.get(json_type, str)
    
    def _create_tool_function(self, tool_name: str, param_model: type):
        """Create an async function for calling the MCP tool"""
        async def tool_func(params: param_model) -> dict:
            # Convert Pydantic model to dict
            arguments = params.dict(exclude_none=True)
            
            # Call the MCP tool
            result_text = await self.call_tool(tool_name, arguments)
            
            # Try to parse as JSON, otherwise return as text
            try:
                return json.loads(result_text)
            except json.JSONDecodeError:
                return {"result": result_text}
        
        return tool_func


async def main():
    """Main entry point"""
    if not COPILOT_AVAILABLE:
        print("\n❌ Cannot start: GitHub Copilot SDK is required")
        print("   Install with: pip install github-copilot-sdk")
        sys.exit(1)
    
    print("🚀 Starting GitHub Copilot with MCP Protocol Integration\n")
    
    # Initialize MCP bridge
    mcp_bridge = MCPToolBridge(["python3", "mcp_server.py"])
    
    try:
        await mcp_bridge.start()
        
        # Create Copilot tools from MCP server
        tools = mcp_bridge.create_copilot_tools()
        
        # Initialize Copilot client
        client = CopilotClient()
        await client.start()
        
        # Create session with MCP-backed tools
        session = await client.create_session({
            "model": "gpt-4.1",
            "streaming": True,
            "tools": tools,
        })
        
        def handle_event(event):
            if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
                sys.stdout.write(event.data.delta_content)
                sys.stdout.flush()
        
        session.on(handle_event)
        
        print("🌤️  Weather Assistant with MCP (type 'exit' to quit)")
        print("   Try: 'What's the weather in Paris?' or 'Compare weather in NYC and LA'\n")
        
        while True:
            try:
                user_input = input("You: ")
            except EOFError:
                break
            
            if user_input.lower() == "exit":
                break
            
            sys.stdout.write("Assistant: ")
            await session.send_and_wait({"prompt": user_input})
            print("\n")
        
        await client.stop()
    
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    
    finally:
        await mcp_bridge.stop()


if __name__ == "__main__":
    asyncio.run(main())