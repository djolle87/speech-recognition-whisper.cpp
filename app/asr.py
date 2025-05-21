import subprocess
import os
import re
import shutil
import logging
from pathlib import Path
import tempfile
import shlex

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def translate(audio_file, include_timestamps=False, save_files=True):
    """
    Transcribe an input audio file using whisper.cpp CLI.

    Args:
        audio_file (str or Path): Path to the input audio file.
        include_timestamps (bool): If True, include timestamps in the transcript.
        save_files (bool): If True, save intermediate and output files under data/tmp.

    Returns:
        str: Transcribed text or error message.
    """
    whisper_dir = Path("whisper.cpp")
    data_dir = Path("data/tmp")
    data_dir.mkdir(parents=True, exist_ok=True)

    if save_files:
        raw_audio = data_dir / "raw_input"
        converted_audio = data_dir / "input.wav"
        output_file = data_dir / "output.txt"
    else:
        raw_audio = audio_file
        converted_audio = Path(tempfile.mktemp(suffix=".wav"))
        output_file = Path(tempfile.mktemp(suffix=".txt"))

    try:
        logger.info(f"{'Saving' if save_files else 'Temporarily processing'} audio file: {audio_file}")

        shutil.copy(audio_file, raw_audio)
        logger.info(f"Copied input audio to: {raw_audio}")

        cmd_convert = f"ffmpeg -y -i {shlex.quote(str(raw_audio))} -ar 16000 -ac 1 -c:a pcm_s16le {shlex.quote(str(converted_audio))}"
        logger.info(f"Converting audio using command: {cmd_convert}")
        subprocess.run(cmd_convert, shell=True, check=True)
        logger.info(f"Audio converted and saved to: {converted_audio}")

        if save_files:
            cmd_whisper = (
                f"cd {shlex.quote(str(whisper_dir))} && "
                f"./build/bin/whisper-cli -f ../{shlex.quote(str(converted_audio))} -l ja "
                f"> ../{shlex.quote(str(output_file))}"
            )
        else:
            raise NotImplementedError("In-memory processing (save_files=False) is not implemented yet.")

        logger.info(f"Running whisper.cpp with command: {cmd_whisper}")
        subprocess.run(cmd_whisper, shell=True, check=True)
        logger.info(f"Transcription completed. Output written to: {output_file}")

        with output_file.open("r", encoding="utf-8") as f:
            transcript = f.read()
            logger.info("Transcript successfully read.")

        if not include_timestamps:
            transcript = re.sub(
                r"\s*\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\]\s*",
                " ", transcript
            ).strip()
            logger.info("Timestamps removed from transcript.")

        return transcript

    except subprocess.CalledProcessError as e:
        logger.error(f"Subprocess failed with return code {e.returncode}: {e.cmd}")
        return "An error occurred during transcription (subprocess failure)."

    except Exception as e:
        logger.exception("Unexpected error during transcription:")
        return "An unexpected error occurred during transcription."

    finally:
        if not save_files:
            for file in [raw_audio, converted_audio, output_file]:
                try:
                    if file.exists():
                        file.unlink()
                        logger.info(f"Deleted temporary file: {file}")
                except Exception as cleanup_err:
                    logger.warning(f"Failed to delete {file}: {cleanup_err}")
