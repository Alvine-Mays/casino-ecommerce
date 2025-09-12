import { useEffect, useRef, useState } from 'react'

export default function Scanner({ onCode }) {
  const videoRef = useRef(null)
  const [active, setActive] = useState(false)
  const [supported, setSupported] = useState(false)
  useEffect(() => { setSupported('BarcodeDetector' in window) }, [])

  useEffect(() => {
    let stream
    let raf
    let detector
    async function start() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        if (videoRef.current) videoRef.current.srcObject = stream
        await videoRef.current.play()
        detector = new window.BarcodeDetector({ formats: ['qr_code', 'code_128', 'code_39'] })
        const scan = async () => {
          if (!active) return
          try {
            const bitmap = await createImageBitmap(videoRef.current)
            const codes = await detector.detect(bitmap)
            if (codes && codes[0]) {
              onCode(codes[0].rawValue)
              stop()
              return
            }
          } catch (e) {}
          raf = requestAnimationFrame(scan)
        }
        raf = requestAnimationFrame(scan)
      } catch (e) {
        console.warn('Scanner init failed', e)
      }
    }
    function stop() {
      setActive(false)
      if (raf) cancelAnimationFrame(raf)
      if (stream) stream.getTracks().forEach(t => t.stop())
      stream = null
    }
    if (active && supported) start()
    return () => stop()
  }, [active, supported, onCode])

  if (!supported) return <div className="text-sm text-gray-500">Scanner non supporté, utilisez la saisie manuelle.</div>

  return (
    <div className="space-y-2">
      <div className="flex gap-2 items-center">
        <button className={`px-3 py-2 rounded ${active?'bg-red-600 text-white':'bg-gray-200'}`} onClick={()=>setActive(!active)}>{active?'Arrêter':'Scanner'}</button>
      </div>
      <video ref={videoRef} className={`w-full max-w-sm rounded ${active?'block':'hidden'}`} muted playsInline />
    </div>
  )
}
