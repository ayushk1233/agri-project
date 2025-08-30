# backend/app/services/llama_service.py
import httpx
import json

async def generate_text(prompt: str) -> str:
    """
    Generate text from local LLaMA model via Ollama server.
    Requires Ollama to be running locally: `ollama serve`
    And the model pulled: `ollama pull llama3`
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3", "prompt": prompt},
                timeout=None  # disable timeout for long generations
            )
            
            # The API streams tokens, collect them
            output = ""
            async for chunk in response.aiter_text():
                for line in chunk.splitlines():
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            output += data["response"]
                    except json.JSONDecodeError:
                        continue


            return output.strip()

    except Exception as e:
        return f"Error communicating with local LLaMA: {str(e)}"
