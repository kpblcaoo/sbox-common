"""
Event protocol converters for sbox-common.

This module provides converters for transforming events between different formats
and validating event schemas.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

import jsonschema
from jsonschema import ValidationError

# Set up logging
logger = logging.getLogger(__name__)


class EventConverter:
    """Base class for event converters."""
    
    def __init__(self, schema_dir: Optional[Union[Path, str]] = None):
        """Initialize converter with schema directory."""
        if schema_dir is None:
            # Default to the events directory where schemas are located
            # This should match the test expectation: Path(__file__).parent.parent / "src" / "sbox_common" / "protocols" / "events"
            schema_dir = Path(__file__).parent / "events"
        elif isinstance(schema_dir, str):
            schema_dir = Path(schema_dir)
        self.schema_dir = schema_dir
        self._schemas = {}
        self._load_schemas()
    
    def _load_schemas(self) -> None:
        """Load all event schemas from schema directory."""
        schema_files = [
            "subscription-events.json",
            "config-events.json", 
            "health-events.json"
        ]
        
        for schema_file in schema_files:
            schema_path = self.schema_dir / schema_file
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    schema_name = schema_path.stem
                    self._schemas[schema_name] = json.load(f)
            else:
                logger.warning(f"Schema file not found: {schema_path}")
    
    def validate_event(self, event: Dict[str, Any], schema_name: str) -> bool:
        """Validate event against schema."""
        if schema_name not in self._schemas:
            raise ValueError(f"Schema '{schema_name}' not found")
        
        try:
            jsonschema.validate(event, self._schemas[schema_name])
            return True
        except ValidationError as e:
            raise ValidationError(f"Event validation failed: {e.message}")
    
    def create_event_base(self, 
                         event_type: str, 
                         source: str,
                         correlation_id: Optional[str] = None,
                         metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create base event structure."""
        event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": source,
            "event_type": event_type
        }
        
        if correlation_id:
            event["correlation_id"] = correlation_id
        
        if metadata:
            event["metadata"] = metadata
        
        return event


