import base64

from googletrans import Translator, constants

#constants.LANGUAGES[detection.lang]
from DjangoReader.services.helper import fromBase64

translator = Translator()



def translate(text, origin_language_name, translating_language_name):
    text = fromBase64(text)
    name = None
    name2 = None
    for key, value in constants.LANGUAGES.items():
        if (value == origin_language_name):
            name = key
        if (value == translating_language_name):
            name2 = key
            #sample_string = "GeeksForGeeks is the best"
            #sample_string_bytes = sample_string.encode("ascii")

            #base64_bytes = base64.b64encode(sample_string_bytes)
            #base64_string = base64_bytes.decode("ascii")
            a = translator.translate(text=text, src=name, dest=name2).text
    return base64.b64encode(translator.translate(text=text, src=name, dest=name2).text.encode()).decode()

