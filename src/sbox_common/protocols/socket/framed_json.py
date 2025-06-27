"""
Framed JSON protocol utilities for Unix socket communication.

This module provides utilities for sending and receiving framed JSON messages
over Unix sockets with proper framing and validation.
"""

import json
import struct
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Union
from pathlib import Path

import jsonschema
from jsonschema import ValidationError


class FramedJSONProtocol:
    """Framed JSON protocol for Unix socket communication."""
    
    # Protocol constants
    FRAME_HEADER_SIZE = 8  # 4 bytes for length + 4 bytes for version
    PROTOCOL_VERSION = 1
    
    def __init__(self, schema_dir: Optional[Path] = None):
        """Initialize protocol with schema directory."""
        self.schema_dir = schema_dir or Path(__file__).parent
        self._load_schemas()
    
    def _load_schemas(self) -> None:
        """Load protocol schemas."""
        schema_path = self.schema_dir / "protocol_v1.schema.json"
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                self._protocol_schema = json.load(f)
        else:
            self._protocol_schema = None
    
    def validate_message(self, message: Dict[str, Any]) -> bool:
        """Validate message against protocol schema."""
        if not self._protocol_schema:
            return True  # Skip validation if schema not available
        
        try:
            jsonschema.validate(message, self._protocol_schema)
            return True
        except ValidationError as e:
            raise ValidationError(f"Message validation failed: {e.message}")
    
    def create_message_base(self, 
                           message_type: str,
                           correlation_id: Optional[str] = None,
                           metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create base message structure."""
        message = {
            "id": str(uuid.uuid4()),
            "type": message_type,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        if correlation_id:
            message["correlation_id"] = correlation_id
        
        if metadata:
            message["metadata"] = metadata
        
        return message
    
    def create_event_message(self,
                           event: Dict[str, Any],
                           correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create event message."""
        message = self.create_message_base("event", correlation_id)
        message["event"] = event
        return message
    
    def create_command_message(self,
                             command: str,
                             params: Dict[str, Any],
                             correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create command message."""
        message = self.create_message_base("command", correlation_id)
        message["command"] = {
            "command": command,
            "params": params
        }
        return message
    
    def create_response_message(self,
                              request_id: str,
                              status: str,
                              data: Optional[Dict[str, Any]] = None,
                              error: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create response message."""
        message = self.create_message_base("response")
        message["response"] = {
            "status": status,
            "request_id": request_id
        }
        
        if data:
            message["response"]["data"] = data
        
        if error:
            message["response"]["error"] = error
        
        return message
    
    def create_heartbeat_message(self,
                               agent_id: str,
                               status: str,
                               uptime_seconds: Optional[float] = None,
                               version: Optional[str] = None) -> Dict[str, Any]:
        """Create heartbeat message."""
        message = self.create_message_base("heartbeat")
        message["heartbeat"] = {
            "agent_id": agent_id,
            "status": status
        }
        
        if uptime_seconds is not None:
            message["heartbeat"]["uptime_seconds"] = uptime_seconds
        
        if version:
            message["heartbeat"]["version"] = version
        
        return message
    
    def encode_message(self, message: Dict[str, Any]) -> bytes:
        """Encode message to framed JSON bytes."""
        # Validate message
        self.validate_message(message)
        
        # Convert to JSON string
        json_str = json.dumps(message, separators=(',', ':'))
        json_bytes = json_str.encode('utf-8')
        
        # Create frame header: 4 bytes length + 4 bytes version
        frame_header = struct.pack('>II', len(json_bytes), self.PROTOCOL_VERSION)
        
        # Combine header and data
        return frame_header + json_bytes
    
    def decode_message(self, data: bytes) -> Tuple[Dict[str, Any], int]:
        """Decode framed JSON message from bytes.
        
        Returns:
            Tuple of (message, bytes_consumed)
        """
        if len(data) < self.FRAME_HEADER_SIZE:
            raise ValueError("Insufficient data for frame header")
        
        # Extract frame header
        length, version = struct.unpack('>II', data[:self.FRAME_HEADER_SIZE])
        
        if version != self.PROTOCOL_VERSION:
            raise ValueError(f"Unsupported protocol version: {version}")
        
        if length > 1024 * 1024:  # 1MB limit
            raise ValueError(f"Message too large: {length} bytes")
        
        # Check if we have enough data
        total_size = self.FRAME_HEADER_SIZE + length
        if len(data) < total_size:
            raise ValueError(f"Insufficient data: need {total_size}, have {len(data)}")
        
        # Extract JSON data
        json_bytes = data[self.FRAME_HEADER_SIZE:self.FRAME_HEADER_SIZE + length]
        json_str = json_bytes.decode('utf-8')
        
        # Parse JSON
        try:
            message = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
        
        # Validate message
        self.validate_message(message)
        
        return message, total_size
    
    def read_message(self, reader) -> Optional[Dict[str, Any]]:
        """Read a complete message from a reader object.
        
        Args:
            reader: Object with read() method (file, socket, etc.)
        
        Returns:
            Message dict or None if no data available
        """
        # Read frame header
        header_data = reader.read(self.FRAME_HEADER_SIZE)
        if not header_data:
            return None  # No data available
        
        if len(header_data) < self.FRAME_HEADER_SIZE:
            raise ValueError("Incomplete frame header")
        
        # Extract length and version
        length, version = struct.unpack('>II', header_data)
        
        if version != self.PROTOCOL_VERSION:
            raise ValueError(f"Unsupported protocol version: {version}")
        
        if length > 1024 * 1024:  # 1MB limit
            raise ValueError(f"Message too large: {length} bytes")
        
        # Read message data
        message_data = reader.read(length)
        if len(message_data) < length:
            raise ValueError(f"Incomplete message: need {length}, got {len(message_data)}")
        
        # Decode message
        json_str = message_data.decode('utf-8')
        try:
            message = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
        
        # Validate message
        self.validate_message(message)
        
        return message
    
    def write_message(self, writer, message: Dict[str, Any]) -> None:
        """Write a complete message to a writer object.
        
        Args:
            writer: Object with write() method (file, socket, etc.)
            message: Message dict to send
        """
        encoded = self.encode_message(message)
        writer.write(encoded)
        writer.flush()  # Ensure data is sent immediately


class SocketMessageBuilder:
    """Helper class for building socket messages."""
    
    def __init__(self, protocol: FramedJSONProtocol):
        """Initialize with protocol instance."""
        self.protocol = protocol
    
    def event(self, event: Dict[str, Any], correlation_id: Optional[str] = None) -> bytes:
        """Build event message."""
        message = self.protocol.create_event_message(event, correlation_id)
        return self.protocol.encode_message(message)
    
    def command(self, command: str, params: Dict[str, Any], correlation_id: Optional[str] = None) -> bytes:
        """Build command message."""
        message = self.protocol.create_command_message(command, params, correlation_id)
        return self.protocol.encode_message(message)
    
    def response(self, request_id: str, status: str, data: Optional[Dict[str, Any]] = None, error: Optional[Dict[str, Any]] = None) -> bytes:
        """Build response message."""
        message = self.protocol.create_response_message(request_id, status, data, error)
        return self.protocol.encode_message(message)
    
    def heartbeat(self, agent_id: str, status: str, uptime_seconds: Optional[float] = None, version: Optional[str] = None) -> bytes:
        """Build heartbeat message."""
        message = self.protocol.create_heartbeat_message(agent_id, status, uptime_seconds, version)
        return self.protocol.encode_message(message)


# Convenience function to get protocol instance
def get_protocol(schema_dir: Optional[Path] = None) -> FramedJSONProtocol:
    """Get protocol instance."""
    return FramedJSONProtocol(schema_dir) 