#!/usr/bin/env python3
"""
MCP Server implementation for GitHub Copilot SDK Demo

This server implements the Model Context Protocol (MCP) to provide tools
that can be used by AI assistants like GitHub Copilot.
"""

import asyncio
import json
import random
import sys
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Tool:
    """Represents an MCP tool"""
    name: str
    description: str
    input_schema: Dict[str, Any]


class MCPServer:
    """MCP Server implementation"""
    
    def __init__(self):
        self.tools: List[Tool] = []
        self.server_info = {
            "name": "github-copilot-demo-server",
            "version": "1.0.0"
        }
        self._register_tools()
    
    def _register_tools(self):
        """Register available tools"""
        self.tools.append(Tool(
            name="get_weather",
            description="Get the current weather for a city",
            input_schema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get weather for"
                    }
                },
                "required": ["city"]
            }
        ))
    
    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": self.server_info
        }
    
    async def handle_tools_list(self) -> Dict[str, Any]:
        """Handle tools/list request"""
        return {
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.input_schema
                }
                for tool in self.tools
            ]
        }
    
    async def handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "get_weather":
            return await self._get_weather(arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    async def _get_weather(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get weather for a city"""
        city = arguments.get("city", "")
        
        # Simulate weather data
        conditions = ["sunny", "cloudy", "rainy", "partly cloudy", "snowy"]
        temp = random.randint(50, 80)
        condition = random.choice(conditions)
        
        result = {
            "city": city,
            "temperature": f"{temp}°F",
            "condition": condition
        }
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2)
                }
            ]
        }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                result = await self.handle_initialize(params)
            elif method == "tools/list":
                result = await self.handle_tools_list()
            elif method == "tools/call":
                result = await self.handle_tools_call(params)
            else:
                raise ValueError(f"Unknown method: {method}")
            
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
        
        return response
    
    async def run(self):
        """Run the MCP server using stdio transport"""
        print("MCP Server started. Listening on stdin...", file=sys.stderr)
        
        while True:
            try:
                # Read line from stdin
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Parse JSON-RPC request
                try:
                    request = json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"Invalid JSON: {e}", file=sys.stderr)
                    continue
                
                # Handle request
                response = await self.handle_request(request)
                
                # Send response to stdout
                print(json.dumps(response), flush=True)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                break


async def main():
    """Main entry point"""
    server = MCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
