import ollama
from loguru import logger

class Agent:
    def __init__(self, model = 'llama3.1') -> None:
        self.model = model
    
    def ask(self, prompt: str) -> str:
        logger.debug(f'Asking {prompt}')
        response = ollama.generate(model=self.model, prompt=prompt, system='Answer very short answers where you can')
        text = response['response']
        logger.debug(f'Answer is {text}')
        return text