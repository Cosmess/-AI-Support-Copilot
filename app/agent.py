from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from app.config import settings
from app.tools import find_ticket, search_logs, suggest_priority


@tool
def tool_find_ticket(ticket_id: str) -> str:
    """Consulta um ticket pelo ID."""
    return find_ticket(ticket_id)


@tool
def tool_search_logs(keyword: str) -> str:
    """Busca pistas em logs por palavra-chave."""
    return search_logs(keyword)


@tool
def tool_suggest_priority(impact: str) -> str:
    """Sugere prioridade de atendimento."""
    return suggest_priority(impact)


def create_support_agent() -> AgentExecutor:
    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )
    tools = [tool_find_ticket, tool_search_logs, tool_suggest_priority]
    prompt = PromptTemplate.from_template(
        """Você é um copiloto técnico de suporte.
Use as ferramentas para investigar antes de responder.

Você deve seguir este formato:
Question: pergunta do usuário
Thought: raciocínio
Action: uma das ferramentas [{tool_names}]
Action Input: entrada da ferramenta
Observation: saída da ferramenta
... (repete Thought/Action/Action Input/Observation se necessário)
Thought: já tenho evidências suficientes
Final Answer: resposta final com diagnóstico, evidências e próximos passos

Ferramentas disponíveis:
{tools}

Question: {input}
Thought:{agent_scratchpad}"""
    )
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False, handle_parsing_errors=True)
