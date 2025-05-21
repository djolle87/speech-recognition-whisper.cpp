import logging
from app.interface import build_interface

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Launching Gradio interface...")
    iface = build_interface()
    iface.launch(debug=True)
