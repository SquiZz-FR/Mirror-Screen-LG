#!/usr/bin/env python3
"""
Stream Server Module

Handles WebSocket streaming of screen frames to connected clients (including LG WebOS TV).
"""

import asyncio
import logging
import websockets
from typing import Optional, Set
import json
import threading

logger = logging.getLogger(__name__)


class StreamServer:
    """
    WebSocket server for streaming screen frames to clients.
    
    Attributes:
        host (str): Host address to bind to.
        port (int): Port to listen on.
        server (websockets.WebSocketServer): WebSocket server instance.
        connected_clients (Set): Set of connected WebSocket clients.
        device_connector: Optional reference to DeviceConnector for TV-specific actions.
    """
    
    def __init__(self, host: str = '0.0.0.0', port: int = 8080):
        """
        Initialize the stream server.
        
        Args:
            host: Host address to bind to (default: '0.0.0.0').
            port: Port to listen on (default: 8080).
        """
        self.host = host
        self.port = port
        self.server: Optional[websockets.WebSocketServer] = None
        self.connected_clients: Set = set()
        self.device_connector = None
        self._running = False
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._server_thread: Optional[threading.Thread] = None
        logger.info(f"StreamServer initialized (Host: {host}, Port: {port})")
    
    def set_device_connector(self, connector):
        """
        Set the device connector for TV-specific actions.
        
        Args:
            connector: DeviceConnector instance.
        """
        self.device_connector = connector
        logger.debug("Device connector set for stream server")
    
    async def _handle_client(self, websocket, path):
        """
        Handle a new WebSocket client connection.
        
        Args:
            websocket: WebSocket connection.
            path: Request path.
        """
        client_id = id(websocket)
        logger.info(f"New client connected: {client_id}")
        self.connected_clients.add(websocket)
        
        try:
            # Send welcome message with server info
            welcome_msg = json.dumps({
                'type': 'welcome',
                'server': 'MirrorScreenLG',
                'message': 'Connected to screen mirroring server'
            })
            await websocket.send(welcome_msg)
            
            # Keep connection alive
            async for message in websocket:
                try:
                    data = json.loads(message)
                    logger.debug(f"Received message from client {client_id}: {data}")
                    
                    # Handle client messages (e.g., control commands)
                    if data.get('type') == 'ping':
                        await websocket.send(json.dumps({'type': 'pong'}))
                    
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON from client {client_id}: {message}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_id} disconnected")
        except Exception as e:
            logger.error(f"Error with client {client_id}: {e}", exc_info=True)
        finally:
            self.connected_clients.discard(websocket)
            logger.info(f"Client {client_id} removed. Active clients: {len(self.connected_clients)}")
    
    async def _broadcast_frame(self, frame_data: bytes):
        """
        Broadcast a frame to all connected clients.
        
        Args:
            frame_data: JPEG-encoded frame bytes.
        """
        if not self.connected_clients:
            return
        
        try:
            # Send frame to all clients
            tasks = []
            for websocket in self.connected_clients:
                try:
                    # Send as binary data (more efficient for images)
                    tasks.append(websocket.send(frame_data))
                except Exception as e:
                    logger.error(f"Failed to send frame to client: {e}")
            
            # Wait for all sends to complete (with timeout)
            if tasks:
                await asyncio.wait(tasks, timeout=0.1)
                
        except Exception as e:
            logger.error(f"Error broadcasting frame: {e}", exc_info=True)
    
    def send_frame(self, frame_data: bytes):
        """
        Send a frame to all connected clients (thread-safe).
        
        Args:
            frame_data: JPEG-encoded frame bytes.
        """
        if not self._running or not self.connected_clients:
            return
        
        # Run in the event loop thread
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(
                self._broadcast_frame(frame_data),
                self._loop
            )
    
    def start(self):
        """Start the WebSocket server in a background thread."""
        if self._running:
            logger.warning("Stream server is already running")
            return
        
        self._running = True
        
        # Create new event loop for the server
        self._loop = asyncio.new_event_loop()
        
        # Start server in background thread
        self._server_thread = threading.Thread(
            target=self._run_server,
            daemon=True
        )
        self._server_thread.start()
        
        # Give the server a moment to start
        import time
        time.sleep(0.5)
        
        logger.info(f"WebSocket server started on ws://{self.host}:{self.port}")
    
    def _run_server(self):
        """Run the WebSocket server in the event loop."""
        try:
            # Set the event loop for this thread
            asyncio.set_event_loop(self._loop)
            
            # Create the server
            self.server = websockets.serve(
                self._handle_client,
                self.host,
                self.port,
                ping_interval=20,
                ping_timeout=60
            )
            
            # Run the server in the event loop
            self._loop.run_until_complete(self.server)
            self._loop.run_forever()
        except Exception as e:
            logger.error(f"WebSocket server error: {e}", exc_info=True)
        finally:
            self._loop.close()
            self._running = False
    
    def stop(self):
        """Stop the WebSocket server."""
        if not self._running:
            return
        
        self._running = False
        logger.info("Stopping WebSocket server...")
        
        try:
            # Close all client connections
            for websocket in self.connected_clients:
                try:
                    if self._loop and self._loop.is_running():
                        asyncio.run_coroutine_threadsafe(websocket.close(), self._loop)
                except:
                    pass
            
            self.connected_clients.clear()
            
            # Stop the server
            if self.server:
                self.server.ws_server.close()
                # Signal the loop to stop
                if self._loop:
                    self._loop.call_soon_threadsafe(self._loop.stop)
            
            # Wait for thread to finish
            if self._server_thread:
                self._server_thread.join(timeout=2)
                
        except Exception as e:
            logger.error(f"Error stopping server: {e}", exc_info=True)
        finally:
            logger.info("WebSocket server stopped")
    
    def get_client_count(self) -> int:
        """Get the number of connected clients."""
        return len(self.connected_clients)
