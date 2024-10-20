import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64
from pydub import AudioSegment
import json

## Conf part
conv_data_path = "conv_data/restaurant_1.json"


## Functions

@st.cache_data
def text_to_speech_segment(text):
    tts = gTTS(text=text, lang='fr')
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return AudioSegment.from_file(audio_fp, format="mp3")


@st.cache_data
def single_convo_segment(cnv_title, cnv_content):
    convo_segment = text_to_speech_segment(cnv_title + ".") + AudioSegment.silent(duration=1000)\
                     + text_to_speech_segment(cnv_content)
    return convo_segment


@st.cache_data
def decode_audio_segment(_audio_segment):
    audio_fp = BytesIO()
    _audio_segment.export(audio_fp, format="mp3")
    audio_fp.seek(0)
    audio_base64 = base64.b64encode(audio_fp.read()).decode("utf-8")
    return "data:audio/mp3;base64," + audio_base64


@st.cache_data
def single_convo(_single_convo_segment):
    return decode_audio_segment(_single_convo_segment)


@st.cache_data
def convo_playlist(_convo_segments):
    combined = AudioSegment.silent(duration=500)  # 0.5 second of silence at the start
    for segment in _convo_segments:
        combined += segment + AudioSegment.silent(duration=1500)  # Add 1.5 second of silence between clips

    return decode_audio_segment(combined)


# Load the conversations from json file
def load_conversation_data(conv_data_path):
    with open(conv_data_path) as json_file:
        return json.load(json_file)


## Display the streamlit page

conversations = load_conversation_data(conv_data_path)

st.write("Play entire list")
convo_segments = [single_convo_segment(convo['conv_title_fr'], convo['conv_content_fr']) for convo in conversations]
st.audio(convo_playlist(convo_segments), format='audio/mp3')

# Make a container for each conversation
for convo in conversations:
    c = st.container()
    colfr, colen = c.columns(2, gap="medium")

    colfr.subheader(convo['conv_title_fr'])
    colfr.write(convo['conv_content_fr'])

    colen.subheader(convo['conv_title_en'])
    colen.write(convo['conv_content_en'])

    audio_file = single_convo(single_convo_segment(convo['conv_title_fr'], convo['conv_content_fr']))
    c.audio(audio_file)
