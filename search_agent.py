from tools import search_tavily, search_wiki, search_ddgs, arxiv_search
from schema import ResearchState, ResearchPlan
from typing import Literal
from utils import fetch_page
from langchain_core.prompts import ChatPromptTemplate
from prompts import PLANNING_PROMPT, SYNTHESIS_PROMPT
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
import asyncio
import aiohttp



# =========================
# MODELS
# =========================

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4,
    max_tokens=1000,
    max_retries=3
)

planner = (
    ChatPromptTemplate.from_messages(PLANNING_PROMPT)
    | model.with_structured_output(ResearchPlan)
)

synthesizer = (
    ChatPromptTemplate.from_messages(SYNTHESIS_PROMPT)
    | model
)

search_tools = [
    search_tavily,
    search_ddgs,
    search_wiki,
    arxiv_search
]



async def call_search_tools(query: str):
    async def run_tool(tool):
        result = tool.invoke(query)
        if asyncio.iscoroutine(result):
            return await result
        return result

    results = await asyncio.gather(
        *(run_tool(tool) for tool in search_tools),
        return_exceptions=True
    )

    texts, urls = [], []

    for res in results:
        if isinstance(res, Exception):
            continue
        t, u = res
        texts.extend(t)
        urls.extend(u)

    return texts, urls



# =========================
# NODES
# =========================

def plan_node(state: ResearchState) -> ResearchState:
    plan: ResearchPlan = planner.invoke({
        "topic": state.topic,
        "mode": state.mode
    })

    state.plan = plan.subtopics
    state.remaining_subtopics = plan.subtopics.copy()
    state.max_depth = plan.depth_required
    return state


async def search_node(state: ResearchState) -> ResearchState:
    if not state.remaining_subtopics:
        return state

    state.depth += 1
    subtopic = state.remaining_subtopics.pop(0)

    _, urls = await call_search_tools(subtopic)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

        for res in results:
            if res:
                state.extracted_notes.append(res)

    return state


async def validate_node(state: ResearchState) -> ResearchState:
    seen = set()

    for url, note in state.extracted_notes:
        if note not in seen:
            seen.add(note)
            state.validated_notes.append(note)
            state.validated_sources.append(url)

    return state


async def synthesize_node(state: ResearchState) -> ResearchState:
    notes = "\n\n".join(
        f"- {note[:1000]}" for note in state.validated_notes
    )

    references = "\n".join(
        f"- {src}" for src in state.validated_sources
    )

    response = await synthesizer.ainvoke({
        "topic": state.topic,
        "validated_notes": notes,
        "validated_sources": references
    })

    state.final_report = response.content
    return state


# =========================
# ROUTER
# =========================

def should_continue(state: ResearchState) -> bool:
    return (
        state.depth < state.max_depth
        and len(state.remaining_subtopics) > 0
    )


# =========================
# GRAPH
# =========================
def create_graph_agent():
    graph = StateGraph(ResearchState)

    graph.add_node("plan", plan_node)
    graph.add_node("search", search_node)
    graph.add_node("validate", validate_node)
    graph.add_node("synthesize", synthesize_node)

    graph.set_entry_point("plan")

    graph.add_edge("plan", "search")
    graph.add_edge("search", "validate")

    graph.add_conditional_edges(
        "validate",
        should_continue,
        {
            True: "search",
            False: "synthesize"
        }
    )

    graph.add_edge("synthesize", END)

    return graph.compile()



# =========================
# RUNNER
# =========================
research_agent = create_graph_agent()


async def main(query: str, mode: Literal['shallow','deep']):
    state = ResearchState(
        topic=query,
        mode=mode
    )
    async for event in research_agent.astream(state):
        print('***'*60)
        print('\n')
        print(event)
        print('\n')
        print('***'*60)
        
    return state
        
        


if __name__ == "__main__":
    asyncio.run(main(query = 'Neural Networks', mode='shallow'))
