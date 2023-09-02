import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import anthropic
import openai
import dotenv
dotenv.load_dotenv('.env')

assert "OPENAI_API_KEY" in os.environ, "Please set your OPENAI_API_KEY in a .env file."


class Chat:
    def __init__(self, system_prompt=""):
        self.system = system_prompt
        self.messages = []

    def response(self, prompt):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
                    #   model="gpt-3.5-turbo",
            model="gpt-4-0314",
            messages=self.messages,
            #         max_tokens=200
        )
        response = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": response})
        return response

api_key = os.getenv("ANTHROPIC_API_KEY")
anthropic = Anthropic(
    api_key=api_key,
)

def call_claude_instant_1(prompt):
    completion = anthropic.completions.create(
        model="claude-instant-1.2",
        max_tokens_to_sample=5000,
        prompt=f"{HUMAN_PROMPT}{prompt}{AI_PROMPT}",
    )
    return completion.completion

def call_claude_2(prompt):
    completion = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=5000,
        prompt=f"{HUMAN_PROMPT}{prompt}{AI_PROMPT}",
    )
    return completion.completion


def call_gpt3(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # Define the parameters for the completion
    response = openai.ChatCompletion.create(
            model="gpt-4-0314",
            messages=[{"role": "user", "content": prompt}],
    )

    response = response["choices"][0]["message"]["content"]
    return response

def call_gpt4(prompt, system_prompt=""):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # Define the parameters for the completion
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
    )

    response = response["choices"][0]["message"]["content"]
    return response


class TokenAwareKnowledgeTree():
    def __init__(self, topic) -> None:
        self.topic = topic
        self.outline = generate_long_text_outline(topic)
        self.root = TokenAwareKnowledgeTreeNode(self.outline)
        self.height = self.root.getHeight()

    
    def generate_component(self, component_index):
        if len(component_index) == 0:
            return None
        transcript = []
        node = self.root
        for index in component_index:
            for i in range(index):
                transcript.append(node.children[i].getTranscript())
            node = node.children[index]
        


class TokenAwareKnowledgeTreeNode():
    def __init__(self, json) -> None:
        self.title = json["title"]
        self.children = []
        self.text = ""
        self.summary = ""
        if json["components"]:
            for component in json["components"]:
                self.children.append(TokenAwareKnowledgeTreeNode(component))
    
    def getTranscript(self):
        if self.children:
            return self.title + " " + " ".join([child.getTranscript() for child in self.children])
        else:
            return self.text
        
    def setTranscript(self, transcript):
        if self.children:
            # error if trying to set transcript of a non-leaf node
            raise Exception("Cannot set transcript of a non-leaf node")
        else:
            self.text = transcript
    


    def getHeight(self):
        if len(self.children) == 0:
            return 0
        else:
            return 1 + max([child.getHeight() for child in self.children])

class LongTextGenerator():
    def __init__(self, topic) -> None:
        self.topic = topic
        self.outline = generate_long_text_outline(topic)
        self.book = Book.from_json(self.outline)
        
        


def generate_long_text_outline(topic, chapters, sections_per_chapter, sub_sections_per_section):
    prompt = f"""
Generate a 5 part outline, each with  subparts on a book about the topic of {topic}.

Output in JSON format. Only reply JSON in your reponse.
"""
    system_prompt = f"""
You are writing a book about {topic}.
The book has {chapters} chapters.
Each chapter has {sections_per_chapter} sections.
Each section has {sub_sections_per_section} sub-sections.
You write the outline of the book, including the chapter names, section names, and sub section names.
When generating chapter, section, and sub section names, create names that are relevant and interesting to the topic of {topic}.
Each section should be relevant to it's corresponding chapter, and no other chapters, 
Each subsection should be relevant to it's corresponding section, and no other sections.
You return the outline in the following JSON format: 
A dictionary with 2 keys: "title" and "components".
The value of "title" is a string with the title of the book.
The value of "components" is a list of dictionaries recursively following the same format.
Extend the recursion until each sub-section has a title and no components.
You only output JSON in your response.
The topic is {topic}.
The outline of the book is:
"""
    response = call_gpt4(system_prompt)
    return response
    
def generate_speech_section_transcript(topic, outline, section, transcript_so_far, system_prompt=""):
    
    prompt = f"""
You are generating the transcript for a speech on {topic}.
The overall outline of the speech is: {outline}
The current section of the speech is: {section}
The transcript so far is: 
"""


if __name__ == '__main__':
    print(generate_long_text_outline(
        topic="Mt. Lassen Volcano National Park",
        chapters=5,
        sections_per_chapter=3,
        sub_sections_per_section=2
        ))