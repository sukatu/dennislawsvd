#!/usr/bin/env python3
"""
API Documentation Generator for Juridence Legal Database System
Generates comprehensive API documentation from FastAPI routes
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import inspect
import re

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent))

def extract_route_info(route) -> Dict[str, Any]:
    """Extract information from a FastAPI route"""
    info = {
        'path': route.path,
        'methods': list(route.methods),
        'name': route.name,
        'summary': '',
        'description': '',
        'parameters': [],
        'request_body': None,
        'responses': {},
        'tags': []
    }
    
    # Get route function
    if hasattr(route, 'endpoint'):
        func = route.endpoint
        if hasattr(func, '__wrapped__'):
            func = func.__wrapped__
        
        # Extract docstring
        if func.__doc__:
            docstring = func.__doc__.strip()
            lines = docstring.split('\n')
            info['summary'] = lines[0] if lines else ''
            if len(lines) > 1:
                info['description'] = '\n'.join(lines[1:]).strip()
        
        # Extract function signature for parameters
        try:
            sig = inspect.signature(func)
            for param_name, param in sig.parameters.items():
                if param_name not in ['self', 'db', 'current_user']:
                    # Handle default values that might not be JSON serializable
                    default_value = None
                    if param.default != inspect.Parameter.empty:
                        try:
                            # Try to serialize the default value
                            json.dumps(param.default)
                            default_value = param.default
                        except (TypeError, ValueError):
                            # If not serializable, convert to string
                            default_value = str(param.default)
                    
                    param_info = {
                        'name': param_name,
                        'type': str(param.annotation) if param.annotation != inspect.Parameter.empty else 'Any',
                        'required': param.default == inspect.Parameter.empty,
                        'default': default_value
                    }
                    info['parameters'].append(param_info)
        except (ValueError, TypeError):
            # Skip if signature extraction fails
            pass
    
    return info

def generate_api_documentation() -> Dict[str, Any]:
    """Generate comprehensive API documentation"""
    
    # Import FastAPI app
    try:
        from main import app
    except ImportError:
        print("Error: Could not import FastAPI app. Make sure you're in the backend directory.")
        return {}
    
    docs = {
        'title': 'Juridence Legal Database API',
        'version': '1.0.0',
        'description': 'Comprehensive API for the Juridence Legal Database System',
        'base_url': 'https://api.juridence.com',
        'authentication': {
            'type': 'Bearer Token',
            'description': 'Include your API key in the Authorization header',
            'example': 'Authorization: Bearer your-api-key-here'
        },
        'rate_limits': {
            'free': '100 requests/hour',
            'professional': '1,000 requests/hour',
            'enterprise': '10,000 requests/hour'
        },
        'endpoints': {}
    }
    
    # Group endpoints by tags
    endpoints_by_tag = {}
    
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            route_info = extract_route_info(route)
            
            # Get tags from route
            tags = getattr(route, 'tags', ['general'])
            if not tags:
                tags = ['general']
            
            for tag in tags:
                if tag not in endpoints_by_tag:
                    endpoints_by_tag[tag] = []
                endpoints_by_tag[tag].append(route_info)
    
    # Organize endpoints
    docs['endpoints'] = endpoints_by_tag
    
    return docs

def generate_markdown_docs(docs: Dict[str, Any]) -> str:
    """Generate Markdown documentation"""
    
    md = f"""# {docs['title']} v{docs['version']}

{docs['description']}

## Base URL
```
{docs['base_url']}
```

## Authentication
{docs['authentication']['description']}

```
{docs['authentication']['example']}
```

## Rate Limits
- **Free Tier**: {docs['rate_limits']['free']}
- **Professional**: {docs['rate_limits']['professional']}
- **Enterprise**: {docs['rate_limits']['enterprise']}

## API Endpoints

"""
    
    for tag, endpoints in docs['endpoints'].items():
        md += f"### {tag.title()}\n\n"
        
        for endpoint in endpoints:
            methods = ', '.join(endpoint['methods'])
            md += f"#### {methods} {endpoint['path']}\n\n"
            
            if endpoint['summary']:
                md += f"**{endpoint['summary']}**\n\n"
            
            if endpoint['description']:
                md += f"{endpoint['description']}\n\n"
            
            if endpoint['parameters']:
                md += "**Parameters:**\n\n"
                for param in endpoint['parameters']:
                    required = "✓" if param['required'] else "○"
                    default = f" (default: {param['default']})" if param['default'] is not None else ""
                    md += f"- `{param['name']}` ({param['type']}) {required}{default}\n"
                md += "\n"
            
            md += "---\n\n"
    
    return md

def main():
    """Main function to generate API documentation"""
    print("Generating API documentation...")
    
    # Generate documentation
    docs = generate_api_documentation()
    
    if not docs:
        print("Failed to generate documentation")
        return
    
    # Save JSON documentation
    json_file = Path(__file__).parent / 'api_documentation.json'
    with open(json_file, 'w') as f:
        json.dump(docs, f, indent=2)
    print(f"JSON documentation saved to: {json_file}")
    
    # Save Markdown documentation
    md_file = Path(__file__).parent / 'API_DOCUMENTATION.md'
    with open(md_file, 'w') as f:
        f.write(generate_markdown_docs(docs))
    print(f"Markdown documentation saved to: {md_file}")
    
    # Print summary
    total_endpoints = sum(len(endpoints) for endpoints in docs['endpoints'].values())
    print(f"\nDocumentation generated successfully!")
    print(f"Total endpoints documented: {total_endpoints}")
    print(f"Tags: {', '.join(docs['endpoints'].keys())}")

if __name__ == "__main__":
    main()
