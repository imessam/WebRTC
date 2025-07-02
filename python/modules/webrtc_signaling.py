import os
import sys

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if base_path not in sys.path:
    sys.path.insert(0, base_path)

from libs.VideoInput.python.modules.i_video_input import IVideoInput
from libs.VideoInput.python.modules.video_input_factory import VideoInputFactory

import asyncio
import threading
import json
import cv2
import yaml

from enum import Enum
from queue import Queue
from websockets.asyncio.server import serve, Server
from websockets.asyncio.server import ServerConnection

from libs.aiortc.src.aiortc import (
    RTCIceCandidate,
    RTCPeerConnection,
    RTCRtpCodecParameters,
    RTCRtpHeaderExtensionParameters,
    RTCSessionDescription,
    VideoStreamTrack,
)
from aiortc.rtcrtpparameters import RTCRtpSendParameters, RTCRtpEncodingParameters, RTCRtpHeaderExtensionParameters

from av import VideoFrame

class FileVideoStreamTrack(VideoStreamTrack):
    """
    A video track that returns an animated flag.
    """

    def __init__(self, video_path : str):
        super().__init__()  # don't forget this!
        self.counter = 0

        self.user_name = ""
        

        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            raise Exception("Video file not found")
        

    
    async def recv(self): # type: ignore

        pts, time_base = await self.next_timestamp()

        ret, frame = self.cap.read()

        if not ret:
            return
        
        video_frame = VideoFrame.from_ndarray(frame, format="bgr24") # type: ignore

        video_frame.pts = pts
        video_frame.time_base = time_base
        self.counter += 1

        return video_frame
    
    def stop(self):
        self.cap.release()
    
class LiveVideoStreamTrack(VideoStreamTrack):

    """
    A video track that returns an animated flag.
    """

    def __init__(self, location_path : str, config_file_path : str):

        super().__init__()  # don't forget this!

        self.counter = 0

        self.user_name = ""

        self.location = location_path
        self.config_file = config_file_path

        with open(self.config_file, 'r') as file:
            config = yaml.safe_load(file)

        status, self.video_input = VideoInputFactory.createVideoInput(self.location, config, IVideoInput.BACKEND.GSTREAMER)

        if status != VideoInputFactory.RETURN_STATUS.OK:
            print("Error creating video input")
            return
        
        self.video_input_thread = threading.Thread(target=asyncio.run, args=(self.video_input_loop(),))

        self.current_frame = None

        self.frames_queue = Queue()

        self.video_input_thread.start()

        self._is_quit = False
        
    async def video_input_loop(self):

        print("Starting video input loop")

        if self.video_input is None:
            print("Video input is None")
            return
        
        if  self.video_input.start() != IVideoInput.RETURN_STATUS.OK_STARTED:
            print("Error starting video input")
            return
        
        while not self._is_quit:

            status, frame = self.video_input.readFrame()

            if frame is None:
                break
            
            # self.frames_queue.put(frame)
            self.current_frame = frame

            self.counter += 1


        self.video_input.stop()

        print("Video input loop stopped")


        return 
        
    
    async def recv(self): # type: ignore

        # if self.frames_queue.empty():
        #     return

        # frame = self.frames_queue.get()

        frame = self.current_frame

        print(f"Received frame {self.counter} from {self.user_name}")

        if frame is None:
            return
        
        pts, time_base = await self.next_timestamp()

        video_frame = VideoFrame.from_ndarray(frame, format="bgr24") # type: ignore

        video_frame.pts = pts
        video_frame.time_base = time_base
        self.counter += 1

        return video_frame
    
    

