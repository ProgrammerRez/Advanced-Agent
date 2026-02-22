from langchain_core.tools import tool
from langchain_community.retrievers import WikipediaRetriever, ArxivRetriever
from langchain_community.tools import DuckDuckGoSearchResults, TavilySearchResults
from dotenv import load_dotenv
import re

load_dotenv()

# 1. Tool Definitions with optimized docstrings for 2026 LLMs
wiki = WikipediaRetriever(top_k_results=2)
arxiv = ArxivRetriever(top_k_results=2)
ddgs = DuckDuckGoSearchResults()
tav = TavilySearchResults(max_results=3)

pattern = r"snippet: (.*?), title: (.*?), link: (.*?)(?=, snippet: |$)"

@tool
def search_wiki(query: str):
    """Useful for general knowledge and history. Input: a search string."""
    result = wiki.invoke(input=query)

    content = [str(res.metadata.get('summary'))[:1000] for res in result]
    url = [res.metadata.get('source') for res in result]
    
    return content, url
    

@tool
def arxiv_search(query: str):
    """Searches and parses research papers on Arxiv"""
    result = arxiv.invoke(input=query)
    content = [res.page_content[:1000] for res in result]
    url = [res.metadata['Entry ID'] for res in result]
    
    return content, url

@tool
def search_ddgs(query: str):
    """Searches DuckDuckGo to search for a specific topic with sources"""
    text = ddgs.invoke(input=query)
    matches = re.findall(pattern, text)
    snippet = [m[0][:1000] for m in matches]
    url = [m[2] for m in matches]
    
    return snippet, url
@tool
def search_tavily(query: str):
    """Can generaly search the web for anything. Use for deep search or intensive tasks"""
    results = tav.invoke(input=query)
    urls = [res['url'] for res in results]
    content = [res['content'][:500] for res in results]
    return content, urls

@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.

    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.

    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?

    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps

    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"
