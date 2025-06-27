# Sbox Common

Shared protocols and utilities for sboxagent/sboxmgr integration.

## Overview

This package provides common protocols and utilities used by both sboxagent (Go) and sboxmgr (Python) for inter-process communication.

## Installation

### Development (editable install)
```bash
pip install -e .
```

### Production
```bash
pip install sbox-common
```

## Structure

```
src/sbox_common/
├── __init__.py
└── protocols/
    ├── __init__.py
    ├── socket/
    │   ├── __init__.py
    │   ├── framed_json.py          # Framed JSON protocol implementation
    │   └── protocol_v1.schema.json # Protocol schema for validation
    ├── events/                     # Event schemas
    └── converters.py               # Data converters
```

## Framed JSON Protocol

The framed JSON protocol enables reliable communication between sboxagent and sboxmgr via Unix sockets.

### Message Format

Each message consists of:
- **Frame Header**: 8 bytes (4 bytes length + 4 bytes protocol version)
- **JSON Payload**: UTF-8 encoded JSON message

### Message Types

1. **Event Messages**: Notifications and status updates
2. **Command Messages**: Requests to execute actions
3. **Response Messages**: Replies to commands
4. **Heartbeat Messages**: Health and status information

### Usage Example

```python
from sbox_common.protocols.socket.framed_json import FramedJSONProtocol

# Create protocol instance
protocol = FramedJSONProtocol()

# Create event message
event_msg = protocol.create_event_message({
    "type": "config_updated",
    "data": {"config_id": "test-123"}
})

# Encode for transmission
encoded = protocol.encode_message(event_msg)
```

## Development

### Dependencies
- Python >= 3.8
- jsonschema >= 4.0.0

### Testing
```bash
pytest tests/
```

## License

Apache-2.0 