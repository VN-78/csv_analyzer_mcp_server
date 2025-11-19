#region imports
from mcp.server.fastmcp import FastMCP
from analyze_csv_tool import analyze_csv
from read_csv_tool import read_csv
#endregion

"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

#region Initialize
# Create an MCP server
mcp = FastMCP(
    name = "Sample_mcp_add",
    host = "localhost", # only use for SSE or Streamable HTTP 
    port = 8050
)
#endregion

#region tools
# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def print_name(name:str) -> None:
    """Print the Name with Hello World"""
    print(name + "hello world")

# Register the CSV analysis tool from analyze_csv_tool.py
# Wrap the imported function with the @mcp.tool() decorator
@mcp.tool()
def analyze_csv_data(file_path: str, analysis_type: str = "comprehensive") -> str:
    """
    Performs comprehensive data analysis on a CSV file, similar to Claude's data analysis tool.
    Generates statistical summaries, data quality checks, correlation analysis, and actionable insights.

    Use when the user wants to:
    - Understand their dataset
    - Get insights and overview of CSV data
    - Perform exploratory data analysis (EDA)
    - Check data quality and issues
    - Find patterns and correlations

    Example queries:
    - 'analyze data.csv'
    - 'give me insights on sales.csv'
    - 'perform data analysis on dataset.csv'
    - 'what are the patterns in customer_data.csv'

    Args:
        file_path: Path to the CSV file to analyze (ask user if not specified)
        analysis_type: Type of analysis to perform:
            - "comprehensive" (default): Full analysis with all sections
            - "quick": Overview and basic statistics only
            - "quality": Focus on data quality issues
            - "statistical": Detailed statistical analysis
            - "correlation": Focus on relationships between variables

    Returns:
        str: Comprehensive analysis report with insights and recommendations
    """
    return analyze_csv(file_path, analysis_type)


@mcp.tool()
def read_csv_data(file_path: str) -> str:
    """
    Reads an Csv file and returns its contents
    Use When analyzing an csv file or reading an csv file 
    Examples : 'Read sample.csv' , 'Whats in sample.csv' , 'what is in the csv file'
    Args:
        file_path: path to the csv file , ask the user if not specified 
        
    Returns:
        str: contents of the csv file and file info and summary
    """
    return read_csv(file_path)
#endregion

#region resources
# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
#endregion

#region prompts
# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."
#endregion





if __name__ == "__main__":
    mcp.run(transport="streamable-http")