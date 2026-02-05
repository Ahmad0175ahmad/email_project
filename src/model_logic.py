from sklearn.cluster import HDBSCAN  # Use the built-in version
from openai import AzureOpenAI

class EmailClustering:
    def __init__(self, client: AzureOpenAI):
        self.client = client
        # Use HDBSCAN from sklearn.cluster
        self.clusterer = HDBSCAN(min_cluster_size=5)

    def get_embedding(self, text):
        # Azure OpenAI Embeddings
        response = self.client.embeddings.create(input=[text], model="text-embedding-3-small")
        return response.data[0].embedding

    def fit_taxonomy(self, embeddings):
        # Unsupervised Level 1 & 2 discovery
        labels = self.clusterer.fit_predict(embeddings)
        return labels # -1 indicates an outlier