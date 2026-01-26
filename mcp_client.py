#!/usr/bin/env python3
"""
MCP Client example for testing the GitHub Copilot SDK Demo MCP Server

This client demonstrates how to interact with the MCP server using
the Model Context Protocol over stdio transport.
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, Optional


class MCPClient:
    """Simple MCP client for testing"""
    
    def __init__(self, server_command: list):
        self.server_command = server_command
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0
    
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
        print("MCP Server process started", file=sys.stderr)
    
    async def stop(self):
        """Stop the MCP server process"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print("MCP Server process stopped", file=sys.stderr)
    
    def _get_next_id(self) -> int:
        """Get next request ID"""
        self.request_id += 1
        return self.request_id
    
    async def send_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a JSON-RPC request to the server"""
        if not self.process:
            raise RuntimeError("Server not started")
        
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
            raise RuntimeError("No response from server")
        
        response = json.loads(response_line)
        
        if "error" in response:
            raise RuntimeError(f"Server error: {response['error']}")
        
        return response.get("result", {})
    
    async def initialize(self) -> Dict[str, Any]:
        """Initialize the MCP session"""
        return await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "mcp-test-client",
                "version": "1.0.0"
            }
        })
    
    async def list_tools(self) -> Dict[str, Any]:
        """List available tools"""
        return await self.send_request("tools/list")
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool"""
        return await self.send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })


async def main():
    """Main entry point for testing"""
    print("🌤️  MCP Weather Demo Client\n")
    
    # Start client
    client = MCPClient(["python3", "mcp_server.py"])
    
    try:
        await client.start()
        
        # Initialize
        print("Initializing MCP session...")
        init_result = await client.initialize()
        print(f"✓ Server: {init_result['serverInfo']['name']} v{init_result['serverInfo']['version']}")
        print(f"✓ Protocol: {init_result['protocolVersion']}\n")
        
        # List tools
        print("Listing available tools...")
        tools_result = await client.list_tools()
        tools = tools_result.get("tools", [])
        print(f"✓ Found {len(tools)} tool(s):")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        print()
        
        # Test weather tool with different cities
        test_cities = ["Paris", "New York", "Tokyo", "London"]
        
        print("Testing weather tool with various cities:\n")
        for city in test_cities:
            print(f"🌍 Calling get_weather for {city}...")
            result = await client.call_tool("get_weather", {"city": city})
            
            # Parse the result
            content = result.get("content", [])
            if content:
                weather_data = json.loads(content[0]["text"])
                print(f"   Temperature: {weather_data['temperature']}")
                print(f"   Condition: {weather_data['condition']}")
            print()
        
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())
