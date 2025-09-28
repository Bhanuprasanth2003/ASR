from asr.transcriber import transcribe
from llm.agent import get_response
from speech_tts.synthesizer import synthesize
from asterisk.audio_stream import record_call
import subprocess

CALL_RECORDING = "/tmp/call_audio.wav"
TTS_REPLY = "/tmp/reply.wav"

def run_pipeline():
    print("Recording call...")
    record_call(CALL_RECORDING)

    print("Transcribing...")
    user_text = transcribe(CALL_RECORDING )
    print("User said:", user_text)

    response = get_response(user_text)
    print("LLM Response:", response)

    print("Synthesizing speech...")
    synthesize(response, TTS_REPLY)

    print("Playing response to caller...")
    
    subprocess.run([
        "sudo", "asterisk", "-rx",
        f'channel originate local/1001@local application Playback({TTS_REPLY[:-4]})'
    ])

if __name__ == "__main__":
    run_pipeline()
