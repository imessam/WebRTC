import sys
import os 
import asyncio

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
if base_path not in sys.path:
    sys.path.insert(0, base_path)

# from libs.another_module.python.modules import *

from modules.webrtc_signaling import WebRTCSignaling

async def main():

    if len(sys.argv) < 2:
        print("Usage: python demo.py <video_path or live_location_url> <config_file>")
        return 1
    
    video_path = sys.argv[1]
    config_file = sys.argv[2] if len(sys.argv) > 2 else ""

    webrtc_signaling = WebRTCSignaling(server_ip="pai1.powercom.co",video_path=video_path, config_file_path=config_file)

    if await webrtc_signaling.start() != WebRTCSignaling.RETURN_STATUS.OK_STARTED:
        return 1
    
    user_input = ""

    while user_input != "q":
        user_input = input("Press q to quit")

    if await webrtc_signaling.stop() != WebRTCSignaling.RETURN_STATUS.OK_STOPPED:
        return 1

    return 0

if __name__ == "__main__":
    asyncio.run(main())