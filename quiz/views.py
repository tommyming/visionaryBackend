from django.http import JsonResponse, HttpResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView
from quiz.serializers import (
    LearningSummarySerializer,
    LearningQuizSerializer,
    LearningOptionSerializer,
)
from quiz.models import LearningSummary, LearningQuiz, LearningOption
from google.cloud import speech
from pytube import YouTube
import ffmpeg
import io
import warnings
from langchain import PromptTemplate
import os
from langchain_google_vertexai import VertexAI


def transcribe_file(speech_file, language="en-US"):

    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio file into memory
    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio({"content": content})

    config = speech.RecognitionConfig(
        {
            "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
            "sample_rate_hertz": 16000,
            "language_code": language,
        }
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript


class QuizView(GenericAPIView):

    ls_queryset = LearningSummary.objects.all()
    lq_queryset = LearningQuiz.objects.all()
    lo_queryset = LearningOption.objects.all()

    ls_serializer_class = LearningSummarySerializer
    lq_serializer_class = LearningQuizSerializer
    lo_serializer_class = LearningOptionSerializer

    def post(self, request, *args, **krgs):

        url = request.data["url"]
        
        yt_obj = YouTube(url)
        
        yt_obj.streams.filter(progressive=True, file_extension="mp4").order_by(
            "resolution"
        ).desc().first().download(filename="tmp.mp4")

        ffmpeg.input("tmp.mp4").output("tmp.wav", ac=1, ar=16000).run()

        text = transcribe_file(speech_file="tmp.wav")

        model = VertexAI(model_name="gemini-pro")

        warnings.filterwarnings("ignore")
        
        message = """You are tutor of the course, you need to prepare the multiple choice exam question based on the lecture summary.
                Each multiple choice must have 4 option with one 1 correct option. You need to prepare in JSON format and insert into system later.

                Lecture Summary
                '''
                """ + text + """
                '''
            
                Prompt Result Return JSON Format
                {
                1 : {
                "question": [Question],
                "options": [List Of Option],
                "correct_option": [Correct Option],
                "correct_rationale": [Correct option explanation]
                },
                2: {
                "question": [Question],
                "options": [List Of Option],
                "correct_option": [Correct Option],
                "correct_rationale": [Correct option explanation]
                },
                N: {
                "question": [Question],
                "options": [List Of Option],
                "correct_option": [Correct Option],
                "correct_rationale": [Correct option explanation]
                }
                }
                """
                
        print(message)
        
        result = model.invoke(message)

        os.remove("tmp.mp4")
        os.remove("tmp.wav")

        return HttpResponse(result)
