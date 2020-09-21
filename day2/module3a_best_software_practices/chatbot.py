#! /usr/bin/python3
# Owen Chapman
# 9/14/2020
# BISB Bootcamp 2020
#   Module 3a: Best Software Practices

def chatbot(input_message):
    
    if input_message == "Hello!":
        reply = "Hello!"
    elif input_message == "Hello there!":
        reply = "General Kenobi!"
    else:
        reply = "I'm sorry. I didn't understand that."
    
    print(reply)
    return


print("Hello. I am a chatbot!")
while True:
    user_input = input("Type a message here: ")
    chatbot(user_input)

