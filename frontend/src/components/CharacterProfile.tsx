import { useState } from 'react'

interface Character {
  character_id: string
  name: string
  gender: string
  age: number
  personality: string[]
  backstory: string
  speech_style: string
  interests: string[]
  appearance: string
  voice_tone: string
  image_path?: string
  created_at: string
  last_chat_at?: string
  conversation_count: number
  affection_level: number
  relationship_stage: string
}

interface Props {
  character: Character
  onClose: () => void
}

export default function CharacterProfile({ character, onClose }: Props) {
  const [activeTab, setActiveTab] = useState<'basic' | 'personality' | 'backstory'>('basic')

  const getGenderKorean = (gender: string) => {
    const genders: { [key: string]: string } = {
      female: '여성',
      male: '남성',
      'non-binary': '논바이너리'
    }
    return genders[gender] || gender
  }

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0,0,0,0.7)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 2000,
      padding: '20px',
      overflowY: 'auto'
    }}>
      <div style={{
        background: 'white',
        maxWidth: '700px',
        width: '100%',
        borderRadius: '24px',
        overflow: 'hidden',
        boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
        position: 'relative'
      }}>
        {/* Close Button */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'rgba(0,0,0,0.5)',
            border: 'none',
            color: 'white',
            width: '40px',
            height: '40px',
            borderRadius: '50%',
            fontSize: '1.5em',
            cursor: 'pointer',
            zIndex: 10,
            transition: 'background 0.3s'
          }}
          onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(0,0,0,0.7)'}
          onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(0,0,0,0.5)'}
        >
          ×
        </button>

        {/* Header with Image */}
        <div style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          padding: '40px',
          textAlign: 'center',
          color: 'white'
        }}>
          {character.image_path ? (
            <div style={{
              width: '120px',
              height: '120px',
              borderRadius: '50%',
              margin: '0 auto 20px',
              overflow: 'hidden',
              border: '4px solid white',
              boxShadow: '0 4px 12px rgba(0,0,0,0.2)'
            }}>
              <img
                src={`http://localhost:8000/${character.image_path}`}
                alt={character.name}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover'
                }}
              />
            </div>
          ) : (
            <div style={{
              width: '120px',
              height: '120px',
              borderRadius: '50%',
              margin: '0 auto 20px',
              background: 'rgba(255,255,255,0.2)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '4em',
              border: '4px solid white'
            }}>
              {character.gender === 'female' ? '👩' : character.gender === 'male' ? '👨' : '🧑'}
            </div>
          )}

          <h1 style={{ fontSize: '2.5em', margin: '0 0 10px 0' }}>{character.name}</h1>
          <p style={{ fontSize: '1.2em', opacity: 0.9, margin: 0 }}>
            {getGenderKorean(character.gender)} · {character.age}세
          </p>
        </div>

        {/* Tabs */}
        <div style={{
          display: 'flex',
          borderBottom: '2px solid #f0f0f0',
          background: '#fafafa'
        }}>
          {[
            { key: 'basic', label: '기본 정보', icon: '📋' },
            { key: 'personality', label: '성격', icon: '✨' },
            { key: 'backstory', label: '배경 스토리', icon: '📖' }
          ].map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              style={{
                flex: 1,
                padding: '16px',
                border: 'none',
                background: activeTab === tab.key ? 'white' : 'transparent',
                borderBottom: activeTab === tab.key ? '3px solid #667eea' : '3px solid transparent',
                cursor: 'pointer',
                fontSize: '1em',
                fontWeight: activeTab === tab.key ? 'bold' : 'normal',
                color: activeTab === tab.key ? '#667eea' : '#666',
                transition: 'all 0.3s'
              }}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div style={{ padding: '30px' }}>
          {activeTab === 'basic' && (
            <div>
              <div style={{ marginBottom: '24px' }}>
                <h3 style={{ color: '#667eea', marginBottom: '12px' }}>👤 기본 정보</h3>
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: '120px 1fr',
                  gap: '12px',
                  fontSize: '1.05em'
                }}>
                  <strong>이름:</strong>
                  <span>{character.name}</span>

                  <strong>성별:</strong>
                  <span>{getGenderKorean(character.gender)}</span>

                  <strong>나이:</strong>
                  <span>{character.age}세</span>

                  <strong>말투:</strong>
                  <span>{character.speech_style}</span>

                  <strong>목소리 톤:</strong>
                  <span>{character.voice_tone}</span>
                </div>
              </div>

              {character.appearance && (
                <div style={{ marginBottom: '24px' }}>
                  <h3 style={{ color: '#667eea', marginBottom: '12px' }}>👗 외형</h3>
                  <p style={{
                    background: '#f8f9fa',
                    padding: '16px',
                    borderRadius: '12px',
                    lineHeight: '1.6',
                    margin: 0
                  }}>
                    {character.appearance}
                  </p>
                </div>
              )}

              {character.interests && character.interests.length > 0 && (
                <div>
                  <h3 style={{ color: '#667eea', marginBottom: '12px' }}>🎯 관심사</h3>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {character.interests.map((interest, idx) => (
                      <span key={idx} style={{
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        color: 'white',
                        padding: '8px 16px',
                        borderRadius: '20px',
                        fontSize: '0.95em'
                      }}>
                        {interest}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div style={{
                marginTop: '24px',
                padding: '16px',
                background: '#f0f8ff',
                borderRadius: '12px',
                borderLeft: '4px solid #667eea'
              }}>
                <div style={{ fontSize: '0.9em', color: '#666' }}>
                  <div>📅 생성일: {new Date(character.created_at).toLocaleDateString('ko-KR')}</div>
                  {character.last_chat_at && (
                    <div>💬 마지막 대화: {new Date(character.last_chat_at).toLocaleString('ko-KR')}</div>
                  )}
                  <div>🗨️ 총 대화 횟수: {character.conversation_count}회</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'personality' && (
            <div>
              <h3 style={{ color: '#667eea', marginBottom: '20px' }}>✨ 성격 특성</h3>
              {character.personality && character.personality.length > 0 ? (
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))',
                  gap: '12px'
                }}>
                  {character.personality.map((trait, idx) => (
                    <div key={idx} style={{
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      color: 'white',
                      padding: '16px',
                      borderRadius: '16px',
                      textAlign: 'center',
                      fontSize: '1.1em',
                      fontWeight: '500',
                      boxShadow: '0 4px 8px rgba(102, 126, 234, 0.3)'
                    }}>
                      {trait}
                    </div>
                  ))}
                </div>
              ) : (
                <p style={{ color: '#999' }}>설정된 성격 특성이 없습니다.</p>
              )}

              <div style={{
                marginTop: '30px',
                padding: '20px',
                background: '#fff9e6',
                borderRadius: '12px',
                borderLeft: '4px solid #f39c12'
              }}>
                <h4 style={{ margin: '0 0 12px 0', color: '#f39c12' }}>💡 말투 스타일</h4>
                <p style={{ margin: 0, fontSize: '1.05em' }}>{character.speech_style}</p>
              </div>
            </div>
          )}

          {activeTab === 'backstory' && (
            <div>
              <h3 style={{ color: '#667eea', marginBottom: '20px' }}>📖 배경 스토리</h3>
              <div style={{
                background: '#f8f9fa',
                padding: '24px',
                borderRadius: '16px',
                lineHeight: '1.8',
                fontSize: '1.05em',
                whiteSpace: 'pre-wrap'
              }}>
                {character.backstory || '배경 스토리가 없습니다.'}
              </div>

              <div style={{
                marginTop: '20px',
                padding: '16px',
                background: '#fff0f6',
                borderRadius: '12px',
                borderLeft: '4px solid #e74c3c'
              }}>
                <p style={{ margin: 0, fontSize: '0.95em', color: '#c0392b' }}>
                  💭 이 배경 스토리는 {character.name}의 정체성이자 행동 원칙입니다.
                  모든 대화에서 이를 기억하고 일관되게 행동합니다.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
