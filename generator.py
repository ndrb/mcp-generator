import yaml
import json
import os
import sys
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any, List
import re

def convert_type_to_python(openapi_type: str, format_: str = None, items: Dict = None) -> str:
    """Convert OpenAPI types to Python types."""
    if openapi_type == "integer":
        return "int"
    elif openapi_type == "number":
        return "float"
    elif openapi_type == "boolean":
        return "bool"
    elif openapi_type == "string":
        if format_ == "date-time":
            return "datetime.datetime"
        elif format_ == "date":
            return "datetime.date"
        return "str"
    elif openapi_type == "array":
        if items and 'type' in items:
            item_type = convert_type_to_python(items['type'], items.get('format'), items.get('items'))
            return f"List[{item_type}]"
        return "List[Any]"
    elif openapi_type == "object":
        return "Dict[str, Any]"
    return "Any"

def parse_openapi_spec(spec_path: str) -> Dict[str, Any]:
    """Parse OpenAPI spec and extract models."""
    with open(spec_path, 'r') as f:
        spec = yaml.safe_load(f)
    
    models = {}
    
    # Extract components/schemas as models
    if 'components' in spec and 'schemas' in spec['components']:
        for model_name, schema in spec['components']['schemas'].items():
            properties = schema.get('properties', {})
            model_def = {
                'properties': {},
                'required': schema.get('required', [])
            }
            
            for prop_name, prop_def in properties.items():
                prop_type = prop_def.get('type', 'string')
                prop_format = prop_def.get('format')
                prop_items = prop_def.get('items')
                
                model_def['properties'][prop_name] = {
                    'type': prop_type,
                    'py_type': convert_type_to_python(prop_type, prop_format, prop_items),
                    'description': prop_def.get('description', ''),
                }
                
                if 'enum' in prop_def:
                    model_def['properties'][prop_name]['enum'] = prop_def['enum']
            
            models[model_name] = model_def
    
    # Extract API info
    api_info = {
        'title': spec.get('info', {}).get('title', 'API'),
        'version': spec.get('info', {}).get('version', '1.0.0'),
        'description': spec.get('info', {}).get('description', ''),
    }
    
    # Extract security schemes
    security_schemes = {}
    if 'components' in spec and 'securitySchemes' in spec['components']:
        for scheme_name, scheme_def in spec['components']['securitySchemes'].items():
            if scheme_def.get('type') == 'apiKey':
                security_schemes[scheme_name] = {
                    'type': 'apiKey',
                    'name': scheme_def.get('name', 'X-API-Key'),
                    'in': scheme_def.get('in', 'header')
                }
            elif scheme_def.get('type') == 'http' and scheme_def.get('scheme') == 'bearer':
                security_schemes[scheme_name] = {
                    'type': 'bearer',
                    'name': 'Authorization',
                    'in': 'header'
                }
    
    # Extract servers
    servers = []
    if 'servers' in spec:
        for server in spec['servers']:
            servers.append({
                'url': server.get('url', ''),
                'description': server.get('description', '')
            })
    
    return {
        'models': models,
        'api_info': api_info,
        'security_schemes': security_schemes,
        'servers': servers
    }

def get_api_name_from_spec(spec_path: str) -> str:
    """Extract API name from spec file or path."""
    # Try to get from file name first
    file_name = os.path.basename(spec_path)
    name_match = re.match(r'(.+)\.(yaml|json)$', file_name)
    if name_match:
        return name_match.group(1).lower()
    
    # If not possible, try to get from spec content
    try:
        with open(spec_path, 'r') as f:
            spec = yaml.safe_load(f)
            if 'info' in spec and 'title' in spec['info']:
                # Convert title to snake_case
                title = spec['info']['title']
                return re.sub(r'[^a-zA-Z0-9]', '_', title).lower()
    except:
        pass
    
    # Default fallback
    return "api"

def generate_mcp_server(spec_path: str, output_path: str = None):
    """Generate MCP server from OpenAPI spec."""
    # Parse OpenAPI spec
    context = parse_openapi_spec(spec_path)
    
    # Get API name if output_path is not specified
    if not output_path:
        api_name = get_api_name_from_spec(spec_path)
        output_path = f"mcp_server_{api_name}.py"
    
    # Set up Jinja environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('mcp_server.py.j2')
    
    # Render template
    output = template.render(**context)
    
    # Write output
    with open(output_path, 'w') as f:
        f.write(output)
    
    print(f"Generated MCP server at {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generator.py <openapi_spec.yaml> [output.py]")
        sys.exit(1)
    
    spec_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    generate_mcp_server(spec_path, output_path)