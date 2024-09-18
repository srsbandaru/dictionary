from django.shortcuts import render
from django.views import View
from django.conf import settings

# Import json data to load JSON Data to Python Dictionary
import json

# To make request to API
import urllib.request

# Create your views here.
class IndexView(View):
    template_name = "definitions/index.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        word = request.POST["word"]
        search_word = word.replace(' ','%20')
        print(word)
        
        try:
            # for definintions
            api_url = str(
                "https://api.wordnik.com/v4/word.json/"+search_word+"/definitions?limit=200&includeRelated=false&sourceDictionaries=wordnet&useCanonical=false&includeTags=false&api_key="+settings.DICTIONARY_API_KEY
            )
            source_data = urllib.request.urlopen(api_url).read()

            # Convert JSON data to a Python Dictionary
            list_of_data = json.loads(source_data)
            # print(list_of_data)
            # print(type(list_of_data))

            definitions = ""
            for data in list_of_data:
                print(data["partOfSpeech"])
                print(data["text"])
                definitions = definitions + str("<i>" + data["partOfSpeech"] + "</i><br><b>" + data["text"] + "</b>") + "<br>"

            # Get partOfSpeech and text from list_of_data
            dictionary_data = {
                "search_word":word,
                "definitions":definitions
            }

            try:
                # for audio
                api_url_audio = str(
                    "https://api.wordnik.com/v4/word.json/"+search_word+"/audio?useCanonical=false&limit=50&api_key="+settings.DICTIONARY_API_KEY
                )
                source_data_audio = urllib.request.urlopen(api_url_audio).read()
                list_of_data_audio = json.loads(source_data_audio)
                # print(list_of_data_audio)
                audio_url = list_of_data_audio[1]["fileUrl"]
                # print(audio)
                # Add audio_url to dictionary
                dictionary_data.update(audio = audio_url)
            except:
                print("Audio not found")

            context = {
                "dictionary_data":dictionary_data
            }  
            
        
        except:
            print("error not found")

            dictionary_data = {
                "error":word + " is not found. Please enter a valid word."
            }

            context = {
                "dictionary_data":dictionary_data
            } 

        return render(request, self.template_name, context)
