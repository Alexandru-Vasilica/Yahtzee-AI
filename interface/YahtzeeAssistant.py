import google.generativeai as genai


class YahtzeeAssistant:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)

    def generate_chat_response(self, message):
        system_prompt = (
            "You are a helpful assistant who only answers questions about the game of Yahtzee. "
            "You can explain the rules, suggest strategies, provide real-time advice, and help with practice scenarios. "
            "Do not provide information or answers unrelated to Yahtzee."
            "Do not say more than you need to. Be concise and to the point."
        )
        try:
            full_prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
            response = genai.GenerativeModel("gemini-1.5-flash").generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error: {e}")
            return "Sorry, I couldn't process your request. Please try again."
