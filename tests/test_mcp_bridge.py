from mcp.types import CallToolResult, TextContent, Tool
from mcp_bridge import mcp_tool_to_ollama, tool_result_text

def test_mcp_tool_to_ollama_converts_schema():
    tool = Tool(
        name='get_weather',
        description='Get current weather for a given city',
        inputSchema={
            'type': 'object',
            'properties': {
                'city': {'type': 'string'}
            },
            'required': ['city']
        }
    )
    converted_tool = mcp_tool_to_ollama(tool)
    assert converted_tool == {
        'type': 'function',
        'function': {
            'name': 'get_weather',
            'description': 'Get current weather for a given city',
            'parameters': {
                'type': 'object',
                'properties': {'city': {'type': 'string'}},
                'required': ['city']
            }
        }
    }

def test_tool_result_text_joins_text_blocks():
    result = CallToolResult(content=[
        TextContent(type='text', text='Weather in London: 15C'),
    ])
    assert tool_result_text(result) == 'Weather in London: 15C'