class WebRTCSignaling:

    class RETURN_STATUS(Enum):

        OK = 0
        OK_STARTED = 1
        OK_STOPPED = 2
        
        ERROR = 3
        ERROR_CANNOT_START = 4
        ERROR_CANNOT_STOP = 5

    def __init__(self, server_ip: str = "localhost", server_port: int = 5678, video_path : str = "", config_file_path : str = "") -> None:

        self.video_path : str = video_path
        self.config_file_path : str = config_file_path

        self.is_live : bool = self.config_file_path != ""
        
        self.server_ip : str = server_ip
        self.server_port : int = server_port

        self.server : Server 
        self.server_thread : threading.Thread

        self._is_server_stopped : bool = False

        self._my_name = "WebRTCSignaling"

        self.rtc_connections = {}

        self.video_track = (LiveVideoStreamTrack(location_path=self.video_path, config_file_path=self.config_file_path) if self.is_live 
                            else FileVideoStreamTrack(video_path=self.video_path))

    async def start(self) -> RETURN_STATUS:

        print(f"{self._my_name} :: Starting webrtc signaling server on {self.server_ip}:{self.server_port}")

        status = WebRTCSignaling.RETURN_STATUS.OK_STARTED

        self.server_thread = threading.Thread(target=asyncio.run, args=(self.loop(),))
        self.server_thread.start()

        print(f"{self._my_name} ::  webrtc signaling server started on {self.server_ip}:{self.server_port}")

        return status
    
    async def loop(self):

        print(f"{self._my_name} :: Starting webrtc signaling server loop on {self.server_ip}:{self.server_port}")

        self.server = await serve(self.handle_connection, self.server_ip, self.server_port)

        await self.server.wait_closed()

        print(f"{self._my_name} ::  webrtc signaling server loop stopped on {self.server_ip}:{self.server_port}")

        return 

    async def stop(self) -> RETURN_STATUS:

        print(f"{self._my_name} :: Stopping webrtc signaling server on {self.server_ip}:{self.server_port}")

        status = WebRTCSignaling.RETURN_STATUS.OK_STOPPED

        if self.server is None:
            status = WebRTCSignaling.RETURN_STATUS.ERROR_CANNOT_STOP

            print(f"{self._my_name} ::  webrtc signaling server cannot be stopped on {self.server_ip}:{self.server_port} :: {self.getStatusMessage(status)}")

            return status
        
        self._is_server_stopped = True
        
        self.server.close()

        self.server_thread.join()

        print(f"{self._my_name} ::  webrtc signaling server stopped on {self.server_ip}:{self.server_port}")

        return status
    

    async def handle_connection(self, websocket : ServerConnection):

        print(f"{self._my_name} :: New connection from {websocket.remote_address}")

        if self._is_server_stopped:
            print(f"{self._my_name} :: server is stopped")
 

        peer_connection = RTCPeerConnection() if self.rtc_connections.get(websocket.remote_address, None) is None else self.rtc_connections[websocket.remote_address]

        self.video_track.user_name = websocket.remote_address

        peer_connection.addTrack(self.video_track)

        self.rtc_connections[websocket.remote_address] = peer_connection


        while True:


            try:
                message_json = await websocket.recv()
            except Exception as e:
                print(f"{self._my_name} :: No message received from {websocket.remote_address} :: {e}")

                self.rtc_connections.pop(websocket.remote_address)

                senders = peer_connection.getSenders()

                for sender in senders:
                    sender.replaceTrack(None)

                peer_connection.cancel()
                await peer_connection.close()

                break

            print(f"{self._my_name} :: Received message: {message_json} from {websocket.remote_address}")

            message = json.loads(message_json)

            if message["type"] == "offer":

                offer = message["data"]

                type = offer["type"]
                sdp = offer["sdp"]

                print(f"{self._my_name} :: Received offer {offer} from {websocket.remote_address}")

                @peer_connection.on("onicecandidate")
                async def on_ice(candidate):
                    print(f"{self._my_name} :: on ICE candidate : {candidate} from {websocket.remote_address}")
                    await websocket.send(json.dumps({
                        "type": "ice",
                        "data": candidate
                    }))

                @peer_connection.on("track")
                def on_track(track):
                    print(f"{self._my_name} :: on Track {track} from {websocket.remote_address}")

                @peer_connection.on("onnegotiationneeded")
                async def on_negotiation_needed():
                    print(f"{self._my_name} :: on Negotiation needed from {websocket.remote_address}")

                    offer = await peer_connection.createOffer()

                    print(f"{self._my_name} :: Created offer {offer} from {websocket.remote_address}")

                    await peer_connection.setLocalDescription(offer)

                    offer = {
                        "type": "offer",
                        "data": peer_connection.localDescription.sdp
                    }

                    await websocket.send(json.dumps(offer))

                    print(f"{self._my_name} :: Sent offer to {websocket.remote_address}")

                @peer_connection.on("onremovetrack")
                def on_remove_track(track):
                    print(f"{self._my_name} :: on Remove track : {track} from {websocket.remote_address}")

                @peer_connection.on("oniceconnectionstatechange")
                def on_ice_connection_state_change():
                    print(f"{self._my_name} :: on  ICE connection state change : {peer_connection.iceConnectionState} from {websocket.remote_address}")

                @peer_connection.on("onicegatheringstatechange")
                def on_ice_gathering_state_change():
                    print(f"{self._my_name} :: on ICE gathering state change : {peer_connection.iceGatheringState} from {websocket.remote_address}")

                @peer_connection.on("onsignalingstatechange")
                def on_signaling_state_change():
                    print(f"{self._my_name} :: on Signaling state change : {peer_connection.signalingState} from {websocket.remote_address}")

                await peer_connection.setRemoteDescription(RTCSessionDescription(sdp=sdp, type="offer"))

                print(f"{self._my_name} :: Set remote description {peer_connection.remoteDescription} from {websocket.remote_address}")

                answer = await peer_connection.createAnswer()
                    
                print(f" {self._my_name} :: Created answer {answer} from {websocket.remote_address}")

                await peer_connection.setLocalDescription(answer)

                answer = {
                    "type": "answer",
                    "data": peer_connection.localDescription.sdp
                }

                await websocket.send(json.dumps(answer))

                print(f"{self._my_name} :: Sent answer to {websocket.remote_address}")

            elif message["type"] == "ice":
                
                data = message["data"]

                candidate = RTCIceCandidate(
                    component=data["component"],
                    foundation=data["foundation"],
                    ip=data["address"],
                    port=data["port"],
                    priority=data["priority"],
                    protocol=data["protocol"],
                    type=data["type"],
                    tcpType=data["tcpType"],
                    relatedAddress=data["relatedAddress"],
                    relatedPort=data["relatedPort"],
                    sdpMLineIndex=data["sdpMLineIndex"],
                    sdpMid=data["sdpMid"],
                )

                print(f"{self._my_name} :: Received candidate {candidate} from {websocket.remote_address}")

                if websocket.remote_address not in self.rtc_connections:
                    print(f"{self._my_name} :: Peer connection not found for {websocket.remote_address}")
                    return

                peer_connection : RTCPeerConnection = self.rtc_connections[websocket.remote_address]
                
                print(f"{self._my_name} :: Adding ice candidate {candidate} from {websocket.remote_address}")

                await peer_connection.addIceCandidate(candidate)

        
        print(f"{self._my_name} :: Connection closed from {websocket.remote_address}")
            
        return   

    def getStatusMessage(self, status: RETURN_STATUS) -> str:

        mapping = {
            WebRTCSignaling.RETURN_STATUS.OK: "OK",
            WebRTCSignaling.RETURN_STATUS.OK_STARTED: "OK started",
            WebRTCSignaling.RETURN_STATUS.OK_STOPPED: "OK stopped",
            WebRTCSignaling.RETURN_STATUS.ERROR: "Error",
            WebRTCSignaling.RETURN_STATUS.ERROR_CANNOT_START: "Error cannot start",
            WebRTCSignaling.RETURN_STATUS.ERROR_CANNOT_STOP: "Error cannot stop",
        }
        return mapping.get(status, "Unknown error")
