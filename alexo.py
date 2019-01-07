# -*- coding: utf-8 -*-

#Chatterbot tiene dependencias de otras librerías, las actualizamos antes de instalarlo
#import selenium
#pip3 install --upgrade pandas
#pip3 install --upgrade plotly

#Instalamos la librería. El parámetro -q es modo 'quiet' para evitar tener muchos logs de la instalación
#pip3 install -q chatterbot

#Importamos las clases necesarias
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

#Inicializamos un objeto de la clase ChatBot
chatbot = ChatBot(
    #Le ponemos nombre a nuestro bebe
    "Alexo",
     #Establecemos adaptadores para que interactue desde la termminal
    input_adapter="chatterbot.input.TerminalAdapter",    
    output_adapter="chatterbot.output.TerminalAdapter",
    #output_format="text",
    #Los adaptadores logicos sirven para saber que tipo de respuesta es la más adecuada.
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_most_frequent_response"
        },
        {
            #Establecemos un límite de confianza para saber que tan bien puede decidir la respuesta correcta
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.51,
            'default_response': 'Disculpa, no entendí. ¿Puedes ser más específico?.'
        },
    ],
    #Para limpiar el texto. En este caso le quito excedentes de espacios blancos y  caracteres especiales
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    #read_only sirve para que el bot no aprenda. Solo conteste con los datos de entrenamiento.
    read_only=False,
)
#La sesión es requisito en la penúltima versión. Éste parámetro ignoralo por ahora
DEFAULT_SESSION_ID = 1
#Configurar que el entrenamiento sea desde un corpus (archivo.yml)
chatbot.set_trainer(ChatterBotCorpusTrainer)
#Inicializamos un objeto 'trainer'
trainer = ChatterBotCorpusTrainer(chatbot.storage)
#Establecemos las rutas a nuestros corpus; en éste caso los tres primeros vienen en la paquetería chatterbot. Los siguientes son creación propia.
trainer.train(
    "chatterbot.corpus.spanish.greetings",
    "chatterbot.corpus.spanish.conversations",
    "chatterbot.corpus.spanish.trivia",
    "./spring.yml",
    "./chistes.yml",
    "./futbol.yml",
    "./cocina.yml",
    "./literatura.yml",
    "./deportes.yml"
)
#Imprimimos en consola un mensaje inicial
print("¡Hola! Teclea algo para iniciar. Para salir presiona 'ctrl + c' o 'ctrl + d' ...")
#Entra en un ciclo, mientras el usuario interactue, chatbot buscará las respuestas más adecuadas en cada uno de los sets de entrenamiento.
while True:
    print("\nYou: ") 
    input_statement = chatbot.input.process_input_statement()
    statement, response = chatbot.generate_response(input_statement, DEFAULT_SESSION_ID)
    print("\nAlexo: \n%s" % response)



