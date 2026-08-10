import asyncio
import os
import tempfile

def text_to_speech(text: str, voice: str = "en-US-AvaNeural") -> str:
    """
    Converts text to speech audio using edge-tts (or gTTS fallback).
    Returns path to the generated audio file (.mp3).
    """
    # Create temp output file
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, f"serene_response_{os.urandom(4).hex()}.mp3")
    
    try:
        import edge_tts
        
        async def _generate():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
            
        asyncio.run(_generate())
        return output_path
        
    except Exception as e:
        print(f"[TTS Notice] edge-tts error or fallback: {e}. Falling back to gTTS...")
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            return output_path
        except Exception as gtts_err:
            raise RuntimeError(f"Both edge-tts and gtts failed: {gtts_err}")

if __name__ == "__main__":
    path = text_to_speech("Hello, I am Serene. I am glad to meet you.")
    print(f"Generated TTS file at: {path}")
