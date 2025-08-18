from typing import TypedDict
from langgraph.graph import StateGraph, END
import os

class AgentState(TypedDict):
    input: str
    output: str
    agent_type: str

def green_hill_agent(state: AgentState):
    """Simple Green Hill Cannabis Agent"""
    input_text = state.get("input", "")
    agent_type = state.get("agent_type", "Strategy")
    
    # Simulated response for demo
    responses = {
        "Strategy": f"Strategic analysis for Green Hill Canarias: {input_text}. Focus on EU-GMP compliance and market expansion in Canary Islands.",
        "Finance": f"Financial analysis: {input_text}. CAPEX requirements and ROI projections for cannabis operations.",
        "Operations": f"Operations review: {input_text}. Production planning and facility management for medicinal cannabis.",
        "Market": f"Market intelligence: {input_text}. European cannabis market opportunities and competitive analysis.",
        "Risk": f"Risk assessment: {input_text}. Regulatory and operational risks in Spanish/EU cannabis sector.",
        "Compliance": f"Compliance review: {input_text}. AEMPS regulations and EU-GMP requirements analysis.",
        "Innovation": f"Innovation opportunities: {input_text}. R&D and technology advancement in cannabis sector."
    }
    
    response = responses.get(agent_type, f"Green Hill agent response: {input_text}")
    
    return {
        "input": input_text,
        "output": response,
        "agent_type": agent_type
    }

# BUILD GRAPH
workflow = StateGraph(AgentState)
workflow.add_node("agent", green_hill_agent)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

graph = workflow.compile()
