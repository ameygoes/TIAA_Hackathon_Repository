from typing import Any, List

from peak_into_the_future.pydantic_models import ActionModel


class Prompter:
    def ai_completion(self, prompt: str):
        # will call the openai chat completion api
        raise NotImplementedError
    
    def ai_function_calling(self, messages, functions):
        # will call the openai function calling api
        raise NotImplementedError

# Need a prompt class to generate 3 options of actions
class ActionPrompter:
    def __call__(self, curr_summary: str, retirement_goals: str, prev_actions: List[ActionModel]) -> Any:
        # raise Not implemented warning
        # TODO (rohan): implement this

        Warning("ActionPrompter is not implemented yet")
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
