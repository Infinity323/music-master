import { useEffect, useState } from 'react';

function useMicrophone(enabled) {
  const [mediaStream, setMediaStream] = useState(null);

  async function enableStream() {
    try {
      const media = await navigator.mediaDevices.getUserMedia({
        audio: true,
        video: false
      });
      setMediaStream(media);
    } catch(err) {
      console.error(err);
    }
  }

  useEffect(() => {
    if (!mediaStream) {
      enableStream();
    } else {
      return () => {
        mediaStream.getTracks().forEach(track => track.stop());
      }
    }
  }, [mediaStream]);

  useEffect(() => {
    if (enabled) enableStream();
    else if (!enabled && mediaStream) mediaStream.getTracks().forEach(track => track.stop());
  }, [enabled]);
  
  return mediaStream;
}

export default useMicrophone;