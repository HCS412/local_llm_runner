# pipelines/router.py

from pipelines import base_pipeline


def route_and_run_pipeline(prompt_type: str, user_prompt: str):
    """
    Routes the user prompt to the appropriate pipeline based on its category.
    For now, all categories use the base pipeline.

    Args:
        prompt_type (str): The classified category.
        user_prompt (str): The original user input.

    Returns:
        None
    """
    # TODO: Add routing logic here when we have specialized pipelines
    return base_pipeline.run_pipeline(user_prompt, prompt_type)
