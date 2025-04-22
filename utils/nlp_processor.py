import sys

from openai import OpenAI

from dashscope.audio.tts import SpeechSynthesizer

qian_wen_api = "your api key"
# 可选 https://dashscope.aliyuncs.com/compatible-mode/v1
qian_wen_url = "your url"

client = OpenAI(api_key=qian_wen_api,
                base_url=qian_wen_url)




def text_to_voice_llm(name,text):
    result = SpeechSynthesizer.call(model=f'sambert-{name}-v1',
                                    api_key=qian_wen_api,
                                    text= text,
                                    sample_rate=48000,
                                   format='wav')
    bin_voice = result.get_audio_data()
    return bin_voice

def polish_results_with_llm(messages):
    completion = client.chat.completions.create(
        model="qwen-max-latest",
        messages= messages,
        temperature=0.3,  # 降低随机性
        top_p=0.95
    )
    # print(completion.model_dump_json())
    result = completion.choices[0].message.content
    print("大模型润色回答", result)
    return result
