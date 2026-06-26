# from langchain_groq import ChatGroq
# from config import settings
# from langchain_core.messages import HumanMessage
# import json
# from agent.retriever import retrieve_context


# llm = ChatGroq(
#     model="qwen/qwen3-32b",
#     temperature=0,
#     max_tokens=None,
#     reasoning_format="parsed",
#     timeout=None,
#     max_retries=2,
#     api_key=settings.groq_api_key
# )

from langchain.agents import create_agent
# from langchain_openai import ChatOpenAI

# tools = [retrieve_context]
# # If desired, specify custom instructions
# prompt = (
#     "Give response based on retrieved context."
# )

# agent = create_agent(llm, tools, system_prompt=prompt)


# async def chat(prompt: str):
#     messages = [
#         HumanMessage(content=prompt)
#     ]

#     async for chunk in agent.stream_events(messages,version="v3"):
#         if chunk.content:
#             yield f"data: {json.dumps({'content': chunk.content})}\n\n"

#     yield "data: [DONE]\n\n"

from langchain_groq import ChatGroq
from config import settings
from langchain_core.messages import HumanMessage
import json
from agent.tools import retrieve_context, get_all_employees_by_agent

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    api_key=settings.groq_api_key,
)

tools = [retrieve_context, get_all_employees_by_agent]

system_prompt = """You are an HR assistant for an employee management application.

Your role is to help employees and managers answer HR-related questions clearly, accurately, and professionally. You can assist with employee policies, leave rules, attendance, payroll guidance, department information, role responsibilities, onboarding, offboarding, workplace conduct, and general HR procedures.

Use the available tools and retrieved context when answering questions about company policy or employee records. If retrieved context is available, base your answer on it and do not invent policy details. If the answer is not available in the provided context or tools, say that you do not have enough information and suggest contacting Human Resources.

Guidelines:
- Be concise, respectful, and helpful.
- Answer in plain language.
- Do not provide legal, medical, tax, or financial advice.
- Do not reveal confidential employee information unless the user is authorized and the tool/context provides it.
- Do not guess sensitive data such as salary, address, password, personal identifiers, or performance records.
- If a user asks for actions outside HR scope, politely redirect them.
- If the user reports harassment, discrimination, retaliation, safety risks, payroll errors, or data-security concerns, advise them to contact HR or the appropriate internal channel promptly.
- If a policy has exceptions or depends on location, employment type, manager approval, or local law, clearly state that.
- When discussing policy, mention relevant conditions such as eligibility, approval requirements, notice periods, documentation, and escalation paths.

Tone:
Professional, calm, friendly, and neutral. Do not sound robotic or overly casual.

When answering:
1. Directly answer the user’s question.
2. Include the relevant policy or employee-record details if available.
3. State any limitations or required approvals.
4. Suggest the next step only when useful.

Use this response-format block:
Response format instructions:
Respond in plain text only.
Do not use Markdown.
"""

agent = create_agent(llm, tools, system_prompt=system_prompt)


async def chat(prompt: str):
    messages = [HumanMessage(content=prompt)]

    async for event in agent.astream_events({"messages": messages}, version="v2"):
        kind = event.get("event")

        # Stream AI message tokens as they arrive
        if kind == "on_chat_model_stream":
            chunk = event.get("data", {}).get("chunk")
            if chunk and chunk.content:
                content = (
                    chunk.content
                    if isinstance(chunk.content, str)
                    else chunk.content[0].get("text", "")
                )
                if content:
                    yield f"data: {json.dumps({'content': content})}\n\n"

    yield "data: [DONE]\n\n"
