import pyttsx3


class TextToSpeech():

    def __init__(self):

        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')

    def greating(self, name:str):
        self.engine.say("Hello"+name+", welcome back!..")

    def ask(self):
        self.engine.say( "Please, put your mask on !" )
        self.engine.say( "Please, shake yours boobs !" )

    def run(self):
        self.engine.runAndWait()


def main():
    speech = TextToSpeech()
    speech.greating(",Ella.....")
    speech.ask()
    speech.run()



if __name__ == "__main__":
    main()
