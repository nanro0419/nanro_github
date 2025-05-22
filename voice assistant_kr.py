# voice assistant
# Voice recognition -> grab information about weather, temperature, current date, and current time -> voice generation
# Functions to make
# 1. voice recognition
# 2. grab weather & temp information
# 3. grab date & time information
# 4. voicve generation
# 6. find keyword from the voice recognition


# packages
# voice recognition: speech_recognition (pip install SpeechRecognition), PyAydui(pip install pyaudio)
# voice generation: gtts (pip install gtts), pydub (pip install pydub), ffmpeg(conda install ffmpeg)
# date & time: Timezone pytz package (pip install pytz)
# 세계 시간 Timezone pytz 패키지 이용 (pip install pytz)

import gtts
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import requests


# 음성인식 함수
def voice_recognition() -> str:
    """recognize the voice and translate into string"""
    import speech_recognition as sr

    r = sr.Recognizer()  # 음성자료가 담길 객체생성성
    microphone = sr.Microphone()  # 마이크 활성

    while True:
        with microphone as source:
            r.adjust_for_ambient_noise
            print("음성 명령을 기다리는 중입니다")
            my_audio = r.listen(source)

            try:
                txt = r.recognize_google(my_audio, language="ko")

            except:
                print("음성인식 실패")

            else:
                return txt


# 키워드를 찾아서 도시 이름을 반환하는 함수
def find_keyword(keywords: list[str], sentence: str, default: str = "서울") -> str:

    for city in keywords:
        if sentence.find(city) != -1:
            return city

    return default


# function for voice generation


def ai_voice(message: str):

    import gtts
    from pydub import AudioSegment
    from pydub.playback import play
    from io import BytesIO

    tts = gtts.gTTS(message, lang="ko")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp = BytesIO(fp.getvalue())
    ai_audio = AudioSegment.from_file(fp, format="mp3")
    play(ai_audio)


# Function for getting city name, weather, and temperature
def grab_weather_temp(city: str):
    import requests

    API_KEYS = "1daa6134e96568a1ec9a8de7bf7ba73a"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    LANGUAGE = "kr"

    city_name = cities_dict_weather[city]
    request_url = f"{BASE_URL}?appid={API_KEYS}&q={city_name}&lang={LANGUAGE}"

    response = requests.get(request_url)
    if response.status_code == 200:
        data = response.json()
        city_name = data["name"]
        weather = data["weather"][0]["description"]
        temperature = round(data["main"]["temp"] - 273.15, 2)
        return city_name, weather, temperature
    else:
        return "데이터를 가져올 수 없습니다."


# Function for getting date and current time
def grab_datetime(city: str) -> list:
    from datetime import datetime, timedelta
    from pytz import timezone

    # 맨마지막에 .year, .month, .day, .hour, .minute 을 붙이면 된다.
    tz = timezone(cities_dict[city])
    current_year = datetime.now().astimezone(tz).year
    current_month = datetime.now().astimezone(tz).month
    current_day = datetime.now().astimezone(tz).day
    current_hour = datetime.now().astimezone(tz).hour
    current_minute = datetime.now().astimezone(tz).minute

    return current_year, current_month, current_day, current_hour, current_minute


# function list
# def voice_recognition() -> str:
# def find_keyword(keywords: list[str], sentence: str, default: str = "서울") -> str:
# def grab_weather_temp(city: str):
# def grab_datetime(city: str) -> list:
# def ai_voice(message: str):

# voice assistant code
# weather or temp -> find city -> grab weather or temp of input city

cities_dict = {
    "서울": "Asia/Seoul",
    "뉴욕": "America/New_York",
    "로스앤젤레스": "America/Los_Angeles",
    "파리": "Europe/Paris",
    "런던": "Europe/London",
}

cities_dict_weather = {
    "서울": "seoul",
    "뉴욕": "new york",
    "로스앤젤레스": "los angeles",
    "파리": "paris",
    "런던": "london",
}

while True:
    user_command = voice_recognition()
    print("인식결과 :", user_command)
    city = find_keyword(
        keywords=cities_dict.keys(), sentence=user_command, default="서울"
    )
    if "날씨" in user_command:
        weather_temp = grab_weather_temp(city)
        message = f"오늘 {city}의 날씨는 {weather_temp[1]} 입니다. 온도는 {weather_temp[2]}도 입니다."

    elif "시간" in user_command:
        time = grab_datetime(city)
        message = f"오늘 {city} 기준 현재 시간은 {time[3]}시 {time[4]}분 입니다."

    elif "날짜" in user_command:
        date = grab_datetime(city)
        message = f"오늘 {city} 기준 오늘은 {date[0]}년 {date[1]}월 {date[2]}일 입니다."

    elif "종료" in user_command:
        message = "종료합니다."
        ai_voice(message)
        break

    print(message)
    ai_voice(message)
