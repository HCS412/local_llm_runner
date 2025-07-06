# pipelines/router.py

from pipelines import (
    base_pipeline,
    technical_pipeline,
    venture_pipeline,
    social_pipeline,
    creative_pipeline,
    emotional_pipeline,
    philosophical_pipeline,
    product_pipeline,
    power_pipeline,
    identity_pipeline,
    vision_pipeline,
    simple_pipeline,
)

def route_and_run_pipeline(prompt_type: str, user_prompt: str):
    """
    Routes the user prompt to the appropriate pipeline based on its category.
    """
    if prompt_type == "technical":
        return technical_pipeline.run_pipeline(user_prompt, prompt_type)
    elif prompt_type == "venture":
        return venture_pipeline.run_pipeline(user_prompt, prompt_type)
    elif prompt_type == "social":
        return social_pipeline.run_pipeline(user_prompt, prompt_type)
    elif prompt_type == "creative":
        return creative_pipeline.run_pipeline(user_prompt, prompt_type)
    elif prompt_type == "emotional":
        return emotional_pipeline.run_pipeline(user_prompt, prompt_type)
    elif prompt_type == "philosophical":
        return philosophical_pipeline.run_pipeline(user_prompt, prompt_type)
    elif prompt_type == "product":
        return product_pipeline.run_pipeline(user_prompt, prompt_type)
    elif prompt_type == "power":
        return power_pipeline.run_pipeline(user_prompt, prompt_type)
    elif prompt_type == "identity":
        return identity_pipeline.run_pipeline(user_prompt, prompt_type)
    elif prompt_type == "vision":
        return vision_pipeline.run_pipeline(user_prompt, prompt_type)
    elif prompt_type == "simple":
        return simple_pipeline.run_pipeline(user_prompt, prompt_type)
    else:
        return base_pipeline.run_pipeline(user_prompt, prompt_type)
