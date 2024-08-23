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
        logger.debug(f'Asking: {prompt}')
        response = self.model(
            f"Question: {prompt}\nAnswer:", # Updated prompt format
            max_tokens=32, # Increased token limit
            stop=["\n"], # Adjusted stop sequence
            echo=False, # Do not echo the prompt
        )
        text = response['choices'][0]["text"].strip()
        logger.debug(f'Answer is: {text}')
        return text