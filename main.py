#!/home/bhanu2003/projects/ASR1/venv/bin/python3
"""
real-time voice assistant 
"""
import sys
sys.path.insert(0, '/home/bhanu2003/projects/ASR1')

from asterisk.agi import AGI
from asr.transcriber import transcribe
from llm.agent import get_response
from speech_tts.synthesizer import synthesize
import os
import time

CALL_RECORDING = "/tmp/call_audio_{}.wav"
TTS_REPLY = "/tmp/reply_{}.wav"

def main():
    try:
        agi = AGI()

        # Get unique identifier for this call
        call_id = agi.env['agi_uniqueid']
        safe_call_id = call_id.replace('.', '_')
        recording_file = CALL_RECORDING.format(safe_call_id)
        reply_file = TTS_REPLY.format(safe_call_id)

        agi.verbose("=== VOICE ASSISTANT STARTING ===")
        agi.verbose(f"Call ID: {call_id}")
        agi.verbose(f"Recording file: {recording_file}")
        
        # Answer the call
        agi.answer()
        agi.verbose("Call answered")

        # Start recording
        agi.verbose("Recording user speech...")
        recording_base = recording_file.replace('.wav', '')
        # Record audio - format: filename, format, escape_digits, timeout(ms)
        agi.appexec('Record', f'{recording_base}:wav,3,15')

        # Wait for file to be written
        time.sleep(1)
        
        # Check if recording exists and has content
        if not os.path.exists(recording_file):
            agi.verbose(f"ERROR: Recording file not found: {recording_file}")
            agi.hangup()
            return
        
        file_size = os.path.getsize(recording_file)
        agi.verbose(f"Recording saved: {recording_file} ({file_size} bytes)")
        
        if file_size < 1000:  # Less than 1KB means no real audio
            agi.verbose("ERROR: Recording too small, no audio captured")
            agi.hangup()
            return
        
        # Transcribe the audio
        agi.verbose("Transcribing...")
        try:
            user_text = transcribe(recording_file)
            agi.verbose(f"User said: {user_text}")
            
            if not user_text or len(user_text.strip()) == 0:
                agi.verbose("ERROR: Empty transcription")
                agi.hangup()
                return
                
        except Exception as e:
            agi.verbose(f"Transcription error: {e}")
            agi.hangup()
            return
        
        # Get LLM response
        agi.verbose("Getting LLM response...")
        try:
            response = get_response(user_text)
            agi.verbose(f"LLM Response: {response}")
            
            if not response or len(response.strip()) == 0:
                agi.verbose("ERROR: Empty LLM response")
                agi.hangup()
                return
                
        except Exception as e:
            agi.verbose(f"LLM error: {e}")
            agi.hangup()
            return
        
        # Synthesize speech
        agi.verbose("Synthesizing speech...")
        try:
            synthesize(response, reply_file)
            
            if not os.path.exists(reply_file):
                agi.verbose(f"ERROR: TTS file not created: {reply_file}")
                agi.hangup()
                return
                
            tts_size = os.path.getsize(reply_file)
            agi.verbose(f"TTS generated: {reply_file} ({tts_size} bytes)")
            
        except Exception as e:
            agi.verbose(f"TTS error: {e}")
            import traceback
            agi.verbose(traceback.format_exc())
            agi.hangup()
            return
        
        # Play the response back to the user IN THE SAME CALL
        agi.verbose("Playing response to caller...")
        reply_base = reply_file.replace('.wav', '')
        agi.stream_file(reply_base)
        
        agi.verbose("=== VOICE ASSISTANT COMPLETED ===")
        
        # Cleanup
        try:
            if os.path.exists(recording_file):
                os.remove(recording_file)
                agi.verbose(f"Cleaned up: {recording_file}")
            if os.path.exists(reply_file):
                os.remove(reply_file)
                agi.verbose(f"Cleaned up: {reply_file}")
        except Exception as e:
            agi.verbose(f"Cleanup error: {e}")
        
        # Hangup
        agi.hangup()
        
    except Exception as e:
        try:
            agi.verbose(f"FATAL ERROR in main: {e}")
            import traceback
            agi.verbose(traceback.format_exc())
        except:
            pass
        raise

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        print(f"FATAL ERROR: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)