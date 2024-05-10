# Chatbot using Flask and TensorFlow
This is a simple chatbot project implemented in Python using Flask for the web application and TensorFlow for natural language processing. The chatbot is capable of understanding user input and responding with appropriate messages based on pre-defined intents.

## Clone the repository
```
git clone https://github.com/TomRigger/Simple-chatbot.git
```
## Install the required dependencies
```
pip install -r requirements.txt
```
## Usage
1. Run the flask application
```
python poc_chatbot.py
```
2. Open your web browser and got to http://127.0.0.1:5000/
3. Start chatting with the bot by typing messages into the input box.

## How it Works
1. The chatbot is trained on a dataset of intents stored in intents.json.
2. It preprocesses user input using tokenization and padding techniques.
3. A neural network model is trained using TensorFlow, which maps user input to corresponding intents.
4. When a user sends a message, the chatbot predicts the intent and responds with a pre-defined message associated with that intent.
