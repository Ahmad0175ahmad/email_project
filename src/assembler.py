class ConversationAssembler:
    def assemble(self, email_list):
        # Sort by timestamp
        sorted_emails = sorted(email_list, key=lambda x: x['timestamp'])
        
        full_text = []
        for msg in sorted_emails:
            # Merge subject, body, and attachment names
            full_text.append(f"Subject: {msg['subject']}\nBody: {msg['body']}")
            if msg.get('attachments'):
                full_text.append(f"Attachments: {', '.join(msg['attachments'])}")
                
        return "\n\n".join(full_text) # Single classification unit