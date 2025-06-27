#!/usr/bin/env python3
"""
Subbox Common CLI utility
Provides validation and management tools for subbox schemas and configurations
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import jsonschema
    import yaml
except ImportError as e:
    print(f"Missing required packages: {e}")
    print("Install with: pip install jsonschema pyyaml")
    sys.exit(1)


class SubboxValidator:
    """Subbox schema validator"""
    
    def __init__(self, schemas_dir: str = "schemas"):
        self.schemas_dir = Path(schemas_dir)
        self.schemas = {}
        self._load_schemas()
    
    def _load_schemas(self):
        """Load all JSON schemas from schemas directory"""
        if not self.schemas_dir.exists():
            print(f"Warning: Schemas directory {self.schemas_dir} not found")
            return
        
        for schema_file in self.schemas_dir.glob("*.json"):
            try:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema = json.load(f)
                    schema_name = schema_file.stem
                    self.schemas[schema_name] = schema
                    print(f"Loaded schema: {schema_name}")
            except Exception as e:
                print(f"Error loading schema {schema_file}: {e}")
    
    def validate_config(self, config_path: str, schema_name: str = "agent_config") -> bool:
        """Validate configuration file against schema"""
        if schema_name not in self.schemas:
            print(f"Schema '{schema_name}' not found")
            return False
        
        config_path = Path(config_path)
        if not config_path.exists():
            print(f"Config file {config_path} not found")
            return False
        
        try:
            # Load config based on file extension
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
            elif config_path.suffix.lower() == '.json':
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            else:
                print(f"Unsupported file format: {config_path.suffix}")
                return False
            
            # Validate
            schema = self.schemas[schema_name]
            validator = jsonschema.Draft202012Validator(schema)
            errors = list(validator.iter_errors(config_data))
            
            if errors:
                print(f"❌ Validation failed for {config_path.name}:")
                for error in errors:
                    path = ' -> '.join(str(p) for p in error.path) if error.path else 'root'
                    print(f"  - {error.message} at {path}")
                return False
            else:
                print(f"✅ Validation passed for {config_path.name}")
                return True
                
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False
    
    def list_schemas(self):
        """List available schemas"""
        if not self.schemas:
            print("No schemas loaded")
            return
        
        print("Available schemas:")
        for name, schema in self.schemas.items():
            version = schema.get('version', 'unknown')
            title = schema.get('title', name)
            print(f"  - {name} (v{version}): {title}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Subbox Common CLI - Schema validation and management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  subbox-common verify agent_config.yaml
  subbox-common verify config.json --schema agent_config
  subbox-common list-schemas
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify configuration against schema')
    verify_parser.add_argument('config_file', help='Configuration file to validate')
    verify_parser.add_argument('--schema', default='agent_config', 
                              help='Schema name to use (default: agent_config)')
    verify_parser.add_argument('--schemas-dir', default='schemas',
                              help='Directory containing schemas (default: schemas)')
    
    # List schemas command
    list_parser = subparsers.add_parser('list-schemas', help='List available schemas')
    list_parser.add_argument('--schemas-dir', default='schemas',
                            help='Directory containing schemas (default: schemas)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize validator
    validator = SubboxValidator(args.schemas_dir)
    
    if args.command == 'verify':
        success = validator.validate_config(args.config_file, args.schema)
        sys.exit(0 if success else 1)
    
    elif args.command == 'list-schemas':
        validator.list_schemas()


if __name__ == "__main__":
    main() 