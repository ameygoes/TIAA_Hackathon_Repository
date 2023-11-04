import json
import os
import openai
import functools
from typing import Any, List, Dict, Optional

from peak_into_the_future.pydantic_models import ActionModel

openai.api_type='azure'
openai.api_base = os.environ["OPENAI_API_HOST"]
openai.api_key = os.environ["OPENAI_API_KEY"]

class Prompter:
    def __init__(self) -> None:
        self.cache = {}

    def ai_completion(self, messages: List[Dict[str, str]], temperature: float, stop: Optional[List[str]]):
        _tmp = json.dumps(messages)
        if temperature == 0 and _tmp in self.cache:
            return self.cache[_tmp]

        response = openai.ChatCompletion.create(
            engine=os.environ["BASE_MODEL_NAME"],
            messages=messages,
            temperature=temperature,
            stop=stop if stop is not None else []
        )
        ret = response['choices'][0]['message']['content']
        if temperature == 0: self.cache[_tmp] = ret
        return ret
    
    def ai_function_calling(self, messages, functions):
        # will call the openai function calling api
        raise NotImplementedError


class JSONExtractor(Prompter):
    def __init__(self) -> None:
        super().__init__()
        self.prompt_template = """Correct the following JSON. DO NOT RETURN ANY OTHER TEXT. ONLY THE CORRECTED JSON WITHOUT BACKTICKS. If the JSON is correct, return the same JSON without backticks.
```
{bad_json}
```
"""

    @functools.lru_cache(maxsize=128)
    def __call__(self, bad_json: str) -> str:
        messages = [{
            'role': 'user',
            'content': self.prompt_template.format(bad_json=bad_json)
        }]
        return self.ai_completion(messages, temperature=0)

# Need a prompt class to generate 3 options of actions
class ActionPrompter(Prompter):
    def __init__(self) -> None:
        super().__init__()
        self.stage_prompt_template = """
Act as a career and finance coach who is experienced in the sector of planning financial decisions and investments with a focus on career development for achieving clients' retirement goals. The client has provided their current state and retirement goals. Use your knowledge about the market trends to provide a highly personalized 10-stage action plan to go from the client's current state to their retirement goals.

Based on the type of path the user has chosen, and the previous actions they have taken, give a stage that will help them achieve their retirement goals. Return a JSON response:
{
  'current_state': <summary of current state>,
  'retirement_goal': <summary of retirement goal>,
  'stage_<n>': {
    'title': <str: should be less than 5 words>,
    'action': <str: action text less than 5 words>,
    'description: <str: text description of the action>,
    'age': <int: age of the user post completion>,
    'delta_in_retirement_savings': <int: expected $$'s growth/decline in retirement savings of the user. positive means growth, and negative means decline>'
  }
}
        """
        self.path_prompt_template = """
Act as a career and finance coach who is experienced in the sector of planning financial decisions and investments with a focus on career development for achieving clients' retirement goals. The client has provided their current state and retirement goals. Use your knowledge about the market trends to provide a highly personalized 10-stage action plan to go from the client's current state to their retirement goals.

First, give 3 different paths they could take. The paths should be such that they offer a wide solution space to explore. Keep one of them related to investments. Then, for each path return a JSON response:

Keep in mind, the stages should also represent significant expense an average person makes in their lifetime, like on marriage, or child's education. DON'T just mention "Major life event", specifiy "Marriage" or "Children's Education" or <something else>
---
Student Profile: {user_name}

```Current state
{curr_summary}

Financial Knowledge:  # TODO (rohan): add this line to financial knowledge variable
{financial_knowledge}

Professional Network in Field of Interest (Environmental Science):
{professional_network}

Additional Notes:
{additional_notes}
```
```Retirement Goals:
{retirement_goals}
```
---
        """
    def __call__(self, curr_summary: str, retirement_goals: str, prev_actions: List[ActionModel]) -> Any:
        # raise Not implemented warning
        Warning("ActionPrompter is not implemented yet")
        # TODO (rohan): implement this
        # return 3 dummy actions
        ret = [
            ActionModel(
                title="Action 1",
                description="This is the description of action 1",
                action="This is the action of action 1",
                age=50
            ),
            ActionModel(
                title="Action 2",
                description="This is the description of action 2",
                action="This is the action of action 2",
                age=50
            ),
            ActionModel(
                title="Action 3",
                description="This is the description of action 3",
                action="This is the action of action 3",
                age=50
            )
        ]
        return ret
        
# Need a prompt class to extract information TODO (rohan): From where? why? and what?
