def synthesize(text: str, output_path: str = "output.wav"):
    from TTS.api import TTS

    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
    tts.tts_to_file(text=text, file_path=output_path)
