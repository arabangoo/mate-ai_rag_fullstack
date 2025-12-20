import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

interface Props {
  characterId: string
  character: any
  onCharacterUpdate?: (characterId: string) => void
}

export default function ChatInterface({ characterId, character, onCharacterUpdate }: Props) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [affectionGained, setAffectionGained] = useState<number | null>(null)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [uploadedFilePreview, setUploadedFilePreview] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploadedFile(file)

    // 이미지 파일인 경우 미리보기 생성
    if (file.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setUploadedFilePreview(e.target?.result as string)
      }
      reader.readAsDataURL(file)
    } else {
      setUploadedFilePreview(null)
    }
  }

  const removeFile = () => {
    setUploadedFile(null)
    setUploadedFilePreview(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const sendMessage = async () => {
    if (!input.trim() && !uploadedFile) return

    let messageContent = input
    if (uploadedFile) {
      messageContent += `\n[첨부파일: ${uploadedFile.name}]`
    }

    const userMessage: Message = {
      role: 'user',
      content: messageContent,
      timestamp: new Date().toISOString()
    }

    setMessages([...messages, userMessage])
    const currentInput = input
    const currentFile = uploadedFile
    setInput('')
    setUploadedFile(null)
    setUploadedFilePreview(null)
    setIsTyping(true)

    try {
      // 파일이 있으면 먼저 업로드
      if (currentFile) {
        const formData = new FormData()
        formData.append('file', currentFile)

        await axios.post('http://localhost:8000/api/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      }

      const response = await axios.post(`http://localhost:8000/api/character/${characterId}/chat`, {
        message: currentInput || `이 ${currentFile?.type.startsWith('image/') ? '이미지' : '파일'}에 대해 이야기해줘`
      })

      const aiMessage: Message = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date().toISOString()
      }

      setMessages(prev => [...prev, aiMessage])

      // Show affection gained notification
      if (response.data.affection_gained > 0) {
        setAffectionGained(response.data.affection_gained)
        setTimeout(() => setAffectionGained(null), 3000)
      }

      // Update character data if callback provided
      if (onCharacterUpdate) {
        onCharacterUpdate(characterId)
      }
    } catch (error) {
      console.error('메시지 전송 실패:', error)
      alert('메시지 전송에 실패했습니다.')
    } finally {
      setIsTyping(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }
  
  const getStageKorean = (stage: string) => {
    const stages: { [key: string]: string } = {
      stranger: '처음 만난 사이',
      acquaintance: '안면이 있는 사이',
      friend: '친구',
      close_friend: '가까운 친구',
      romantic: '연인 ❤️'
    }
    return stages[stage] || stage
  }

  return (
    <>
    <div className="chat-interface" style={{display: 'flex', height: '100vh', background: '#f8f9fa'}}>
      {/* Left Panel - Character Profile */}
      <div style={{
        width: '320px',
        background: 'white',
        borderRight: '2px solid #e0e0e0',
        padding: '30px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
      }}>
        {/* Character Image */}
        <div style={{
          width: '200px',
          height: '200px',
          borderRadius: '50%',
          background: character.imageDataUrl
            ? `url(${character.imageDataUrl}) center/cover`
            : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          marginBottom: '20px',
          boxShadow: '0 8px 24px rgba(102, 126, 234, 0.3)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '6em'
        }}>
          {!character.imageDataUrl && (character.gender === 'female' ? '👩' : character.gender === 'male' ? '👨' : '🧑')}
        </div>

        {/* Character Info */}
        <h2 style={{margin: '10px 0', fontSize: '1.8em', color: '#2c3e50', textAlign: 'center'}}>
          {character.name}
        </h2>
        <p style={{margin: '5px 0', fontSize: '1.1em', color: '#7f8c8d'}}>
          {character.age}세 • {character.gender === 'female' ? '여성' : '남성'}
        </p>

        <div style={{
          width: '100%',
          marginTop: '30px',
          padding: '20px',
          background: '#f8f9fa',
          borderRadius: '12px'
        }}>
          <div style={{marginBottom: '15px'}}>
            <div style={{fontSize: '0.9em', color: '#7f8c8d', marginBottom: '5px'}}>대화 횟수</div>
            <div style={{fontSize: '1.5em', fontWeight: 'bold', color: '#667eea'}}>
              💬 {character.conversation_count}회
            </div>
          </div>
          <div style={{marginBottom: '15px'}}>
            <div style={{fontSize: '0.9em', color: '#7f8c8d', marginBottom: '5px'}}>호감도</div>
            <div style={{fontSize: '1.5em', fontWeight: 'bold', color: '#e74c3c'}}>
              ❤️ {character.affection_level}/100
            </div>
          </div>
          <div>
            <div style={{fontSize: '0.9em', color: '#7f8c8d', marginBottom: '5px'}}>관계</div>
            <div style={{fontSize: '1.2em', fontWeight: 'bold', color: '#2c3e50'}}>
              👥 {getStageKorean(character.relationship_stage)}
            </div>
          </div>
        </div>
      </div>

      {/* Center Panel - Chat Messages */}
      <div style={{flex: 1, display: 'flex', flexDirection: 'column'}}>
      {/* Affection Gained Notification */}
      {affectionGained !== null && (
        <div style={{
          position: 'fixed',
          top: '100px',
          left: '50%',
          transform: 'translateX(-50%)',
          background: 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)',
          color: 'white',
          padding: '12px 24px',
          borderRadius: '30px',
          fontSize: '1.1em',
          fontWeight: 'bold',
          zIndex: 1500,
          boxShadow: '0 4px 12px rgba(231, 76, 60, 0.4)',
          animation: 'slideDown 0.3s ease'
        }}>
          ❤️ +{affectionGained} 호감도 상승!
        </div>
      )}

      <div className="messages" style={{
        flex: 1,
        overflowY: 'auto',
        padding: '30px 20px',
        background: 'linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%)'
      }}>
        {messages.length === 0 && (
          <div style={{
            textAlign: 'center',
            padding: '60px 20px',
            color: '#95a5a6'
          }}>
            <div style={{fontSize: '4em', marginBottom: '20px'}}>💭</div>
            <p style={{fontSize: '1.2em', margin: 0}}>
              {character.name}에게 첫 메시지를 보내보세요!
            </p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} style={{
            marginBottom: '20px',
            textAlign: msg.role === 'user' ? 'right' : 'left',
            animation: 'fadeIn 0.3s ease'
          }}>
            <div style={{
              display: 'inline-block',
              padding: '14px 20px',
              borderRadius: '20px',
              background: msg.role === 'user'
                ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                : 'white',
              color: msg.role === 'user' ? 'white' : '#2c3e50',
              maxWidth: '70%',
              boxShadow: msg.role === 'user'
                ? '0 4px 12px rgba(102, 126, 234, 0.3)'
                : '0 2px 8px rgba(0,0,0,0.1)',
              fontSize: '1.05em',
              lineHeight: '1.5',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word'
            }}>
              {msg.content}
            </div>
            <div style={{
              fontSize: '0.85em',
              color: '#95a5a6',
              marginTop: '4px',
              padding: '0 10px'
            }}>
              {new Date(msg.timestamp).toLocaleTimeString('ko-KR', {
                hour: '2-digit',
                minute: '2-digit'
              })}
            </div>
          </div>
        ))}

        {isTyping && (
          <div style={{textAlign: 'left', marginBottom: '20px', animation: 'fadeIn 0.3s ease'}}>
            <div style={{
              display: 'inline-block',
              padding: '14px 20px',
              borderRadius: '20px',
              background: 'white',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
            }}>
              <span style={{color: '#7f8c8d'}}>✍️ {character.name}이(가) 입력 중...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="input-area" style={{
        padding: '20px',
        background: 'white',
        borderTop: '2px solid #e0e0e0',
        boxShadow: '0 -2px 10px rgba(0,0,0,0.05)'
      }}>
        {/* 파일 미리보기 */}
        {uploadedFile && (
          <div style={{
            marginBottom: '12px',
            padding: '12px',
            background: '#f8f9fa',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px'
          }}>
            {uploadedFilePreview ? (
              <img src={uploadedFilePreview} alt="Preview" style={{
                width: '60px',
                height: '60px',
                objectFit: 'cover',
                borderRadius: '8px'
              }} />
            ) : (
              <div style={{
                width: '60px',
                height: '60px',
                background: '#667eea',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '2em',
                color: 'white'
              }}>
                📄
              </div>
            )}
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: '600', color: '#2c3e50' }}>{uploadedFile.name}</div>
              <div style={{ fontSize: '0.9em', color: '#7f8c8d' }}>
                {(uploadedFile.size / 1024).toFixed(1)} KB
              </div>
            </div>
            <button
              onClick={removeFile}
              style={{
                padding: '8px 12px',
                background: '#e74c3c',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '0.9em'
              }}
            >
              삭제
            </button>
          </div>
        )}

        <div style={{ display: 'flex', gap: '12px' }}>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*,.pdf,.docx,.txt,.json"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={isTyping}
            style={{
              padding: '16px',
              background: uploadedFile ? '#27ae60' : '#95a5a6',
              color: 'white',
              border: 'none',
              borderRadius: '16px',
              cursor: isTyping ? 'not-allowed' : 'pointer',
              fontSize: '1.5em',
              transition: 'all 0.3s'
            }}
            title="파일 첨부"
          >
            {uploadedFile ? '✅' : '📎'}
          </button>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                sendMessage()
              }
            }}
            placeholder={`${character.name}에게 메시지 보내기... (Enter: 전송, Shift+Enter: 줄바꿈)`}
            rows={3}
            style={{
              flex: 1,
              padding: '16px',
              borderRadius: '16px',
              border: '2px solid #e0e0e0',
              fontSize: '1.05em',
              resize: 'none',
              fontFamily: 'inherit',
              transition: 'border-color 0.3s'
            }}
            onFocus={(e) => e.currentTarget.style.borderColor = '#667eea'}
            onBlur={(e) => e.currentTarget.style.borderColor = '#e0e0e0'}
          />
          <button
            onClick={sendMessage}
            disabled={(!input.trim() && !uploadedFile) || isTyping}
            style={{
              padding: '16px 36px',
              background: ((!input.trim() && !uploadedFile) || isTyping)
                ? '#dcdde1'
                : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '16px',
              cursor: ((!input.trim() && !uploadedFile) || isTyping) ? 'not-allowed' : 'pointer',
              fontSize: '1.1em',
              fontWeight: '600',
              transition: 'all 0.3s',
              boxShadow: ((!input.trim() && !uploadedFile) || isTyping)
                ? 'none'
                : '0 4px 12px rgba(102, 126, 234, 0.3)'
            }}
            onMouseEnter={(e) => {
              if (!((!input.trim() && !uploadedFile) || isTyping)) {
                e.currentTarget.style.transform = 'translateY(-2px)'
                e.currentTarget.style.boxShadow = '0 6px 16px rgba(102, 126, 234, 0.4)'
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)'
              e.currentTarget.style.boxShadow = ((!input.trim() && !uploadedFile) || isTyping)
                ? 'none'
                : '0 4px 12px rgba(102, 126, 234, 0.3)'
            }}
          >
            {isTyping ? '전송 중...' : '전송 ✈️'}
          </button>
        </div>
      </div>
      </div>
    </div>

    <style>{`
      @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
      }
      @keyframes slideDown {
        from { opacity: 0; transform: translate(-50%, -20px); }
        to { opacity: 1; transform: translate(-50%, 0); }
      }
    `}</style>
    </>
  )
}
