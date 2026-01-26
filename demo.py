#!/usr/bin/env python3
"""
Interactive MCP Demo

This script demonstrates how the MCP server can be used interactively
by simulating requests from an AI assistant.
"""

import asyncio
import json
import subprocess
import sys
from typing import Optional


class InteractiveMCPDemo:
    """Interactive demonstration of MCP capabilities"""
    
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0
    
    async def start_server(self):
        """Start the MCP server"""
        self.process = subprocess.Popen(
            ["python3", "mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        print("✓ MCP Server started\n", file=sys.stderr)
    
    async def stop_server(self):
        """Stop the MCP server"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
    
    async def send_request(self, method: str, params: Optional[dict] = None) -> dict:
        """Send a request and get response"""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method
        }
        if params:
            request["params"] = params
        
        # Send
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: self.process.stdin.write(json.dumps(request) + "\n")
        )
        await loop.run_in_executor(None, self.process.stdin.flush)
        
        # Receive
        response_line = await loop.run_in_executor(
            None,
            self.process.stdout.readline
        )
        return json.loads(response_line)
    
    def print_section(self, title: str):
        """Print a section header"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    
    async def run_demo(self):
        """Run the interactive demo"""
        print("\n🎯 GitHub Copilot SDK Demo - MCP Protocol Implementation\n")
        print("This demo shows how AI assistants can use tools through MCP.\n")
        
        await self.start_server()
        
        try:
            # Step 1: Initialize
            self.print_section("1. Initialize MCP Session")
            print("Request:")
            init_request = {
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "demo-client", "version": "1.0.0"}
                }
            }
            print(json.dumps(init_request, indent=2))
            
            response = await self.send_request(
                "initialize",
                init_request["params"]
            )
            
            print("\nResponse:")
            print(json.dumps(response.get("result", {}), indent=2))
            
            # Step 2: List Tools
            self.print_section("2. Discover Available Tools")
            print("Request:")
            print(json.dumps({"method": "tools/list"}, indent=2))
            
            response = await self.send_request("tools/list")
            result = response.get("result", {})
            
            print("\nResponse:")
            print(json.dumps(result, indent=2))
            
            # Step 3: Call Tool
            self.print_section("3. Call Weather Tool")
            
            cities = ["San Francisco", "Seattle"]
            
            for city in cities:
                print(f"\n📍 Getting weather for {city}...")
                print("\nRequest:")
                call_request = {
                    "method": "tools/call",
                    "params": {
                        "name": "get_weather",
                        "arguments": {"city": city}
                    }
                }
                print(json.dumps(call_request, indent=2))
                
                response = await self.send_request(
                    "tools/call",
                    call_request["params"]
                )
                
                print("\nResponse:")
                result = response.get("result", {})
                print(json.dumps(result, indent=2))
                
                # Parse and display nicely
                if result.get("content"):
                    weather_data = json.loads(result["content"][0]["text"])
                    print("\n🌤️  Weather Summary:")
                    print(f"   City: {weather_data['city']}")
                    print(f"   Temperature: {weather_data['temperature']}")
                    print(f"   Condition: {weather_data['condition']}")
            
            # Step 4: Summary
            self.print_section("4. Demo Complete")
            print("✅ Successfully demonstrated MCP protocol capabilities:")
            print("   • Session initialization with protocol negotiation")
            print("   • Tool discovery via tools/list")
            print("   • Tool execution via tools/call")
            print("   • JSON-RPC 2.0 request/response handling")
            print("\n🎉 This MCP server can now be used with any MCP-compatible")
            print("   AI assistant, including GitHub Copilot!\n")
            
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
        finally:
            await self.stop_server()


async def main():
    """Main entry point"""
    demo = InteractiveMCPDemo()
    await demo.run_demo()


if __name__ == "__main__":
    asyncio.run(main())
