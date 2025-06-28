"""
Tests for event protocols and converters.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from sbox_common.protocols.converters import (
    EventConverter,
    SubscriptionEventConverter,
    ConfigEventConverter,
    HealthEventConverter,
    get_event_converters
)


class TestEventConverter:
    """Test base EventConverter class."""
    
    def test_init_with_default_schema_dir(self):
        """Test initialization with default schema directory."""
        converter = EventConverter()
        assert converter.schema_dir == Path(__file__).parent.parent / "src" / "sbox_common" / "protocols" / "events"
    
    def test_init_with_custom_schema_dir(self, tmp_path):
        """Test initialization with custom schema directory."""
        converter = EventConverter(tmp_path)
        assert converter.schema_dir == tmp_path
    
    def test_create_event_base(self):
        """Test creating base event structure."""
        converter = EventConverter()
        event = converter.create_event_base("test.event", "sboxmgr")
        
        assert "event_id" in event
        assert "timestamp" in event
        assert event["source"] == "sboxmgr"
        assert event["event_type"] == "test.event"
        assert "correlation_id" not in event
        assert "metadata" not in event
    
    def test_create_event_base_with_optional_fields(self):
        """Test creating base event with optional fields."""
        converter = EventConverter()
        metadata = {"test": "value"}
        event = converter.create_event_base(
            "test.event", 
            "sboxagent", 
            correlation_id="test-correlation",
            metadata=metadata
        )
        
        assert event["correlation_id"] == "test-correlation"
        assert event["metadata"] == metadata


class TestSubscriptionEventConverter:
    """Test SubscriptionEventConverter class."""
    
    def test_create_subscription_created(self):
        """Test creating subscription.created event."""
        converter = SubscriptionEventConverter()
        subscription_data = {
            "subscription_id": "test-sub",
            "name": "Test Subscription",
            "url": "https://example.com/sub",
            "type": "sing-box"
        }
        
        event = converter.create_subscription_created(subscription_data)
        
        assert event["event_type"] == "subscription.created"
        assert event["source"] == "sboxmgr"
        assert event["data"] == subscription_data
    
    def test_create_subscription_deleted(self):
        """Test creating subscription.deleted event."""
        converter = SubscriptionEventConverter()
        event = converter.create_subscription_deleted("test-sub")
        
        assert event["event_type"] == "subscription.deleted"
        assert event["data"]["subscription_id"] == "test-sub"
    
    def test_create_subscription_update_completed_success(self):
        """Test creating subscription.update_completed event with success."""
        converter = SubscriptionEventConverter()
        event = converter.create_subscription_update_completed(
            "test-sub",
            "success",
            nodes_count=10,
            config_changed=True
        )
        
        assert event["event_type"] == "subscription.update_completed"
        assert event["data"]["status"] == "success"
        assert event["data"]["nodes_count"] == 10
        assert event["data"]["config_changed"] is True
        assert "error" not in event["data"]
    
    def test_create_subscription_update_completed_failed(self):
        """Test creating subscription.update_completed event with failure."""
        converter = SubscriptionEventConverter()
        event = converter.create_subscription_update_completed(
            "test-sub",
            "failed",
            error="Network timeout"
        )
        
        assert event["event_type"] == "subscription.update_completed"
        assert event["data"]["status"] == "failed"
        assert event["data"]["error"] == "Network timeout"


class TestConfigEventConverter:
    """Test ConfigEventConverter class."""
    
    def test_create_config_created(self):
        """Test creating config.created event."""
        converter = ConfigEventConverter()
        config_data = {
            "config_id": "test-config",
            "name": "Test Config",
            "type": "sing-box",
            "content": {"test": "content"}
        }
        
        event = converter.create_config_created(config_data)
        
        assert event["event_type"] == "config.created"
        assert event["data"] == config_data
    
    def test_create_config_activated(self):
        """Test creating config.activated event."""
        converter = ConfigEventConverter()
        event = converter.create_config_activated(
            "test-config",
            previous_config_id="old-config"
        )
        
        assert event["event_type"] == "config.activated"
        assert event["data"]["config_id"] == "test-config"
        assert event["data"]["previous_config_id"] == "old-config"
    
    def test_create_config_reload_requested(self):
        """Test creating config.reload_requested event."""
        converter = ConfigEventConverter()
        event = converter.create_config_reload_requested(
            "test-config",
            force=True
        )
        
        assert event["event_type"] == "config.reload_requested"
        assert event["data"]["config_id"] == "test-config"
        assert event["data"]["force"] is True


class TestHealthEventConverter:
    """Test HealthEventConverter class."""
    
    def test_create_health_status_changed(self):
        """Test creating health.status_changed event."""
        converter = HealthEventConverter()
        event = converter.create_health_status_changed(
            "sing-box",
            "healthy",
            "degraded",
            message="High CPU usage"
        )
        
        assert event["event_type"] == "health.status_changed"
        assert event["data"]["component"] == "sing-box"
        assert event["data"]["previous_status"] == "healthy"
        assert event["data"]["current_status"] == "degraded"
        assert event["data"]["message"] == "High CPU usage"
    
    def test_create_health_check_completed(self):
        """Test creating health.check_completed event."""
        converter = HealthEventConverter()
        components = [
            {
                "component": "sing-box",
                "status": "healthy",
                "message": "All good"
            }
        ]
        
        event = converter.create_health_check_completed(
            "check-123",
            "healthy",
            components,
            check_duration_ms=150,
            errors=["Component timeout"]
        )
        
        assert event["event_type"] == "health.check_completed"
        assert event["data"]["check_id"] == "check-123"
        assert event["data"]["overall_status"] == "healthy"
        assert event["data"]["components"] == components
        assert event["data"]["check_duration_ms"] == 150
        assert event["data"]["errors"] == ["Component timeout"]
    
    def test_create_health_alert_triggered(self):
        """Test creating health.alert_triggered event."""
        converter = HealthEventConverter()
        event = converter.create_health_alert_triggered(
            "alert-123",
            "warning",
            "High memory usage",
            "sing-box",
            threshold={"memory_percent": 80},
            current_value={"memory_percent": 85}
        )
        
        assert event["event_type"] == "health.alert_triggered"
        assert event["data"]["alert_id"] == "alert-123"
        assert event["data"]["severity"] == "warning"
        assert event["data"]["message"] == "High memory usage"
        assert event["data"]["component"] == "sing-box"
        assert event["data"]["acknowledged"] is False
        assert event["data"]["threshold"] == {"memory_percent": 80}
        assert event["data"]["current_value"] == {"memory_percent": 85}


class TestEventValidation:
    """Test event validation functionality."""
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.exists", return_value=True)
    def test_validate_event_with_mock_schema(self, mock_exists, mock_file):
        """Test event validation with mock schema."""
        # Mock schema content
        mock_schema = {
            "type": "object",
            "required": ["event_id", "timestamp", "source", "event_type"],
            "properties": {
                "event_id": {"type": "string"},
                "timestamp": {"type": "string"},
                "source": {"type": "string"},
                "event_type": {"type": "string"}
            }
        }
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(mock_schema)
        
        converter = EventConverter()
        
        # Valid event
        valid_event = {
            "event_id": "test-id",
            "timestamp": "2023-01-01T00:00:00Z",
            "source": "sboxmgr",
            "event_type": "test.event"
        }
        
        assert converter.validate_event(valid_event, "subscription-events") is True
        
        # Invalid event
        invalid_event = {
            "event_id": "test-id"
            # Missing required fields
        }
        
        with pytest.raises(Exception):
            converter.validate_event(invalid_event, "subscription-events")


class TestGetEventConverters:
    """Test get_event_converters function."""
    
    def test_get_event_converters(self):
        """Test getting all event converters."""
        converters = get_event_converters()
        
        assert "subscription" in converters
        assert "config" in converters
        assert "health" in converters
        
        assert isinstance(converters["subscription"], SubscriptionEventConverter)
        assert isinstance(converters["config"], ConfigEventConverter)
        assert isinstance(converters["health"], HealthEventConverter)
    
    def test_get_event_converters_with_custom_schema_dir(self, tmp_path):
        """Test getting converters with custom schema directory."""
        converters = get_event_converters(tmp_path)
        
        for converter in converters.values():
            assert converter.schema_dir == tmp_path


if __name__ == "__main__":
    pytest.main([__file__]) 