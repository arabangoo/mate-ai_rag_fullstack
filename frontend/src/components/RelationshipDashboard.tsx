import { useState, useEffect } from 'react'
import axios from 'axios'

interface RelationshipData {
  affection_level: number
  relationship_stage: string
  total_conversations: number
  days_known: number
  consecutive_days: number
  milestones_count: number
  recent_milestones: any[]
  emotional_moments_count: number
  last_interaction: string
  conversation_quality_score: number
}

interface Props {
  characterId: string
  characterName: string
  onClose: () => void
}

export default function RelationshipDashboard({ characterId, characterName, onClose }: Props) {
  const [relationshipData, setRelationshipData] = useState<RelationshipData | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadRelationshipData()
  }, [characterId])

  const loadRelationshipData = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/character/${characterId}/relationship`)
      if (response.data.success) {
        setRelationshipData(response.data)
      }
    } catch (error) {
      console.error('관계 정보 로딩 실패:', error)
    } finally {
      setIsLoading(false)
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

  const getStageColor = (stage: string) => {
    const colors: { [key: string]: string } = {
      stranger: '#95a5a6',
      acquaintance: '#3498db',
      friend: '#2ecc71',
      close_friend: '#9b59b6',
      romantic: '#e74c3c'
    }
    return colors[stage] || '#95a5a6'
  }

  if (isLoading) {
    return (
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0,0,0,0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 2000
      }}>
        <div style={{
          background: 'white',
          padding: '40px',
          borderRadius: '20px',
          fontSize: '1.2em'
        }}>
          로딩 중...
        </div>
      </div>
    )
  }

  if (!relationshipData) {
    return null
  }

  return (
    <div
      style={{
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
        padding: '20px'
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          maxWidth: '900px',
          width: '100%',
          borderRadius: '20px',
          padding: '30px',
          color: 'white',
          position: 'relative',
          boxShadow: '0 20px 60px rgba(0,0,0,0.3)'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'rgba(255,255,255,0.2)',
            border: 'none',
            color: 'white',
            width: '40px',
            height: '40px',
            borderRadius: '50%',
            fontSize: '2em',
            cursor: 'pointer',
            transition: 'background 0.3s',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            lineHeight: '1'
          }}
          onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.3)'}
          onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.2)'}
        >
          ×
        </button>

        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <h1 style={{ fontSize: '1.8em', margin: '0 0 8px 0' }}>💕 관계 대시보드</h1>
          <p style={{ fontSize: '1em', opacity: 0.9, margin: 0 }}>{characterName}와의 관계</p>
        </div>

        {/* Main Stats */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '12px',
          marginBottom: '24px'
        }}>
          {/* Affection Level */}
          <div style={{
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '12px',
            padding: '16px',
            textAlign: 'center',
            backdropFilter: 'blur(10px)'
          }}>
            <div style={{ fontSize: '2em', marginBottom: '8px' }}>❤️</div>
            <div style={{ fontSize: '1.5em', fontWeight: 'bold' }}>{relationshipData.affection_level}</div>
            <div style={{ opacity: 0.8, marginTop: '4px', fontSize: '0.9em' }}>호감도</div>
            <div style={{
              background: 'rgba(255,255,255,0.2)',
              height: '8px',
              borderRadius: '4px',
              marginTop: '12px',
              overflow: 'hidden'
            }}>
              <div style={{
                background: '#e74c3c',
                height: '100%',
                width: `${relationshipData.affection_level}%`,
                transition: 'width 0.5s ease'
              }} />
            </div>
          </div>

          {/* Relationship Stage */}
          <div style={{
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '12px',
            padding: '16px',
            textAlign: 'center',
            backdropFilter: 'blur(10px)'
          }}>
            <div style={{ fontSize: '2em', marginBottom: '8px' }}>👥</div>
            <div style={{
              fontSize: '1.1em',
              fontWeight: 'bold',
              color: getStageColor(relationshipData.relationship_stage)
            }}>
              {getStageKorean(relationshipData.relationship_stage)}
            </div>
            <div style={{ opacity: 0.8, marginTop: '4px', fontSize: '0.85em' }}>관계 단계</div>
          </div>

          {/* Conversations */}
          <div style={{
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '12px',
            padding: '16px',
            textAlign: 'center',
            backdropFilter: 'blur(10px)'
          }}>
            <div style={{ fontSize: '2em', marginBottom: '8px' }}>💬</div>
            <div style={{ fontSize: '1.5em', fontWeight: 'bold' }}>{relationshipData.total_conversations}</div>
            <div style={{ opacity: 0.8, marginTop: '4px', fontSize: '0.9em' }}>대화 횟수</div>
          </div>

          {/* Days Known */}
          <div style={{
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '12px',
            padding: '16px',
            textAlign: 'center',
            backdropFilter: 'blur(10px)'
          }}>
            <div style={{ fontSize: '2em', marginBottom: '8px' }}>📅</div>
            <div style={{ fontSize: '1.5em', fontWeight: 'bold' }}>{relationshipData.days_known}</div>
            <div style={{ opacity: 0.8, marginTop: '4px', fontSize: '0.9em' }}>알고 지낸 날</div>
          </div>

          {/* Consecutive Days */}
          <div style={{
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '12px',
            padding: '16px',
            textAlign: 'center',
            backdropFilter: 'blur(10px)'
          }}>
            <div style={{ fontSize: '2em', marginBottom: '8px' }}>🔥</div>
            <div style={{ fontSize: '1.5em', fontWeight: 'bold' }}>{relationshipData.consecutive_days}</div>
            <div style={{ opacity: 0.8, marginTop: '4px', fontSize: '0.9em' }}>연속 대화 일수</div>
          </div>

          {/* Milestones */}
          <div style={{
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '12px',
            padding: '16px',
            textAlign: 'center',
            backdropFilter: 'blur(10px)'
          }}>
            <div style={{ fontSize: '2em', marginBottom: '8px' }}>🎉</div>
            <div style={{ fontSize: '1.5em', fontWeight: 'bold' }}>{relationshipData.milestones_count}</div>
            <div style={{ opacity: 0.8, marginTop: '4px', fontSize: '0.9em' }}>달성한 마일스톤</div>
          </div>
        </div>

        {/* Recent Milestones */}
        {relationshipData.recent_milestones && relationshipData.recent_milestones.length > 0 && (
          <div style={{
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '12px',
            padding: '16px',
            marginBottom: '16px',
            backdropFilter: 'blur(10px)'
          }}>
            <h3 style={{ margin: '0 0 12px 0', fontSize: '1.2em' }}>🏆 최근 마일스톤</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {relationshipData.recent_milestones.map((milestone, idx) => (
                <div key={idx} style={{
                  background: 'rgba(255,255,255,0.1)',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}>
                  <span style={{ fontSize: '0.95em' }}>
                    {milestone.type.replace(/_/g, ' ')}
                  </span>
                  <span style={{ opacity: 0.7, fontSize: '0.85em' }}>
                    {new Date(milestone.timestamp).toLocaleDateString('ko-KR')}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Quality Score */}
        <div style={{
          background: 'rgba(255,255,255,0.1)',
          borderRadius: '12px',
          padding: '16px',
          textAlign: 'center',
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', fontSize: '1.1em' }}>⭐ 대화 품질 점수</h3>
          <div style={{ fontSize: '1.5em', fontWeight: 'bold' }}>
            {relationshipData.conversation_quality_score.toFixed(1)} / 10
          </div>
          <div style={{
            background: 'rgba(255,255,255,0.2)',
            height: '8px',
            borderRadius: '4px',
            marginTop: '10px',
            overflow: 'hidden'
          }}>
            <div style={{
              background: 'linear-gradient(90deg, #f39c12, #e74c3c)',
              height: '100%',
              width: `${(relationshipData.conversation_quality_score / 10) * 100}%`,
              transition: 'width 0.5s ease'
            }} />
          </div>
        </div>

        {/* Footer */}
        <div style={{
          textAlign: 'center',
          marginTop: '16px',
          opacity: 0.7,
          fontSize: '0.85em'
        }}>
          마지막 대화: {relationshipData.last_interaction ?
            new Date(relationshipData.last_interaction).toLocaleString('ko-KR') :
            '없음'}
        </div>
      </div>
    </div>
  )
}
