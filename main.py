from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
import os

class State(TypedDict):
    messages: Annotated[list, add_messages]
    agent: str

def call_agent(state: State):
    agent = state.get("agent", "Strategy")
    messages = state.get("messages", [])
    if not messages:
        return {"messages": [{"role": "assistant", "content": "No messages to process"}]}
    last_message = messages[-1]["content"]
    if agent == "ghc_dt":
        from agents.ghc_dt import run_ghc_dt
        result = run_ghc_dt(last_message, state)
        return {"messages": [{"role": "assistant", "content": result["answer"]}]}
    else:
        import openai
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            return {"messages": [{"role": "assistant", "content": "❌ OpenAI API key not configured"}]}
        client = openai.OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a {agent} specialist for Green Hill Canarias cannabis operations."},
                {"role": "user", "content": last_message}
            ],
            max_tokens=1000
        )
        return {
            "messages": [{
                "role": "assistant", 
                "content": f"✅ {agent}: {response.choices[0].message.content}"
            }]
        }

# BUILD GRAPH
workflow = StateGraph(State)
workflow.add_node("agent", call_agent)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

app = workflow.compile()
