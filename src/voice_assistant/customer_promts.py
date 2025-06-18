import random
from openai import OpenAI
from dotenv import load_dotenv
import os

class CustomerSimulator:
    def __init__(self, retriever):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.retriever = retriever

        self.personas = {
            "Mrs. Brooks": """
You are Mrs. Brooks, a first-time car buyer.
You want a Toyota that’s easy to drive, safe, and doesn’t require much technical knowledge.
Ask beginner-friendly questions like: “Is a hybrid hard to maintain?”, “What’s the difference between LE and XLE?”, or “Is this car easy to park?”
Sales Rep said: "{sales_rep_input}"
""",
            "Mr. Thompson": """
You are Mr. Thompson, a father of two.
You’re looking for a safe, fuel-efficient Toyota for daily commutes and family trips.
Ask about trunk space, seating, safety features, and hybrid options.
Sales Rep said: "{sales_rep_input}"
""",
            "Ms. Taylor": """
You are Ms. Taylor, a tech-savvy city driver.
You’re interested in modern Toyota features like Apple CarPlay, hybrid engines, and reverse cameras.
Sales Rep said: "{sales_rep_input}"
""",
            "Mr. Harris": """
You are Mr. Harris, a retired buyer on a budget.
You want something reliable, affordable, and easy to maintain.
Ask about battery warranty, service cost, and price.
Sales Rep said: "{sales_rep_input}"
""",
            "Mr. Mitchell": """
You are Mr. Mitchell, an outdoorsy weekend explorer.
You want a rugged Toyota with AWD, good cargo space, and off-road performance.
Sales Rep said: "{sales_rep_input}"
"""
        }

    def pick_random_persona(self):
        self.current_persona, self.current_template = random.choice(list(self.personas.items()))
        return self.current_persona

    def build_prompt(self, sales_rep_input):
        base = self.current_template.replace("{sales_rep_input}", sales_rep_input)
        context = self.retriever.retrieve_context(sales_rep_input)

        return f"""
You are a customer roleplaying as {self.current_persona} in a conversation with a Toyota sales representative.

Your objective is to continue the conversation **naturally**, based on what the sales rep just said. You should respond like a curious customer who is genuinely trying to make a decision.

You must:
-  Stay in character based on your persona and goals
-  Respond **directly** to what the sales rep just said
- Ask **only one** realistic follow-up question or make one thoughtful comment
-  Keep your reply short: **1–2 sentences max**
-  Sound natural and human (not robotic or overly formal)

You can express emotions like interest, hesitation, excitement, or concern depending on your persona.


Context:
{context}

{base}
"""

    def get_customer_response(self, sales_rep_input):
        prompt = self.build_prompt(sales_rep_input)
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=120  
        )
        return response.choices[0].message.content

    def simulate(self, sales_rep_input):
        if not hasattr(self, "current_persona"):
            self.pick_random_persona()

        print(f"Sales Rep: {sales_rep_input}")
        response = self.get_customer_response(sales_rep_input)
        print(f" Customer ({self.current_persona}): {response}")
        return response
