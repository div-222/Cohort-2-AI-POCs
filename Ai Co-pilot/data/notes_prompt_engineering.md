# Notes: Prompt Engineering Techniques

*Personal notes compiled from various sources*

## Core Principles

1. **Be specific**: Vague prompts → vague outputs
2. **Provide context**: What role, what task, what format?
3. **Show examples**: Few-shot learning is powerful
4. **Iterate**: First prompt rarely optimal

## Key Techniques

### 1. Role Prompting
```
You are an expert Python developer with 10 years of experience in web frameworks.
```
Sets the model's "persona" and expected expertise level.

### 2. Chain-of-Thought (CoT)
```
Let's think step by step:
1. First, identify...
2. Then, calculate...
3. Finally, conclude...
```
Forces the model to show reasoning, improves accuracy on complex tasks.

**Key finding**: Adding "Let's think step by step" can improve math problem accuracy from 20% to 80%!

### 3. Few-Shot Learning
Provide 2-5 examples of input → output:
```
Q: Paris is the capital of?
A: France

Q: Tokyo is the capital of?
A: Japan

Q: Berlin is the capital of?
A:
```

### 4. ReAct (Reasoning + Acting)
Interleave thoughts and actions:
```
Thought: I need to find the population of Tokyo
Action: Search[Tokyo population]
Observation: 14 million in city proper, 37 million in metro area
Thought: The question likely refers to the metro area
Answer: Approximately 37 million people
```

### 5. Self-Consistency
Generate multiple reasoning paths and take majority vote. More reliable than single-shot.

### 6. Structured Output
Request JSON, XML, or specific format:
```
Return a JSON object with keys: {name, age, occupation}
```
Use `json_mode` in APIs when available.

## Advanced Patterns

### Tree of Thoughts (ToT)
Explore multiple reasoning branches:
- Generate several possible next steps
- Evaluate each step's promise
- Backtrack if needed
- Combine successful branches

Like beam search for reasoning!

### Prompt Chaining
Break complex tasks into steps:
1. Extract key facts → Prompt 1
2. Analyze facts → Prompt 2 (uses output of 1)
3. Generate conclusion → Prompt 3 (uses output of 2)

More reliable than one giant prompt.

### Constitutional AI (Anthropic)
1. Generate initial response
2. Critique it against principles/rules
3. Revise based on critique
4. Repeat until satisfactory

Self-correction through prompted feedback.

## Common Mistakes

❌ **Too vague**: "Write about AI"
✅ **Specific**: "Write a 500-word blog post explaining transformer architecture to high school students, using analogies to help understanding"

❌ **No format guidance**: Model decides structure
✅ **Explicit format**: "Respond in bullet points with headers"

❌ **Assuming knowledge**: "What's the latest version?"
✅ **Provide context**: "What's the latest version of Python as of February 2026?"

## Optimization Tips

1. **Temperature tuning**:
   - 0.0-0.3: Deterministic, factual
   - 0.5-0.7: Balanced
   - 0.8-1.0: Creative, diverse

2. **System vs. User prompts**:
   - System: Instructions, role, constraints
   - User: Specific query

3. **Negative prompting**: Tell it what NOT to do
   ```
   Do not include opinions. Do not make up statistics. Do not use jargon.
   ```

4. **Delimiters**: Use clear boundaries
   ```
   Context: """[your context]"""
   Question: ###[your question]###
   ```

## Prompt Engineering for Different Tasks

### For Summarization
```
Summarize the following text in 3 bullet points, focusing on:
- Main findings
- Key statistics
- Practical implications

Text: [content]
```

### For Classification
```
Classify the following email as: URGENT, NORMAL, or LOW_PRIORITY
Consider factors: deadline mentioned, sender importance, action required

Email: [content]

Classification:
```

### For Coding
```
Write a Python function that:
- Takes a list of integers as input
- Returns the sum of even numbers only
- Includes type hints
- Has a docstring
- Includes 2 test cases
```

## Resources I've Found Helpful

- OpenAI Prompt Engineering Guide
- Anthropic's Claude prompt library
- LangChain documentation (real-world patterns)
- Prompt Engineering Guide by DAIR.AI

## My Takeaways

The best prompt engineering is often:
1. Clear role/context upfront
2. Specific task description
3. Output format explicitly stated
4. Few examples if non-trivial
5. Chain complex tasks, don't monolith them

And remember: **Garbage prompt → Garbage output**, no matter how good the model!

Test, iterate, measure. Treat prompts like code.
