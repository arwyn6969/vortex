"""Tests for MCP transport implementations."""

import pytest
import asyncio
import json
from typing import AsyncGenerator
from src.core.ai.mcp_transport import (
    MCPTransport,
    MCPRequest,
    MCPResponse,
    StdioTransport,
    HTTPTransport,
    WebSocketTransport,
    TransportType
)

@pytest.fixture
def mock_process(monkeypatch):
    """Fixture for mocking subprocess communication."""
    class MockProcess:
        def __init__(self):
            self.returncode = None
            self.stdin = asyncio.StreamWriter(None, None, None, None)
            self.stdout = asyncio.StreamReader()
            self.responses = []
            
        async def wait(self):
            return 0
            
        def terminate(self):
            self.returncode = 0
            
        def kill(self):
            self.returncode = -9
            
        async def add_response(self, response):
            self.responses.append(response)
            self.stdout.feed_data(f"{json.dumps(response)}\n".encode())
            
    return MockProcess()

@pytest.fixture
async def stdio_transport(mock_process, monkeypatch):
    """Fixture for StdioTransport with mocked process."""
    async def mock_create_subprocess(*args, **kwargs):
        return mock_process
        
    monkeypatch.setattr(
        "asyncio.create_subprocess_shell",
        mock_create_subprocess
    )
    
    transport = StdioTransport("mock_cmd")
    yield transport
    await transport.close()

@pytest.mark.asyncio
async def test_stdio_transport_basic(stdio_transport, mock_process):
    """Test basic stdio transport functionality."""
    request = MCPRequest(
        type="generate",
        payload={"prompt": "test"},
        metadata={"test": True}
    )
    
    # Add mock responses
    await mock_process.add_response({
        "type": "text",
        "payload": {"content": "Hello"},
        "metadata": {}
    })
    await mock_process.add_response({
        "type": "done",
        "payload": {},
        "metadata": {}
    })
    mock_process.stdout.feed_eof()
    
    responses = []
    async for response in stdio_transport.send_request(request):
        responses.append(response)
        
    assert len(responses) == 2
    assert responses[0].type == "text"
    assert responses[0].payload["content"] == "Hello"
    assert responses[1].type == "done"

@pytest.mark.asyncio
async def test_stdio_transport_error(stdio_transport, mock_process):
    """Test stdio transport error handling."""
    request = MCPRequest(
        type="generate",
        payload={"prompt": "test"},
        metadata={}
    )
    
    # Add error response
    await mock_process.add_response({
        "type": "error",
        "payload": {"error": "Test error"},
        "metadata": {}
    })
    mock_process.stdout.feed_eof()
    
    responses = []
    async for response in stdio_transport.send_request(request):
        responses.append(response)
        
    assert len(responses) == 1
    assert responses[0].type == "error"
    assert responses[0].payload["error"] == "Test error"

@pytest.mark.asyncio
async def test_http_transport(monkeypatch):
    """Test HTTP transport functionality."""
    import httpx
    
    class MockResponse:
        def __init__(self, status_code=200):
            self.status_code = status_code
            self.lines = []
            
        def raise_for_status(self):
            if self.status_code != 200:
                raise httpx.HTTPError(f"HTTP {self.status_code}")
                
        async def aiter_lines(self):
            for line in self.lines:
                yield line
                
        def add_line(self, data):
            self.lines.append(json.dumps(data))
            
    class MockClient:
        async def __aenter__(self):
            return self
            
        async def __aexit__(self, *args):
            pass
            
        async def stream(self, *args, **kwargs):
            response = MockResponse()
            response.add_line({
                "type": "text",
                "payload": {"content": "Test response"},
                "metadata": {}
            })
            return response
            
    monkeypatch.setattr(httpx, "AsyncClient", lambda: MockClient())
    
    transport = HTTPTransport("http://test", {"test": "header"})
    request = MCPRequest(
        type="generate",
        payload={"prompt": "test"},
        metadata={}
    )
    
    responses = []
    async for response in transport.send_request(request):
        responses.append(response)
        
    assert len(responses) == 1
    assert responses[0].type == "text"
    assert responses[0].payload["content"] == "Test response"

@pytest.mark.asyncio
async def test_websocket_transport(monkeypatch):
    """Test WebSocket transport functionality."""
    import websockets
    
    class MockWebSocket:
        def __init__(self):
            self.closed = False
            self.sent = []
            self.responses = []
            
        async def send(self, data):
            self.sent.append(json.loads(data))
            
        async def recv(self):
            if self.responses:
                return json.dumps(self.responses.pop(0))
            return json.dumps({"type": "done", "payload": {}, "metadata": {}})
            
        async def close(self):
            self.closed = True
            
    async def mock_connect(*args, **kwargs):
        return MockWebSocket()
        
    monkeypatch.setattr(websockets, "connect", mock_connect)
    
    transport = WebSocketTransport("ws://test")
    request = MCPRequest(
        type="generate",
        payload={"prompt": "test"},
        metadata={}
    )
    
    ws = await websockets.connect("")
    ws.responses = [{
        "type": "text",
        "payload": {"content": "Test response"},
        "metadata": {}
    }]
    
    responses = []
    async for response in transport.send_request(request):
        responses.append(response)
        
    assert len(responses) == 2  # text + done
    assert responses[0].type == "text"
    assert responses[0].payload["content"] == "Test response"
    assert responses[1].type == "done"
    
    await transport.close()
    assert ws.closed 