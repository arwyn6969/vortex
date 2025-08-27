"""
Model Control Protocol (MCP) transport implementation.
Provides standardized communication with AI models using Vercel AI SDK patterns.
"""

import asyncio
import json
from typing import AsyncGenerator, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging
import httpx
from .retry import with_retry, RetryConfig

logger = logging.getLogger(__name__)

class TransportType(Enum):
    """Supported transport types for model communication."""
    STDIO = "stdio"
    HTTP = "http"
    WEBSOCKET = "websocket"

@dataclass
class MCPRequest:
    """MCP request structure."""
    type: str
    payload: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class MCPResponse:
    """MCP response structure."""
    type: str
    payload: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

class MCPTransport:
    """Base class for MCP transports."""
    
    async def send_request(self, request: MCPRequest) -> AsyncGenerator[MCPResponse, None]:
        """Send request through the transport.
        
        Args:
            request: The MCP request to send
            
        Yields:
            Response chunks from the model
        """
        raise NotImplementedError()
        
    async def close(self):
        """Close the transport connection."""
        pass

class StdioTransport(MCPTransport):
    """MCP transport using stdio for model communication."""
    
    def __init__(self, process_cmd: str):
        """Initialize stdio transport.
        
        Args:
            process_cmd: Command to start the model process
        """
        self.process_cmd = process_cmd
        self.process = None
        self._setup_lock = asyncio.Lock()
        
    async def _ensure_process(self):
        """Ensure the model process is running."""
        if self.process is None or self.process.returncode is not None:
            async with self._setup_lock:
                if self.process is None or self.process.returncode is not None:
                    self.process = await asyncio.create_subprocess_shell(
                        self.process_cmd,
                        stdin=asyncio.subprocess.PIPE,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    
    async def send_request(self, request: MCPRequest) -> AsyncGenerator[MCPResponse, None]:
        """Send request through stdio transport.
        
        Args:
            request: The MCP request to send
            
        Yields:
            Response chunks from the model
        """
        await self._ensure_process()
        
        try:
            # Send request
            request_data = json.dumps({
                "type": request.type,
                "payload": request.payload,
                "metadata": request.metadata or {}
            })
            self.process.stdin.write(f"{request_data}\n".encode())
            await self.process.stdin.drain()
            
            # Read responses
            while True:
                if self.process.stdout.at_eof():
                    break
                    
                line = await self.process.stdout.readline()
                if not line:
                    break
                    
                try:
                    response_data = json.loads(line)
                    yield MCPResponse(
                        type=response_data["type"],
                        payload=response_data["payload"],
                        metadata=response_data.get("metadata")
                    )
                    
                    if response_data["type"] == "error":
                        logger.error(f"Model error: {response_data['payload']}")
                        break
                    elif response_data["type"] == "done":
                        break
                        
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse model response: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Stdio transport error: {e}")
            # Kill process on error to ensure clean state
            self.process.kill()
            self.process = None
            raise
            
    async def close(self):
        """Close the stdio transport."""
        if self.process is not None:
            try:
                self.process.terminate()
                await asyncio.wait_for(self.process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self.process.kill()
            finally:
                self.process = None

class HTTPTransport(MCPTransport):
    """MCP transport using HTTP for model communication."""
    
    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        pool_limits: Optional[httpx.Limits] = None,
        retry_config: Optional[RetryConfig] = None
    ):
        """Initialize HTTP transport.
        
        Args:
            base_url: Base URL for model API
            headers: Optional headers for requests
            pool_limits: Optional connection pool limits
            retry_config: Optional retry configuration
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.pool_limits = pool_limits or httpx.Limits(
            max_keepalive_connections=10,
            max_connections=20,
            keepalive_expiry=30.0
        )
        self.retry_config = retry_config or RetryConfig()
        self._client: Optional[httpx.AsyncClient] = None
        self._client_lock = asyncio.Lock()
        
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            async with self._client_lock:
                if self._client is None:
                    self._client = httpx.AsyncClient(
                        limits=self.pool_limits,
                        timeout=30.0
                    )
        return self._client
        
    @with_retry()
    async def send_request(self, request: MCPRequest) -> AsyncGenerator[MCPResponse, None]:
        """Send request through HTTP transport.
        
        Args:
            request: The MCP request to send
            
        Yields:
            Response chunks from the model
        """
        client = await self._get_client()
        
        async with client.stream(
            "POST",
            f"{self.base_url}/v1/completions",
            headers=self.headers,
            json={
                "type": request.type,
                "payload": request.payload,
                "metadata": request.metadata or {}
            }
        ) as response:
            response.raise_for_status()
            
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                    
                try:
                    data = json.loads(line)
                    yield MCPResponse(
                        type=data["type"],
                        payload=data["payload"],
                        metadata=data.get("metadata")
                    )
                except json.JSONDecodeError:
                    continue
                    
    async def close(self):
        """Close the HTTP transport."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

class WebSocketTransport(MCPTransport):
    """MCP transport using WebSocket for model communication."""
    
    def __init__(self, ws_url: str):
        """Initialize WebSocket transport.
        
        Args:
            ws_url: WebSocket URL for model connection
        """
        self.ws_url = ws_url
        self.ws = None
        
    async def send_request(self, request: MCPRequest) -> AsyncGenerator[MCPResponse, None]:
        """Send request through WebSocket transport.
        
        Args:
            request: The MCP request to send
            
        Yields:
            Response chunks from the model
        """
        import websockets
        
        if self.ws is None:
            self.ws = await websockets.connect(self.ws_url)
            
        try:
            await self.ws.send(json.dumps({
                "type": request.type,
                "payload": request.payload,
                "metadata": request.metadata or {}
            }))
            
            while True:
                message = await self.ws.recv()
                try:
                    data = json.loads(message)
                    yield MCPResponse(
                        type=data["type"],
                        payload=data["payload"],
                        metadata=data.get("metadata")
                    )
                    
                    if data["type"] in ["error", "done"]:
                        break
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            logger.error(f"WebSocket transport error: {e}")
            await self.close()
            raise
            
    async def close(self):
        """Close the WebSocket transport."""
        if self.ws is not None:
            await self.ws.close()
            self.ws = None 