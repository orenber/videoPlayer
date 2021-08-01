import pyttsx3


engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    engine.setProperty('voice', voice.id)
    engine.say("Hello Oren, welcome back!..")
    engine.say("Please, put your mask on !")
engine.runAndWait()