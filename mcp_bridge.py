def mcp_tool_to_ollama(tool):
    return {
        'type': 'function',
        'function': {
            'name': tool.name,
            'description': tool.description,
            'parameters': tool.input_schema,
        }
    }