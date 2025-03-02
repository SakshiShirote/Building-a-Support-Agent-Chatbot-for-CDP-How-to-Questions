from flask import Flask, render_template, request, jsonify
import re
from typing import Dict, List
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Simulated documentation storage (in production, this would be populated from actual docs)
class DocumentationIndex:
    def __init__(self):
        self.index = {
            "segment": {
                "set up a new source": "To set up a new source in Segment:\n1. Log into your Segment workspace\n2. Go to Connections > Sources\n3. Click 'Add Source'\n4. Choose your source type\n5. Follow the configuration steps\nSee: https://segment.com/docs/connections/sources/",
                "default": "I can help with Segment tasks like setting up sources. What specifically would you like to know?"
            },
            "mparticle": {
                "create a user profile": "To create a user profile in mParticle:\n1. Go to Setup > Inputs\n2. Configure your platform input\n3. Send events with user identities via SDK/API\n4. Profile will automatically be created\nSee: https://docs.mparticle.com/guides/platform-guide/profile/",
                "default": "I can help with mParticle tasks like creating user profiles. What specifically would you like to know?"
            },
            "lytics": {
                "build an audience segment": "To build an audience segment in Lytics:\n1. Navigate to Audiences > Create Audience\n2. Define criteria using the visual builder\n3. Add behavioral conditions\n4. Save and activate\nSee: https://docs.lytics.com/docs/audience-creation/",
                "default": "I can help with Lytics tasks like building audience segments. What specifically would you like to know?"
            },
            "zeotap": {
                "integrate my data": "To integrate data with Zeotap:\n1. Go to Data > Integrations\n2. Select your data source\n3. Configure connection parameters\n4. Map fields to Zeotap schema\nSee: https://docs.zeotap.com/data-integration/",
                "default": "I can help with Zeotap tasks like data integration. What specifically would you like to know?"
            }
        }
        
        # Cross-CDP comparison data
        self.comparisons = {
            "audience creation": {
                "segment": "Segment uses Personas with a visual builder and unlimited lookback",
                "lytics": "Lytics uses AI-driven behavioral segmentation with real-time updates",
                "mparticle": "mParticle offers real-time audience builder with historical data support",
                "zeotap": "Zeotap provides Audience Module with condition blocks"
            }
        }

    def search(self, platform: str, query: str) -> str:
        platform = platform.lower()
        query = query.lower()
        
        if platform not in self.index:
            return "Sorry, I only support Segment, mParticle, Lytics, and Zeotap."

        # Check for comparison questions
        if "compare" in query or "difference" in query:
            for topic, comp_data in self.comparisons.items():
                if topic in query:
                    return self._format_comparison(comp_data)
        
        # Search for specific how-to
        for key, value in self.index[platform].items():
            if key in query:
                return value
                
        return self.index[platform]["default"]

    def _format_comparison(self, comp_data: Dict) -> str:
        response = "Here's how they compare:\n"
        for platform, desc in comp_data.items():
            response += f"- {platform.capitalize()}: {desc}\n"
        return response

class Chatbot:
    def __init__(self):
        self.doc_index = DocumentationIndex()
        self.platform_pattern = r"(segment|mparticle|lytics|zeotap)"
        
    def process_message(self, message: str) -> str:
        if not message.strip():
            return "Please ask a question!"

        # Check for irrelevant questions
        if not any(cdp in message.lower() for cdp in ["segment", "mparticle", "lytics", "zeotap"]):
            return "Sorry, I can only help with questions about Segment, mParticle, Lytics, or Zeotap CDPs."

        # Extract platform and query
        platform_match = re.search(self.platform_pattern, message, re.IGNORECASE)
        platform = platform_match.group(0) if platform_match else "segment"  # Default to segment
        
        return self.doc_index.search(platform, message)

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message', '')
    chatbot = Chatbot()
    response = chatbot.process_message(message)
    return jsonify({'response': response})

# HTML Template (save as templates/index.html)
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>CDP Support Chatbot</title>
    <style>
        .chat-container {
            width: 600px;
            margin: 20px auto;
            border: 1px solid #ccc;
            padding: 20px;
        }
        .messages {
            height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            border: 1px solid #eee;
            padding: 10px;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
        }
        .user-message {
            background: #e3f2fd;
            text-align: right;
        }
        .bot-message {
            background: #f5f5f5;
            text-align: left;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        textarea {
            width: 100%;
            resize: none;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="messages" id="messages"></div>
        <div class="input-container">
            <textarea id="messageInput" rows="3" placeholder="Ask about Segment, mParticle, Lytics, or Zeotap..."></textarea>
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;

            addMessage(message, 'user-message');
            input.value = '';

            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => addMessage(data.response, 'bot-message'));
        }

        function addMessage(text, className) {
            const messages = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = `message ${className}`;
            div.textContent = text;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }

        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    # In production, you'd populate this with actual documentation content
    with open('templates/index.html', 'w') as f:
        f.write(html_template)
    
    app.run(debug=True, host='0.0.0.0', port=5000)