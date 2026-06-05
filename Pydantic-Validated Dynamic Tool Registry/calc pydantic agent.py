from pydantic_ai import Agent
from openai import AsyncOpenAI
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

client = AsyncOpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)

model = OpenAIChatModel(
    model_name='qwen3.5:4b',
    provider=OpenAIProvider(openai_client=client)
)

agent = Agent(model)

@agent.tool_plain
def add(a:int,b:int):
    return a+b

result = agent.run_sync(
    "Add 10 and 20"
)

print(result.output)