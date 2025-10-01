def synthesize(text: str, output_path: str = "output.wav"):
    import subprocess
    import os
    from TTS.api import TTS

    # Generate TTS to a temporary file
    temp_path = output_path.replace('.wav', '_temp.wav')
    
    # Generate speech using Coqui TTS
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
    tts.tts_to_file(text=text, file_path=temp_path)
    
    # Convert to 8kHz mono WAV for Asterisk compatibility
    subprocess.run([
        'ffmpeg', '-y', '-i', temp_path,
        '-ar', '8000',           # Sample rate: 8kHz
        '-ac', '1',              # Mono audio
        '-acodec', 'pcm_s16le',  # 16-bit PCM
        output_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Clean up temp file
    if os.path.exists(temp_path):
        os.remove(temp_path)