class SubscriptionEventConverter(EventConverter):
    """Converter for subscription events."""
    
    def create_subscription_created(self,
                                  subscription_data: Dict[str, Any],
                                  source: str = "sboxmgr",
                                  correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create subscription.created event."""
        event = self.create_event_base("subscription.created", source, correlation_id)
        event["data"] = subscription_data
        return event
    
    def create_subscription_updated(self,
                                  subscription_data: Dict[str, Any],
                                  source: str = "sboxmgr",
                                  correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create subscription.updated event."""
        event = self.create_event_base("subscription.updated", source, correlation_id)
        event["data"] = subscription_data
        return event
    
    def create_subscription_deleted(self,
                                  subscription_id: str,
                                  source: str = "sboxmgr",
                                  correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create subscription.deleted event."""
        event = self.create_event_base("subscription.deleted", source, correlation_id)
        event["data"] = {"subscription_id": subscription_id}
        return event
    
    def create_subscription_enabled(self,
                                  subscription_id: str,
                                  source: str = "sboxmgr",
                                  correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create subscription.enabled event."""
        event = self.create_event_base("subscription.enabled", source, correlation_id)
        event["data"] = {"subscription_id": subscription_id}
        return event
    
    def create_subscription_disabled(self,
                                   subscription_id: str,
                                   source: str = "sboxmgr",
                                   correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create subscription.disabled event."""
        event = self.create_event_base("subscription.disabled", source, correlation_id)
        event["data"] = {"subscription_id": subscription_id}
        return event
    
    def create_subscription_update_started(self,
                                         subscription_id: str,
                                         source: str = "sboxagent",
                                         correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create subscription.update_started event."""
        event = self.create_event_base("subscription.update_started", source, correlation_id)
        event["data"] = {"subscription_id": subscription_id}
        return event
    
    def create_subscription_update_completed(self,
                                           subscription_id: str,
                                           status: str,
                                           source: str = "sboxagent",
                                           correlation_id: Optional[str] = None,
                                           error: Optional[str] = None,
                                           nodes_count: Optional[int] = None,
                                           config_changed: Optional[bool] = None) -> Dict[str, Any]:
        """Create subscription.update_completed event."""
        event = self.create_event_base("subscription.update_completed", source, correlation_id)
        event["data"] = {
            "subscription_id": subscription_id,
            "status": status
        }
        
        if error:
            event["data"]["error"] = error
        if nodes_count is not None:
            event["data"]["nodes_count"] = nodes_count
        if config_changed is not None:
            event["data"]["config_changed"] = config_changed
        
        return event


class ConfigEventConverter(EventConverter):
    """Converter for configuration events."""
    
    def create_config_created(self,
                            config_data: Dict[str, Any],
                            source: str = "sboxmgr",
                            correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create config.created event."""
        event = self.create_event_base("config.created", source, correlation_id)
        event["data"] = config_data
        return event
    
    def create_config_updated(self,
                            config_data: Dict[str, Any],
                            source: str = "sboxmgr",
                            correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create config.updated event."""
        event = self.create_event_base("config.updated", source, correlation_id)
        event["data"] = config_data
        return event
    
    def create_config_deleted(self,
                            config_id: str,
                            source: str = "sboxmgr",
                            correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create config.deleted event."""
        event = self.create_event_base("config.deleted", source, correlation_id)
        event["data"] = {"config_id": config_id}
        return event
    
    def create_config_activated(self,
                              config_id: str,
                              previous_config_id: Optional[str] = None,
                              source: str = "sboxagent",
                              correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create config.activated event."""
        event = self.create_event_base("config.activated", source, correlation_id)
        event["data"] = {"config_id": config_id}
        if previous_config_id:
            event["data"]["previous_config_id"] = previous_config_id
        return event
    
    def create_config_reload_requested(self,
                                     config_id: str,
                                     force: bool = False,
                                     source: str = "sboxmgr",
                                     correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Create config.reload_requested event."""
        event = self.create_event_base("config.reload_requested", source, correlation_id)
        event["data"] = {
            "config_id": config_id,
            "force": force
        }
        return event
    
    def create_config_reload_completed(self,
                                     config_id: str,
                                     status: str,
                                     source: str = "sboxagent",
                                     correlation_id: Optional[str] = None,
                                     error: Optional[str] = None,
                                     reload_time_ms: Optional[int] = None) -> Dict[str, Any]:
        """Create config.reload_completed event."""
        event = self.create_event_base("config.reload_completed", source, correlation_id)
        event["data"] = {
            "config_id": config_id,
            "status": status
        }
        
        if error:
            event["data"]["error"] = error
        if reload_time_ms is not None:
            event["data"]["reload_time_ms"] = reload_time_ms
        
        return event


class HealthEventConverter(EventConverter):
    """Converter for health events."""
    
    def create_health_status_changed(self,
                                   component: str,
                                   previous_status: str,
                                   current_status: str,
                                   source: str = "sboxagent",
                                   correlation_id: Optional[str] = None,
                                   message: Optional[str] = None) -> Dict[str, Any]:
        """Create health.status_changed event."""
        event = self.create_event_base("health.status_changed", source, correlation_id)
        event["data"] = {
            "component": component,
            "previous_status": previous_status,
            "current_status": current_status,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        if message:
            event["data"]["message"] = message
        
        return event
    
    def create_health_check_completed(self,
                                    check_id: str,
                                    overall_status: str,
                                    components: List[Dict[str, Any]],
                                    source: str = "sboxagent",
                                    correlation_id: Optional[str] = None,
                                    check_duration_ms: Optional[int] = None,
                                    errors: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create health.check_completed event."""
        event = self.create_event_base("health.check_completed", source, correlation_id)
        event["data"] = {
            "check_id": check_id,
            "overall_status": overall_status,
            "components": components
        }
        
        if check_duration_ms is not None:
            event["data"]["check_duration_ms"] = check_duration_ms
        if errors:
            event["data"]["errors"] = errors
        
        return event
    
    def create_health_alert_triggered(self,
                                    alert_id: str,
                                    severity: str,
                                    message: str,
                                    component: str,
                                    source: str = "sboxagent",
                                    correlation_id: Optional[str] = None,
                                    threshold: Optional[Dict[str, Any]] = None,
                                    current_value: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create health.alert_triggered event."""
        event = self.create_event_base("health.alert_triggered", source, correlation_id)
        event["data"] = {
            "alert_id": alert_id,
            "severity": severity,
            "message": message,
            "component": component,
            "acknowledged": False
        }
        
        if threshold:
            event["data"]["threshold"] = threshold
        if current_value:
            event["data"]["current_value"] = current_value
        
        return event


# Convenience function to get all converters
def get_event_converters(schema_dir: Optional[Path] = None) -> Dict[str, EventConverter]:
    """Get all event converters."""
    return {
        "subscription": SubscriptionEventConverter(schema_dir),
        "config": ConfigEventConverter(schema_dir),
        "health": HealthEventConverter(schema_dir)
    } 