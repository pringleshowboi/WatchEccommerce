import nltk
from nltk.chat.util import Chat, reflections

# Define basic conversation patterns
pairs = [
    ["hi|hello|hey", ["Hello! How can I help you today?"]],
    ["(.*) your name?", ["I'm the assistant for your Fake-Ecommerce site!"]],
    ["(.*) products?", ["You can browse products under the products section."]],
    ["bye|exit", ["Goodbye! Have a nice day!"]],
    ["(.*)", ["I'm not sure how to help with that, but feel free to ask anything about the store."]]
]

# Initialize chatbot
def chatbot_response(message):
    chatbot = Chat(pairs, reflections)
    return chatbot.respond(message)
