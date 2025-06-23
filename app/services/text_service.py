"""Text generation service."""

import random

from app.generated.generated_models import GenerateTextResponse


class TextService:
    """Service for text generation operations."""

    def __init__(self):
        # Sample text templates for generation
        self.templates = [
            "Based on your prompt '{prompt}', here are some thoughts: ",
            "Continuing from '{prompt}', we could explore: ",
            "Your idea about '{prompt}' reminds me of: ",
            "Building on '{prompt}', consider this: ",
            "In response to '{prompt}', I would suggest: ",
        ]

        self.continuations = [
            "the importance of creativity in problem-solving.",
            "how technology shapes our daily experiences.",
            "the value of continuous learning and adaptation.",
            "the interconnectedness of all things in nature.",
            "the power of collaboration and teamwork.",
            "the beauty found in simplicity and minimalism.",
            "the significance of sustainable practices.",
            "the impact of positive thinking on outcomes.",
            "the role of innovation in progress.",
            "the wisdom gained through diverse perspectives.",
        ]

    async def generate_text(
        self, prompt: str, max_length: int = 50, temperature: float = 1.0
    ) -> GenerateTextResponse:
        """
        Generate text based on input prompt.

        This is a simple rule-based text generator since we don't have
        access to external models in this environment.
        """
        # Select a random template and continuation
        template = random.choice(self.templates)
        continuation = random.choice(self.continuations)

        # Generate the text
        generated_part = template.format(prompt=prompt) + continuation

        # Respect max_length by truncating if necessary
        if len(generated_part) > max_length:
            generated_part = generated_part[: max_length - 3] + "..."

        # Add some metadata
        metadata = {
            "generation_method": "rule_based",
            "temperature_used": temperature,
            "max_length_requested": max_length,
            "actual_length": len(generated_part),
            "prompt_length": len(prompt),
        }

        return GenerateTextResponse(
            generated_text=generated_part, input_prompt=prompt, metadata=metadata
        )
