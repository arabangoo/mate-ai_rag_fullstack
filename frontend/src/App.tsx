import { useState, useEffect } from 'react'
import axios from 'axios'
import CharacterCreation from './components/CharacterCreation'
import ChatInterface from './components/ChatInterface'
import RelationshipDashboard from './components/RelationshipDashboard'
import './App.css'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [currentCharacterId, setCurrentCharacterId] = useState<string | null>(null)
  const [character, setCharacter] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [showDashboard, setShowDashboard] = useState(false)
  
  useEffect(() => {
    const savedCharacterId = localStorage.getItem('current_character_id')
    if (savedCharacterId) {
      loadCharacter(savedCharacterId)
    } else {
      setIsLoading(false)
    }
  }, [])
  
  const loadCharacter = async (characterId: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/character/${characterId}`)
      
      if (response.data.success) {
        setCharacter(response.data.character)
        setCurrentCharacterId(characterId)
      } else {
        localStorage.removeItem('current_character_id')
      }
    } catch (error) {
      console.error('캐릭터 로딩 실패:', error)
      localStorage.removeItem('current_character_id')
    } finally {
      setIsLoading(false)
    }
  }
  
  const handleCharacterCreated = (characterId: string) => {
    loadCharacter(characterId)
  }
  
  const handleResetCharacter = async () => {
    if (!confirm('정말 캐릭터를 초기화하시겠습니까? 모든 대화 내역이 삭제됩니다.')) {
      return
    }
    
    try {
      await axios.delete(`${API_BASE_URL}/api/character/${currentCharacterId}/reset`)
      localStorage.removeItem('current_character_id')
      setCurrentCharacterId(null)
      setCharacter(null)
      alert('캐릭터가 초기화되었습니다.')
    } catch (error) {
      console.error('초기화 실패:', error)
      alert('초기화에 실패했습니다.')
    }
  }
  
  if (isLoading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        fontSize: '1.5em'
      }}>
        로딩 중...
      </div>
    )
  }
  
  if (!currentCharacterId || !character) {
    return <CharacterCreation onComplete={handleCharacterCreated} />
  }
  
  return (
    <div className="app">
      <header style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        borderBottom: '2px solid rgba(255,255,255,0.1)',
        padding: '15px 20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        zIndex: 1000,
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
      }}>
        <h1 style={{margin: 0, fontSize: '1.8em', color: 'white', fontWeight: '700'}}>
          💕 MATE.AI
        </h1>
        <div style={{display: 'flex', gap: '10px'}}>
          <button
            onClick={() => setShowDashboard(true)}
            style={{
              padding: '10px 20px',
              background: 'rgba(255,255,255,0.2)',
              color: 'white',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: '500',
              transition: 'all 0.3s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.3)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.2)'
            }}
          >
            📊 관계 대시보드
          </button>
          <button
            onClick={handleResetCharacter}
            style={{
              padding: '10px 20px',
              background: '#e74c3c',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: '500',
              transition: 'all 0.3s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#c0392b'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = '#e74c3c'
            }}
          >
            🗑️ 초기화
          </button>
        </div>
      </header>

      <div style={{marginTop: '70px'}}>
        <ChatInterface
          characterId={currentCharacterId}
          character={character}
          onCharacterUpdate={loadCharacter}
        />
      </div>

      {showDashboard && currentCharacterId && character && (
        <RelationshipDashboard
          characterId={currentCharacterId}
          characterName={character.name}
          onClose={() => setShowDashboard(false)}
        />
      )}
    </div>
  )
}

export default App
