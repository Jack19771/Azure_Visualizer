# Azure Terraform Complete Schemas

## Overview
Complete schemas for all Azure Terraform resources extracted from the official provider.

## Details
- **Provider Version**: 3.116.0
- **Total Resources**: 1108
- **Extracted**: 2025-08-28 16:34:52
- **Extractor**: Robust Schema Extractor v1.0

## Files
- `azure_complete_schema.json` - Full provider schema with metadata
- `azure_resources_formatted.json` - All resources in readable format
- `statistics.json` - Analysis and statistics
- `all_resource_names.txt` - Simple list of all resource names
- `individual_resources/` - Each resource in separate file (optional)

## Usage
Load `azure_resources_formatted.json` in your application to access all resource schemas.

```python
import json
with open('azure_resources_formatted.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    resources = data['resources']
    print(f"Available resources: {len(resources)}")
```
