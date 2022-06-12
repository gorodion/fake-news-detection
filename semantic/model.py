from scipy.spatial.distance import cosine
from transformers import AutoModel, AutoTokenizer, AutoConfig
import torch


class SemanticModel:
    """
    This model extracts the semantics of a text, using https://huggingface.co/DeepPavlov/rubert-base-cased
    """
    def __init__(self, model_path, model_name, device):
        self.model = AutoModel.from_pretrained(model_path, config=AutoConfig.from_pretrained(model_name))
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model.to(device)
        self.model.eval()
        self.device = device

    def __call__(self, text1: str, text2: str):
        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)

        sim = 1 - cosine(emb1, emb2)
        return sim

    def get_embedding(self, text):
        t = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            inputs = {k: v.to(self.device) for k, v in t.items()}
            model_output = self.model(**inputs)
        embeddings = model_output.last_hidden_state[:, 0, :]
        embeddings = torch.nn.functional.normalize(embeddings)
        return embeddings[0].cpu().numpy()
