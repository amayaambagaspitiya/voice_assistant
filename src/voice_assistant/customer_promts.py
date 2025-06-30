import random
from openai import OpenAI
from dotenv import load_dotenv
import os

class CustomerSimulator:
    def __init__(self, retriever):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.retriever = retriever
        self.message_history = []

        self.personas = {
            "Mrs. Brooks": "You are Mrs. Brooks, a first-time car buyer. You want a Toyota that’s easy to drive, safe, and not too technical.",
            "Mr. Thompson": "You are Mr. Thompson, a father of two. You want a safe, fuel-efficient Toyota for commuting and family trips.",
            "Ms. Taylor": "You are Ms. Taylor, a tech-savvy city driver. You like features like Apple CarPlay, hybrid engines, and smart tech.",
            "Mr. Harris": "You are Mr. Harris, a retired buyer on a budget. You value reliability, low maintenance, and affordability.",
            "Mr. Mitchell": "You are Mr. Mitchell, an adventurous weekend explorer. You want a rugged Toyota with AWD and good cargo space."
        }

    def pick_random_persona(self):
        self.current_persona, self.persona_description = random.choice(list(self.personas.items()))
        self.message_history = []
        return self.current_persona

    def build_prompt(self, sales_rep_input):
        context = self.retriever.retrieve_context(sales_rep_input)
        mood = random.choice(["curious", "hesitant", "excited", "skeptical", "confident"])

        instructions = f"""
You are a customer named {self.current_persona}. {self.persona_description}
You are NOT the sales rep. You are ONLY the customer. Stay fully in character.

You are currently in a conversation with a Toyota sales representative.

Your objective is to continue the conversation **naturally**, based on what the sales rep just said.

You must:
- Stay in character
- Reply to the sales rep's latest comment
- Ask **one** realistic follow-up question or make a thoughtful remark
- Keep your response to 1–2 short, natural-sounding sentences
- Speak in a tone that is {mood}

Use the info below to inform your response if helpful.

Context (retrieved knowledge):
{context}
"""

        messages = [{"role": "system", "content": instructions}]
        for pair in self.message_history:
            messages.append({"role": "user", "content": pair["user"]})
            messages.append({"role": "assistant", "content": pair["assistant"]})

        messages.append({"role": "user", "content": sales_rep_input})
        return messages

    def get_customer_response(self, sales_rep_input):
        messages = self.build_prompt(sales_rep_input)
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=120,
            temperature=0.5
        )
        output = response.choices[0].message.content
        self.message_history.append({
            "user": sales_rep_input,
            "assistant": output
        })
        return output

    def simulate(self, sales_rep_input):
        if not hasattr(self, "current_persona"):
            self.pick_random_persona()

        print(f"Sales Rep: {sales_rep_input}")
        response = self.get_customer_response(sales_rep_input)
        print(f" Customer ({self.current_persona}): {response}")
        return response
