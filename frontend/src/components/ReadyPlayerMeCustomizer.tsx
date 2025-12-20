import { useEffect, useRef, useState } from 'react'

interface Props {
  onSave: (avatarUrl: string) => void
}

export default function ReadyPlayerMeCustomizer({ onSave }: Props) {
  const iframeRef = useRef<HTMLIFrameElement>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Ready Player Me Application ID (환경변수 또는 기본값)
  const RPM_SUBDOMAIN = import.meta.env.VITE_READYPLAYERME_SUBDOMAIN || 'demo'

  useEffect(() => {
    // iframe에서 메시지를 받는 이벤트 리스너
    const handleMessage = (event: MessageEvent) => {
      console.log('📨 Received message:', event.data)
      const data = event.data

      // 1. URL 문자열로 직접 전송되는 경우 (일부 Ready Player Me 버전)
      if (typeof data === 'string' && data.includes('readyplayer.me')) {
        console.log('✅ Ready Player Me 캐릭터 URL 수신:', data)
        onSave(data)
        return
      }

      // 2. 이벤트 객체 형식으로 전송되는 경우
      if (data?.source !== 'readyplayerme') {
        return
      }

      console.log('✅ Ready Player Me event:', data.eventName)

      // 캐릭터 생성 완료 이벤트
      if (data.eventName === 'v1.avatar.exported') {
        const avatarUrl = data.data.url
        console.log('✅ Ready Player Me 캐릭터 생성 완료:', avatarUrl)
        onSave(avatarUrl)
      }

      // iframe 로딩 완료
      if (data.eventName === 'v1.frame.ready') {
        console.log('✅ Frame ready!')
        setIsLoading(false)
      }
    }

    window.addEventListener('message', handleMessage)

    // 타임아웃 설정: 10초 후에도 로딩 중이면 강제로 로딩 해제
    const timeout = setTimeout(() => {
      console.warn('⚠️ Timeout: Frame not ready after 10s, hiding loader anyway')
      setIsLoading(false)
    }, 10000)

    return () => {
      window.removeEventListener('message', handleMessage)
      clearTimeout(timeout)
    }
  }, [onSave])

  // frameApi: 공식 파라미터 - iframe 이벤트 통신 활성화
  const iframeUrl = `https://${RPM_SUBDOMAIN}.readyplayer.me/avatar?frameApi`

  console.log('🔍 RPM Subdomain:', RPM_SUBDOMAIN)
  console.log('🔍 RPM iframe URL:', iframeUrl)

  return (
    <div style={{ width: '100%', height: '600px', position: 'relative' }}>
      {isLoading && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: '#f5f5f5',
            zIndex: 10
          }}
        >
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2em', marginBottom: '10px' }}>⏳</div>
            <div style={{ color: '#667eea', fontWeight: '600' }}>
              MATE.AI 로딩 중...
            </div>
          </div>
        </div>
      )}

      <iframe
        ref={iframeRef}
        src={iframeUrl}
        allow="camera *; microphone *"
        style={{
          width: '100%',
          height: '100%',
          border: '2px solid #667eea',
          borderRadius: '12px'
        }}
      />
    </div>
  )
}
