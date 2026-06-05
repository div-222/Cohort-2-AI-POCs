from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider


def build_ollama_model() -> OpenAIChatModel:
	"""Create one shared Ollama-backed model config for all demos."""
	client = AsyncOpenAI(
		base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
		api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
	)

	return OpenAIChatModel(
		model_name=os.getenv("OLLAMA_MODEL", "qwen3.5:4b"),
		provider=OpenAIProvider(openai_client=client),
	)


MODEL = build_ollama_model()


def run_case(title: str, func) -> None:
	print(f"\n{'=' * 20} {title} {'=' * 20}")
	try:
		func()
	except Exception as exc:
		print(f"Case failed: {exc}")


def case_1_basic_chat() -> None:
	"""Use case 1: Basic prompt -> text output."""
	agent = Agent(
		MODEL,
		system_prompt="You are a concise Python mentor. Keep answers to 2-3 lines.",
	)
	result = agent.run_sync("Explain what an AI agent is in simple words.")
	print(result.output)


def case_2_tool_plain() -> None:
	"""Use case 2: Plain function tools (`tool_plain`)."""
	calc_agent = Agent(MODEL, system_prompt="Use tools for calculations whenever possible.")

	@calc_agent.tool_plain
	def add(a: int, b: int) -> int:
		return a + b

	@calc_agent.tool_plain
	def multiply(a: int, b: int) -> int:
		return a * b

	result = calc_agent.run_sync("Add 35 and 7, then multiply the result by 2.")
	print(result.output)


class LeaveDecision(BaseModel):
	approved: bool = Field(description="Whether leave is approved")
	reason: str = Field(description="One-line explanation")
	risk_level: Literal["low", "medium", "high"] = Field(description="Business impact")


def case_3_structured_output() -> None:
	"""Use case 3: Typed/validated output with `output_type`."""
	policy_agent = Agent(
		MODEL,
		output_type=LeaveDecision,
		system_prompt=(
			"You are an HR policy bot. Return only values that match the schema."
		),
	)
	result = policy_agent.run_sync(
		"Employee requests 2 days leave after finishing all sprint tasks."
	)
	print(result.output.model_dump())


@dataclass
class EmployeeDB:
	records: dict[int, dict[str, str]]


def case_4_deps_and_context_tools() -> None:
	"""Use case 4: Dependency injection + context-aware tools."""
	db = EmployeeDB(
		records={
			101: {"name": "Ananya", "department": "Engineering", "location": "Pune"},
			102: {"name": "Ravi", "department": "Finance", "location": "Bengaluru"},
			103: {"name": "Sara", "department": "HR", "location": "Hyderabad"},
		}
	)

	employee_agent = Agent(
		MODEL,
		deps_type=EmployeeDB,
		system_prompt="You are an internal HR assistant. Use tools for employee lookup.",
	)

	@employee_agent.tool
	def get_employee(ctx: RunContext[EmployeeDB], employee_id: int) -> dict[str, str] | None:
		"""Return employee info by employee id."""
		return ctx.deps.records.get(employee_id)

	result = employee_agent.run_sync(
		"Find employee 102 and tell me name and department.",
		deps=db,
	)
	print(result.output)


def case_5_message_history() -> None:
	"""Use case 5: Conversation memory using `message_history`."""
	memory_agent = Agent(MODEL)

	first = memory_agent.run_sync("My project codename is Atlas.")
	history = first.all_messages()

	second = memory_agent.run_sync(
		"What is my project codename? Reply in one line.",
		message_history=history,
	)
	print(second.output)


class Sentiment(BaseModel):
	label: Literal["positive", "neutral", "negative"]
	confidence: float = Field(ge=0.0, le=1.0)


def case_6_runtime_output_override() -> None:
	"""Use case 6: Override output schema at run-time."""
	versatile_agent = Agent(MODEL, system_prompt="You are an analyst assistant.")

	result = versatile_agent.run_sync(
		"Classify sentiment: 'The onboarding process is smooth but a bit slow.'",
		output_type=Sentiment,
	)
	print(result.output.model_dump())


if __name__ == "__main__":
	print("PydanticAI Use-Case Demo (Ollama-backed)")
	run_case("1) Basic Chat", case_1_basic_chat)
	run_case("2) Tool Plain", case_2_tool_plain)
	run_case("3) Structured Output", case_3_structured_output)
	run_case("4) Deps + RunContext Tool", case_4_deps_and_context_tools)
	run_case("5) Message History", case_5_message_history)
	run_case("6) Runtime Output Override", case_6_runtime_output_override)
