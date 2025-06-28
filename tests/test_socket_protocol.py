"""
Tests for socket protocol and framed JSON utilities.
"""

import json
import pytest
import struct
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from io import BytesIO

from sbox_common.protocols.socket.framed_json import (
    FramedJSONProtocol,
    SocketMessageBuilder,
    get_protocol
)


class TestFramedJSONProtocol:
    """Test FramedJSONProtocol class."""
    
    def test_init_with_default_schema_dir(self):
        """Test initialization with default schema directory."""
        protocol = FramedJSONProtocol()
        assert protocol.schema_dir == Path(__file__).parent.parent / "src" / "sbox_common" / "protocols" / "socket"
    
    def test_init_with_custom_schema_dir(self, tmp_path):
        """Test initialization with custom schema directory."""
        protocol = FramedJSONProtocol(tmp_path)
        assert protocol.schema_dir == tmp_path
    
    def test_create_message_base(self):
        """Test creating base message structure."""
        protocol = FramedJSONProtocol()
        message = protocol.create_message_base("test")
        
        assert "id" in message
        assert "timestamp" in message
        assert message["type"] == "test"
        assert "correlation_id" not in message
        assert "metadata" not in message
    
    def test_create_message_base_with_optional_fields(self):
        """Test creating base message with optional fields."""
        protocol = FramedJSONProtocol()
        metadata = {"test": "value"}
        message = protocol.create_message_base(
            "test", 
            correlation_id="test-correlation",
            metadata=metadata
        )
        
        assert message["correlation_id"] == "test-correlation"
        assert message["metadata"] == metadata
    
    def test_create_event_message(self):
        """Test creating event message."""
        protocol = FramedJSONProtocol()
        event = {"event_type": "test.event", "data": {"test": "value"}}
        
        message = protocol.create_event_message(event)
        
        assert message["type"] == "event"
        assert message["event"] == event
    
    def test_create_command_message(self):
        """Test creating command message."""
        protocol = FramedJSONProtocol()
        params = {"param1": "value1"}
        
        message = protocol.create_command_message("test_command", params)
        
        assert message["type"] == "command"
        assert message["command"]["command"] == "test_command"
        assert message["command"]["params"] == params
    
    def test_create_response_message_success(self):
        """Test creating response message with success."""
        protocol = FramedJSONProtocol()
        data = {"result": "success"}
        
        message = protocol.create_response_message("req-123", "success", data=data)
        
        assert message["type"] == "response"
        assert message["response"]["status"] == "success"
        assert message["response"]["request_id"] == "req-123"
        assert message["response"]["data"] == data
        assert "error" not in message["response"]
    
    def test_create_response_message_error(self):
        """Test creating response message with error."""
        protocol = FramedJSONProtocol()
        error = {"code": "E001", "message": "Test error"}
        
        message = protocol.create_response_message("req-123", "error", error=error)
        
        assert message["type"] == "response"
        assert message["response"]["status"] == "error"
        assert message["response"]["error"] == error
        assert "data" not in message["response"]
    
    def test_create_heartbeat_message(self):
        """Test creating heartbeat message."""
        protocol = FramedJSONProtocol()
        
        message = protocol.create_heartbeat_message(
            "agent-123",
            "healthy",
            uptime_seconds=3600.5,
            version="1.0.0"
        )
        
        assert message["type"] == "heartbeat"
        assert message["heartbeat"]["agent_id"] == "agent-123"
        assert message["heartbeat"]["status"] == "healthy"
        assert message["heartbeat"]["uptime_seconds"] == 3600.5
        assert message["heartbeat"]["version"] == "1.0.0"
    
    def test_encode_message(self):
        """Test encoding message to framed JSON bytes."""
        protocol = FramedJSONProtocol()
        message = protocol.create_event_message({"test": "value"})
        
        encoded = protocol.encode_message(message)
        
        # Check frame header
        length, version = struct.unpack('>II', encoded[:8])
        assert version == 1  # PROTOCOL_VERSION
        assert length > 0
        
        # Check JSON data
        json_data = encoded[8:]
        decoded_message = json.loads(json_data.decode('utf-8'))
        assert decoded_message["type"] == "event"
    
    def test_decode_message(self):
        """Test decoding framed JSON message."""
        protocol = FramedJSONProtocol()
        original_message = protocol.create_event_message({"test": "value"})
        encoded = protocol.encode_message(original_message)
        
        decoded_message, bytes_consumed = protocol.decode_message(encoded)
        
        assert decoded_message["type"] == "event"
        assert decoded_message["event"]["test"] == "value"
        assert bytes_consumed == len(encoded)
    
    def test_decode_message_insufficient_data(self):
        """Test decoding with insufficient data."""
        protocol = FramedJSONProtocol()
        
        with pytest.raises(ValueError, match="Insufficient data for frame header"):
            protocol.decode_message(b"short")
    
    def test_decode_message_invalid_version(self):
        """Test decoding with invalid protocol version."""
        protocol = FramedJSONProtocol()
        
        # Create frame with invalid version
        json_str = json.dumps({"test": "value"})
        json_bytes = json_str.encode('utf-8')
        frame_header = struct.pack('>II', len(json_bytes), 999)  # Invalid version
        data = frame_header + json_bytes
        
        with pytest.raises(ValueError, match="Unsupported protocol version"):
            protocol.decode_message(data)
    
    def test_decode_message_too_large(self):
        """Test decoding message that's too large."""
        protocol = FramedJSONProtocol()
        
        # Create frame with very large length
        frame_header = struct.pack('>II', 2 * 1024 * 1024, 1)  # 2MB
        data = frame_header + b"test"
        
        with pytest.raises(ValueError, match="Message too large"):
            protocol.decode_message(data)
    
    def test_read_message(self):
        """Test reading message from reader."""
        protocol = FramedJSONProtocol()
        message = protocol.create_event_message({"test": "value"})
        encoded = protocol.encode_message(message)
        
        reader = BytesIO(encoded)
        decoded_message = protocol.read_message(reader)
        
        assert decoded_message["type"] == "event"
        assert decoded_message["event"]["test"] == "value"
    
    def test_read_message_no_data(self):
        """Test reading message when no data available."""
        protocol = FramedJSONProtocol()
        reader = BytesIO(b"")
        
        result = protocol.read_message(reader)
        assert result is None
    
    def test_write_message(self):
        """Test writing message to writer."""
        protocol = FramedJSONProtocol()
        message = protocol.create_event_message({"test": "value"})
        
        writer = BytesIO()
        protocol.write_message(writer, message)
        
        # Verify written data
        writer.seek(0)
        written_data = writer.read()
        decoded_message, _ = protocol.decode_message(written_data)
        
        assert decoded_message["type"] == "event"
        assert decoded_message["event"]["test"] == "value"


