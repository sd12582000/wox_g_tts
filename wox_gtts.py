#encoding=utf8

#Your class must inherit from Wox base class https://github.com/qianlifeng/Wox/blob/master/PythonHome/wox.py
#The wox class here did some works to simplify the communication between Wox and python plugin.
from gtts import gTTS
import pygame
pygame.mixer.init()
pygame.init()

from wox import Wox,WoxAPI
class Wox_G_TTS(Wox):
    def __init__(self):
        super().__init__()
    from os.path import abspath, join, dirname
    from json import load
    file_path = join(abspath(dirname(__file__)), "config.json")
    config = {}
    with open(file_path, 'r', encoding='utf-8') as json_file:
        config = load(json_file)

    default_lang = config['Common_lang']

    def say(self, text, lang='en', slow=True):
        """
        get audio from gTTS and play it
        """
        import io
        tts = gTTS(text=text, lang=lang, slow=slow)
        with io.BytesIO() as fp:
            tts.write_to_fp(fp)
            fp.seek(0)
            pygame.mixer.music.load(fp)
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            pygame.event.set_allowed(pygame.USEREVENT)
            pygame.mixer.music.play()
            pygame.event.wait()

    def detect_language(self, string):
        """
        return probabilities for the top languages list
        """
        from langdetect import detect_langs
        return detect_langs(string)

    def query(self, query):
        """
        query to Speech
        """
        results = []
        query = query.strip()
        if not query:
            return results
        argv = query.split()

        if len(argv) > 1:
            if argv[0] in self.default_lang:
                query = ' '.join(argv[1:])
                results.append({
                    "Title":query,
                    "SubTitle": self.default_lang[argv[0]],
                    "IcoPath":"speaker.png",
                    "JsonRPCAction":{"method": "say"
                                               , "parameters": [query, argv[0], False]},
                    "dontHideAfterAction":True
                    })

        pro_list = self.detect_language(query)
        for lang in pro_list:
            results.append({
                "Title":'Detect {}'.format(query),
                "SubTitle": lang.lang,
                "IcoPath":"question-mark.png",
                "JsonRPCAction":{"method": "say"
                                           , "parameters": [query, lang.lang, False]},
                "dontHideAfterAction":True
                })
        return results

#Following statement is necessary
if __name__ == "__main__":
    Wox_G_TTS()
