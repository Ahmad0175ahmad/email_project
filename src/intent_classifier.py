import json
import re

class IntentClassifierL3:
    def __init__(self, azure_openai_client):
        self.client = azure_openai_client
        # Fast rule-based triggers
        self.urgency_keywords = ["urgent", "emergency", "asap", "immediate"] # cite: 310

    def get_intent(self, text, signals):
        # 1. Check deterministic rules first
        if any(word in text.lower() for word in self.urgency_keywords):
            return "Urgent Request", 0.95  # High confidence for rule match

        # 2. Hybrid: Use LLM for nuanced intent
        prompt = f"""
        Analyze this email conversation and categorize the intent into one of:
        'Service Request', 'Status Inquiry', 'Complaint', 'Additional Info'.
        Return ONLY valid JSON in this format: {{"intent": "value", "confidence": 0.0}}
        Content: {text[:2000]}  # Cite: 309 (sanitized text)
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4", # cite: 1.4
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" } # cite: 309
        )
        
        res_data = json.loads(response.choices[0].message.content)
        return res_data['intent'], res_data['confidence']