import pyttsx3


class TextToSpeech():

    def __init__(self):

        female = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', female)

    def greeting(self, name:str):
        self.engine.say("Hello"+name+", welcome back!..")

    def ask(self):
        self.engine.say( "Please, put your mask on !" )
        #self.engine.say( "Please, shake yours boobs !" )

    def run(self):
        self.engine.runAndWait()


def main():
    speech = TextToSpeech()
    speech.greeting(",Ella.....")
    speech.ask()
    speech.run()

if __name__ == "__main__":
    main()
