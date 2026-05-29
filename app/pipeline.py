from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from app.config import settings
from app.knowledge_base import build_or_load_vectorstore
from app.agent import create_support_agent


class CopilotState(TypedDict):
    question: str
    context: str
    agent_output: str
    final_answer: str


vectorstore = build_or_load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
agent_executor = create_support_agent()
llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0)


def retrieve_context(state: CopilotState) -> CopilotState:
    docs = retriever.invoke(state["question"])
    context = "\n\n".join(d.page_content for d in docs)
    return {**state, "context": context}


def investigate_with_agent(state: CopilotState) -> CopilotState:
    result = agent_executor.invoke({"input": state["question"]})
    return {**state, "agent_output": result["output"]}


def generate_answer(state: CopilotState) -> CopilotState:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Você é um analista de suporte sênior. Responda com objetividade."),
            (
                "human",
                """Pergunta:
{question}

Contexto RAG:
{context}

Resultado da investigação do agente:
{agent_output}

Escreva:
1) Diagnóstico provável
2) Evidências
3) Próximos passos""",
            ),
        ]
    )
    chain = prompt | llm
    output = chain.invoke(
        {
            "question": state["question"],
            "context": state["context"],
            "agent_output": state["agent_output"],
        }
    )
    return {**state, "final_answer": output.content}


graph = StateGraph(CopilotState)
graph.add_node("retrieve_context", retrieve_context)
graph.add_node("investigate_with_agent", investigate_with_agent)
graph.add_node("generate_answer", generate_answer)
graph.set_entry_point("retrieve_context")
graph.add_edge("retrieve_context", "investigate_with_agent")
graph.add_edge("investigate_with_agent", "generate_answer")
graph.add_edge("generate_answer", END)
copilot_graph = graph.compile()


def run_copilot(question: str) -> dict:
    initial_state: CopilotState = {
        "question": question,
        "context": "",
        "agent_output": "",
        "final_answer": "",
    }
    result = copilot_graph.invoke(initial_state)
    return result
