"""LLM operations using LiteLLM."""

import os
from pathlib import Path
from typing import Optional, Any
import litellm
from litellm import completion


# Configure LiteLLM
litellm.drop_params = True  # Drop unsupported params
litellm.set_verbose = os.getenv("LITELLM_VERBOSE", "false").lower() == "true"  # type: ignore


def load_prompt_template(template_name: str) -> str:
    """
    Load a prompt template from the prompts directory.

    Args:
        template_name: Name of the template file (without .md extension)

    Returns:
        Template content as string

    Raises:
        FileNotFoundError: If template doesn't exist
    """
    prompts_dir = Path(__file__).parent.parent / "prompts"
    template_path = prompts_dir / f"{template_name}.md"

    if not template_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {template_path}")

    return template_path.read_text(encoding="utf-8")


def format_prompt(template: str, **variables) -> str:
    """
    Format a prompt template with variables.

    Args:
        template: Template string with {variable} placeholders
        **variables: Variables to substitute into template

    Returns:
        Formatted prompt string
    """
    return template.format(**variables)


def call_llm(
    prompt: str,
    model: str = "mistral/mistral-small-latest",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    response_format: Optional[dict[str, str]] = None,
    **kwargs: Any,
) -> tuple[str, dict[str, Any]]:
    """
    Unified wrapper for LLM API calls using LiteLLM.

    Args:
        prompt: The prompt to send to the LLM
        model: Model identifier (e.g., "mistral/mistral-small-latest")
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum tokens in response
        response_format: Optional response format (e.g., {"type": "json_object"})
        **kwargs: Additional arguments passed to litellm.completion()

    Returns:
        Tuple of (response_text, metadata_dict)
        metadata includes: model, tokens, etc.

    Raises:
        Exception: If LLM call fails
    """
    messages = [{"role": "user", "content": prompt}]

    call_kwargs = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        **kwargs,
    }

    if max_tokens:
        call_kwargs["max_tokens"] = max_tokens

    if response_format:
        call_kwargs["response_format"] = response_format

    try:
        response = completion(**call_kwargs)

        content = response.choices[0].message.content  # type: ignore
        metadata = {
            "model": response.model,
            "total_tokens": getattr(response.usage, "total_tokens", None),  # type: ignore
            "prompt_tokens": getattr(response.usage, "prompt_tokens", None),  # type: ignore
            "completion_tokens": getattr(response.usage, "completion_tokens", None),  # type: ignore
        }

        return content or "", metadata  # type: ignore

    except Exception as e:
        raise Exception(f"LLM call failed: {str(e)}") from e


def call_llm_with_template(
    template_name: str,
    model: str = "mistral/mistral-small-latest",
    temperature: float = 0.7,
    **template_vars: Any,
) -> tuple[str, dict[str, Any]]:
    """
    Load a template, format it, and call the LLM.

    Args:
        template_name: Name of the template file (without .md)
        model: Model identifier
        temperature: Sampling temperature
        **template_vars: Variables to substitute into template

    Returns:
        Tuple of (response_text, metadata_dict)
    """
    template = load_prompt_template(template_name)
    prompt = format_prompt(template, **template_vars)
    return call_llm(prompt, model=model, temperature=temperature)
