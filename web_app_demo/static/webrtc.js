const websocket = new WebSocket("ws://localhost:5678/");
const remoteVideo = document.getElementById('remoteVideo');

let makingOffer = false;
let ignoreOffer = false;
let isSettingRemoteAnswerPending = false;
let polite = false;


async function websocket_send(type, data) {

  console.log("sending ", type, data);

  let message = {
    "type": type,
    "data": data
  }

  let message_json = JSON.stringify(message);

  console.log(message_json);

  try {
    websocket.send(message_json);
  } catch (err) {
    console.error(err);
  }
}

function handleNegotiationNeededEvent() {

  console.log("Negotiation needed");

  myPeerConnection
    .createOffer()
    .then((offer) => myPeerConnection.setLocalDescription(offer))
    .then(() => {
      websocket_send(
        type = "offer",
        data =  myPeerConnection.localDescription,
      );
    })
    .catch(window.reportError);
}

function handleICECandidateEvent(event) {

  if (event.candidate == null) {
    return;
  }

  console.log("ICE candidate : ", event.candidate);

  candidate = event.candidate

  data = {
    address: candidate.address,
    candidate: candidate.candidate,
    component: candidate.component,
    foundation: candidate.foundation,
    port: candidate.port,
    priority: candidate.priority,
    protocol: candidate.protocol,
    relatedAddress: candidate.relatedAddress,
    relatedPort: candidate.relatedPort,
    sdpMLineIndex: candidate.sdpMLineIndex,
    sdpMid: candidate.sdpMid,
    tcpType: candidate.tcpType,
    type: candidate.type,
    usernameFragment: candidate.usernameFragment

  }

  if (data.address) {
    websocket_send(
      type = "ice",
      data = data,
    );
  }
}

function handleTrackEvent(event) {

  console.log("Track event");

  remoteVideo.srcObject = event.streams[0];
}


function handleICEConnectionStateChangeEvent(event) {
  console.log("ICE connection state change", myPeerConnection.iceConnectionState);
}

function handleSignalingStateChangeEvent(event) {
  console.log("Signaling state change", myPeerConnection.signalingState);
}

function handleICEGatheringStateChangeEvent(event) {
  console.log("ICE gathering state change", myPeerConnection.iceGatheringState);
}



function handleAnswer(answer) {

  console.log("received answer", answer);

  const desc = new RTCSessionDescription(answer);
  myPeerConnection.setRemoteDescription(desc).catch(window.reportError);
}

function handleNewICECandidateMsg(candidate_data) {

  console.log("received ICE candidate", candidate_data);

  const candidate = new RTCIceCandidate(candidate_data.candidate);

  myPeerConnection.addIceCandidate(candidate).catch(window.reportError);
}


const config = {
  iceServers: [
    {
      urls: "stun:stun.l.google.com:19302",
    },
  ],
};

const myPeerConnection = new RTCPeerConnection();
myPeerConnection.addTransceiver('video', { direction: 'recvonly' });

myPeerConnection.onicecandidate = handleICECandidateEvent;
myPeerConnection.ontrack = handleTrackEvent;
myPeerConnection.onnegotiationneeded = handleNegotiationNeededEvent;
myPeerConnection.oniceconnectionstatechange = handleICEConnectionStateChangeEvent;
myPeerConnection.onicegatheringstatechange = handleICEGatheringStateChangeEvent;
myPeerConnection.onsignalingstatechange = handleSignalingStateChangeEvent;

websocket.onmessage = async ({ data }) => {

  console.log("received ", data);

  let message_object = JSON.parse(data);

  let type = message_object["type"];
  let payload = message_object["data"];

  let description = type === "offer" || type === "answer" ? new RTCSessionDescription({ type, sdp: payload }) : null;
  let candidate = type === "ice" ? new RTCIceCandidate({ candidate: payload }) : null;

  switch (type) {
    case "offer":
      console.log("received offer");
      break;
    case "answer":
      handleAnswer(description);
      break;
    case "ice":
      handleNewICECandidateMsg(candidate);
      break;
  }
};

websocket.onopen = handleNegotiationNeededEvent;