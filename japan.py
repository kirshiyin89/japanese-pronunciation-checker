import requests
import json
import pykakasi
import streamlit as st
import random
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from recorder import record_audio, read_audio
import SessionState


# Wit speech API endpoint
API_ENDPOINT = 'https://api.wit.ai/'
API_FUNCTION_SPEECH = 'speech'

# Wit API token
wit_access_token = 'VPEZHKEUXSSOGT4EVCO5Z5YHBBIYZSVQ'

def recognize_speech(audiofile, duration):
    
    record_audio(duration, audiofile)

    audio = read_audio(audiofile)

    headers = {'authorization': 'Bearer ' + wit_access_token,
               'Content-Type': 'audio/wav'}

    resp = requests.post(API_ENDPOINT+API_FUNCTION_SPEECH, headers = headers,
                         data = audio)

    data = json.loads(resp.content)

    print(data)
    # return the text from data response
    return data['text'] if 'text' in data else ''


def get_romaji(duration):
    text =  recognize_speech('myspeech.wav', duration)
    romaji = ''
    if text:
    	print("\nYou said: {}".format(text))
    	print("**************************************")    
    	kks = pykakasi.kakasi()
    	result = kks.convert(text)
    	for item in result:
        	print("{}[{}] ".format(item['orig'], item['hepburn'].capitalize()), end='')
        	romaji += item['hepburn']
        	print()        
    return romaji

def evaluate_speech(target_word, user_input):
    if user_input == target_word.split('[')[0]:
        return 'Correct'
    else:
        return 'Incorrect'

def select_word_from_list():
    words_file = open("words.txt", "r")
    word = words_file.readlines()
    return random.choice(word).strip()
    


if __name__ == "__main__":

    st.sidebar.title("Record Duration")
    # choose duration from 1 to 10 where 4 is default
    duration = st.sidebar.slider("Choose Duration", 1, 10, 4)
    st.title('Japanese Pronunciation Checker')

    result_message = st.empty()
    target_word_message = st.empty()
    session_state = SessionState.get(selected_word='')
    if not session_state.selected_word:
        session_state.selected_word = select_word_from_list()

    target_word_message.text('Say in Japanese: ' + session_state.selected_word)
    record_button = Button(label="Speak", width=100)

    user_input = ''
    
    if st.button("Try another one"):
        session_state.selected_word = select_word_from_list()
        target_word_message.text('Say in Japanese: ' + session_state.selected_word)

    if st.button("Record speech"):
        with st.spinner("Say " + session_state.selected_word):
            user_input = get_romaji(duration)
            if user_input != '':
            	result_message.text('You said: ' + user_input + ' which is: ' + evaluate_speech(session_state.selected_word, user_input))
            else:
            	result_message.text("Unrecognized audio. Try again.")

    

