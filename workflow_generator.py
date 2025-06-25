#Parsing may need tweaks if LLM formatting shifts—monitor escape behavior.

from llm_ollama import query_ollama
import json

# Template: LLM outputs reasoning and JSON
PROMPT_TEMPLATE = '''
You are a geospatial reasoning assistant.

Given a user task, first think through the required inputs, preprocessing, and analyses _step by step_.
Then output two parts:

--BEGIN REASONING--
1.

--END REASONING--

--BEGIN WORKFLOW--
{{  "tasks": [ /* JSON array of processing steps */ ]  }}
--END WORKFLOW--
'''  


def generate_workflow(user_query: str) -> dict:
    """
    Returns a dict with keys 'reasoning' (list of steps) and 'workflow' (dict).
    """
    prompt = PROMPT_TEMPLATE.replace("user task", user_query)
    raw = query_ollama(prompt)

    # Parse reasoning and JSON block
    try:
        reasoning = raw.split("--BEGIN REASONING--")[1].split("--END REASONING--")[0].strip().splitlines()
        wf_json = raw.split("--BEGIN WORKFLOW--")[1].split("--END WORKFLOW--")[0].strip()
        workflow = json.loads(wf_json)
    except Exception as e:
        raise ValueError(f"Failed to parse LLM output: {e}\nRaw output:\n{raw}")

    return {"reasoning": reasoning, "workflow": workflow}