class TestSocketMessageBuilder:
    """Test SocketMessageBuilder class."""
    
    def test_init(self):
        """Test initialization."""
        protocol = FramedJSONProtocol()
        builder = SocketMessageBuilder(protocol)
        assert builder.protocol == protocol
    
    def test_event(self):
        """Test building event message."""
        protocol = FramedJSONProtocol()
        builder = SocketMessageBuilder(protocol)
        event = {"event_type": "test.event", "data": {"test": "value"}}
        
        encoded = builder.event(event)
        
        decoded_message, _ = protocol.decode_message(encoded)
        assert decoded_message["type"] == "event"
        assert decoded_message["event"] == event
    
    def test_command(self):
        """Test building command message."""
        protocol = FramedJSONProtocol()
        builder = SocketMessageBuilder(protocol)
        params = {"param1": "value1"}
        
        encoded = builder.command("test_command", params)
        
        decoded_message, _ = protocol.decode_message(encoded)
        assert decoded_message["type"] == "command"
        assert decoded_message["command"]["command"] == "test_command"
        assert decoded_message["command"]["params"] == params
    
    def test_response(self):
        """Test building response message."""
        protocol = FramedJSONProtocol()
        builder = SocketMessageBuilder(protocol)
        data = {"result": "success"}
        
        encoded = builder.response("req-123", "success", data=data)
        
        decoded_message, _ = protocol.decode_message(encoded)
        assert decoded_message["type"] == "response"
        assert decoded_message["response"]["status"] == "success"
        assert decoded_message["response"]["request_id"] == "req-123"
        assert decoded_message["response"]["data"] == data
    
    def test_heartbeat(self):
        """Test building heartbeat message."""
        protocol = FramedJSONProtocol()
        builder = SocketMessageBuilder(protocol)
        
        encoded = builder.heartbeat("agent-123", "healthy", uptime_seconds=3600.5)
        
        decoded_message, _ = protocol.decode_message(encoded)
        assert decoded_message["type"] == "heartbeat"
        assert decoded_message["heartbeat"]["agent_id"] == "agent-123"
        assert decoded_message["heartbeat"]["status"] == "healthy"
        assert decoded_message["heartbeat"]["uptime_seconds"] == 3600.5


class TestGetProtocol:
    """Test get_protocol function."""
    
    def test_get_protocol_default(self):
        """Test getting protocol with default schema directory."""
        protocol = get_protocol()
        assert isinstance(protocol, FramedJSONProtocol)
    
    def test_get_protocol_custom_schema_dir(self, tmp_path):
        """Test getting protocol with custom schema directory."""
        protocol = get_protocol(tmp_path)
        assert isinstance(protocol, FramedJSONProtocol)
        assert protocol.schema_dir == tmp_path


class TestProtocolValidation:
    """Test protocol validation functionality."""
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_validate_message_with_mock_schema(self, mock_exists, mock_file):
        """Test message validation with mock schema."""
        # Mock schema content
        mock_schema = {
            "type": "object",
            "required": ["id", "type", "timestamp"],
            "properties": {
                "id": {"type": "string"},
                "type": {"type": "string"},
                "timestamp": {"type": "string"}
            }
        }
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(mock_schema)
        
        protocol = FramedJSONProtocol()
        
        # Valid message
        valid_message = {
            "id": "test-id",
            "type": "event",
            "timestamp": "2023-01-01T00:00:00Z"
        }
        
        assert protocol.validate_message(valid_message) is True
        
        # Invalid message
        invalid_message = {
            "id": "test-id"
            # Missing required fields
        }
        
        with pytest.raises(Exception):
            protocol.validate_message(invalid_message)


if __name__ == "__main__":
    pytest.main([__file__]) 