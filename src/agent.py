from llama_cpp import Llama
from loguru import logger

class Agent:
    def __init__(self, model_path: str) -> None:
        self.model = Llama(
            model_path=model_path,
            # n_gpu_layers=-1, # Uncomment to use GPU acceleration
            # seed=1337, # Uncomment to set a specific seed
            # n_ctx=2048, # Uncomment to increase the context window
        )
    
    def ask(self, prompt: str) -> str:
        logger.debug(f'Asking {prompt}')
        response = self.model(
            f"Q: {prompt} A: ", # Prompt
            max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
            stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
            echo=True # Echo the prompt back in the output
        ) # Generate a completion, can also call create_completion
        text = response['choices'][0]["text"]
        logger.debug(f'Answer is {text}')
        return text