#!/usr/bin/env python3
"""
Schema validation test script for subbox-common
Tests YAML configuration against JSON schemas
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any

try:
    import jsonschema
    import yaml
except ImportError as e:
    print(f"Missing required packages: {e}")
    print("Install with: pip install jsonschema pyyaml")
    sys.exit(1)


def load_json_schema(schema_path: str) -> Dict[str, Any]:
    """Load JSON schema from file"""
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading schema {schema_path}: {e}")
        sys.exit(1)


def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """Load YAML configuration from file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config {config_path}: {e}")
        sys.exit(1)


def validate_config(config_data: Dict[str, Any], schema: Dict[str, Any], config_name: str) -> bool:
    """Validate configuration against schema"""
    try:
        # Use Draft202012Validator for better default handling
        validator = jsonschema.Draft202012Validator(schema)
        
        # Validate with defaults
        errors = list(validator.iter_errors(config_data))
        
        if errors:
            print(f"❌ Validation failed for {config_name}:")
            for error in errors:
                print(f"  - {error.message} at {' -> '.join(str(p) for p in error.path)}")
            return False
        else:
            print(f"✅ Validation passed for {config_name}")
            return True
            
    except Exception as e:
        print(f"❌ Validation error for {config_name}: {e}")
        return False


def main():
    """Main validation function"""
    print("🧪 Subbox Schema Validation Test")
    print("=" * 40)
    
    # Get script directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Test agent_config schema
    schema_path = project_root / "schemas" / "agent_config.schema.json"
    config_path = project_root / "examples" / "agent_config.yaml"
    
    if not schema_path.exists():
        print(f"❌ Schema not found: {schema_path}")
        sys.exit(1)
    
    if not config_path.exists():
        print(f"❌ Config example not found: {config_path}")
        sys.exit(1)
    
    print(f"📋 Testing schema: {schema_path.name}")
    print(f"📄 Testing config: {config_path.name}")
    print()
    
    # Load schema and config
    schema = load_json_schema(str(schema_path))
    config = load_yaml_config(str(config_path))
    
    # Validate
    success = validate_config(config, schema, "agent_config.yaml")
    
    # Test API schema if available
    api_schema_path = project_root / "protocols" / "api.schema.json"
    if api_schema_path.exists():
        print()
        print(f"📋 Testing API schema: {api_schema_path.name}")
        
        api_schema = load_json_schema(str(api_schema_path))
        
        # Test a sample API request
        sample_request = {
            "trace_id": "b0f4d6a0-f309-44f4-900e-9df0bcb2a755",
            "timestamp": "2025-06-27T10:30:00Z",
            "action": "update_config",
            "protocol_version": "1.0.0",
            "config": config
        }
        
        # Extract the update_config request schema
        request_schema = api_schema["properties"]["requests"]["properties"]["update_config"]
        success_api = validate_config(sample_request, request_schema, "API update_config request")
        success = success and success_api
    
    print()
    if success:
        print("🎉 All validations passed!")
        sys.exit(0)
    else:
        print("💥 Some validations failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 