import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64
from pydub import AudioSegment
import json


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
                    + text_to_speech_segment(cnv_content) \
                    + AudioSegment.silent(duration=1500)  # Add 1.5 second of silence at the end
    return convo_segment


@st.cache_data
def sentence_group_segment(gr_title, sentences):
    sentences_segment = text_to_speech_segment(gr_title + ".") + AudioSegment.silent(duration=1000)
    for sn in sentences:
        sentences_segment += text_to_speech_segment(sn) + AudioSegment.silent(duration=500)
    return sentences_segment + AudioSegment.silent(duration=1500)


def decode_audio_segment(_audio_segment):
    audio_fp = BytesIO()
    _audio_segment.export(audio_fp, format="mp3")
    audio_fp.seek(0)
    audio_base64 = base64.b64encode(audio_fp.read()).decode("utf-8")
    return "data:audio/mp3;base64," + audio_base64


def single_convo(cnv_title, cnv_content):
    segment = single_convo_segment(cnv_title, cnv_content)
    return decode_audio_segment(segment)


def convo_playlist(_convo_segments):
    combined = AudioSegment.silent(duration=500)  # 0.5 second of silence at the start
    for segment in _convo_segments:
        combined += segment

    return decode_audio_segment(combined)


# Load the conversations from json file
def load_conversation_data(conv_data_path):
    with open(conv_data_path) as json_file:
        return json.load(json_file)


def display_audio_pair(audio_file):
    inc1 = st.container()
    col11, col21 = inc1.columns([1, 3], gap="small", vertical_alignment='center')
    col11.write(":black_right_pointing_triangle_with_double_vertical_bar: Play once")
    col21.audio(audio_file, loop=False)

    inc2 = st.container()
    col12, col22 = inc2.columns([1, 3], gap="small", vertical_alignment='center')
    col12.write(":repeat: Play continuously")
    col22.audio(audio_file, loop=True)


def display_conv_page(page_data):
    st.image(page_data['himage'], use_column_width='always')
    st.header(page_data['title'])

    conversations = load_conversation_data(page_data['content'])

    st.write("Play all")
    st.audio(
        convo_playlist([single_convo_segment(convo['conv_title_fr'], convo['conv_content_fr']) for convo in conversations]),
        format='audio/mp3'
    )

    st.divider()

    # Make a container for each conversation
    for convo in conversations:
        c = st.container()
        colfr, colen = c.columns(2, gap="medium")

        colfr.subheader(convo['conv_title_fr'])
        colfr.write(convo['conv_content_fr'])

        colen.subheader(convo['conv_title_en'])
        colen.write(convo['conv_content_en'])

        audio_file = single_convo(convo['conv_title_fr'], convo['conv_content_fr'])
        display_audio_pair(audio_file)


def display_sentences_page(page_data):
    st.image(page_data['himage'], use_column_width='always')
    st.header(page_data['title'])

    sentence_groups = load_conversation_data(page_data['content'])

    for sg in sentence_groups:
        colfr, colen = st.columns(2)
        colfr.subheader(sg['sentences_group_fr'])
        colen.subheader(sg['sentences_group_en'])

        for pair in sg['content']:
            colfr, colen = st.columns(2)
            colfr.write(pair['sentence_fr'])
            colen.write(pair['sentence_en'])

        sentences = [pair['sentence_fr'] for pair in sg['content']]
        audio_file = decode_audio_segment(sentence_group_segment(sg['sentences_group_fr'], sentences))
        display_audio_pair(audio_file)