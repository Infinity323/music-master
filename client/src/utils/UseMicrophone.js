import { useEffect, useState } from 'react';

function useMicrophone() {
  const [mediaStream, setMediaStream] = useState(null);

  useEffect(() => {
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

    if (!mediaStream) {
      enableStream();
    } else {
      return () => {
        mediaStream.getTracks().forEach(track => track.stop());
      }
    }
  }, [mediaStream])
  
  return mediaStream;
}

export default useMicrophone;