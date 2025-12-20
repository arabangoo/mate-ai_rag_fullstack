import { useState } from 'react'
import axios from 'axios'
import ReadyPlayerMeCustomizer from './ReadyPlayerMeCustomizer'

interface CharacterData {
  name: string
  gender: string
  age: number
  personality: string[]
  backstory: string
  image: File | null
  imageDataUrl: string
  avatarUrl: string
  speechStyle: string
  interests: string[]
  voiceTone: string
  customizationType: 'rpm' | 'upload' | ''
  customizationData: any
}

interface Props {
  onComplete: (characterId: string) => void
}

export default function CharacterCreation({ onComplete }: Props) {
  const [step, setStep] = useState(1)
  const [character, setCharacter] = useState<CharacterData>({
    name: '',
    gender: 'female',
    age: 23,
    personality: [],
    backstory: '',
    image: null,
    imageDataUrl: '',
    avatarUrl: '',
    speechStyle: '친근하고 다정함',
    interests: [],
    voiceTone: 'soft',
    customizationType: '',
    customizationData: null
  })

  const [isCreating, setIsCreating] = useState(false)
  const [wordCount, setWordCount] = useState(0)

  const updateBackstory = (text: string) => {
    setCharacter({...character, backstory: text})
    setWordCount(text.length)
  }

  const handleRPMSave = async (avatarUrl: string) => {
    console.log('Ready Player Me 캐릭터 URL:', avatarUrl)

    // 썸네일 URL 생성 (Ready Player Me는 .png로 변경하면 썸네일)
    const thumbnailUrl = avatarUrl.replace('.glb', '.png')

    setCharacter({
      ...character,
      avatarUrl,
      imageDataUrl: thumbnailUrl,
      customizationType: 'rpm',
      customizationData: { avatarUrl, thumbnailUrl }
    })
    setStep(3)
  }

  const handleImageUpload = (file: File) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      setCharacter({
        ...character,
        image: file,
        imageDataUrl: e.target?.result as string,
        customizationType: 'upload'
      })
      setStep(3)
    }
    reader.readAsDataURL(file)
  }

  const handleSubmit = async () => {
    if (!character.name) {
      alert('캐릭터 이름을 입력해주세요.')
      return
    }

    if (!character.backstory || character.backstory.length < 100) {
      alert('배경설정을 최소 100자 이상 작성해주세요.')
      return
    }

    setIsCreating(true)

    try {
      const formData = new FormData()
      formData.append('name', character.name)
      formData.append('gender', character.gender)
      formData.append('age', character.age.toString())
      formData.append('personality', JSON.stringify(character.personality))
      formData.append('backstory', character.backstory)
      formData.append('speechStyle', character.speechStyle)
      formData.append('interests', JSON.stringify(character.interests))
      formData.append('voiceTone', character.voiceTone)

      // 이미지 데이터 전송
      if (character.imageDataUrl) {
        // DataURL을 Blob으로 변환
        const blob = await (await fetch(character.imageDataUrl)).blob()
        formData.append('image', blob, 'character.png')
      }

      // 커스터마이징 데이터 전송
      if (character.customizationData) {
        formData.append('customization_type', character.customizationType)
        formData.append('customization_data', JSON.stringify(character.customizationData))
      }

      const response = await axios.post('http://localhost:8000/api/character/create', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      const { character_id } = response.data
      localStorage.setItem('current_character_id', character_id)
      onComplete(character_id)

    } catch (error) {
      console.error('캐릭터 생성 실패:', error)
      alert('캐릭터 생성에 실패했습니다.')
    } finally {
      setIsCreating(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '40px 20px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      <div style={{
        maxWidth: character.customizationType === 'rpm' && step === 2 ? '1000px' : '800px',
        width: '100%',
        background: 'white',
        borderRadius: '24px',
        boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
        overflow: 'hidden'
      }}>
        <div style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          padding: '40px',
          textAlign: 'center',
          color: 'white'
        }}>
          <h1 style={{
            margin: '0 0 20px 0',
            fontSize: '2.5em',
            fontWeight: '700'
          }}>
            💕 당신만의 AI 연인 만들기
          </h1>
          <p style={{
            margin: 0,
            fontSize: '1.2em',
            opacity: 0.9
          }}>
            영화 Her처럼 특별한 AI와의 로맨스를 시작하세요
          </p>
        </div>

        <div style={{
          display: 'flex',
          padding: '30px 40px',
          borderBottom: '2px solid #f0f0f0',
          background: '#fafafa'
        }}>
          {[
            {num: 1, label: '기본정보', icon: '👤'},
            {num: 2, label: '외형', icon: '✨'},
            {num: 3, label: '성격', icon: '💭'},
            {num: 4, label: '배경', icon: '📖'}
          ].map((s) => (
            <div
              key={s.num}
              style={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                position: 'relative'
              }}
            >
              <div style={{
                width: '50px',
                height: '50px',
                borderRadius: '50%',
                background: step >= s.num
                  ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                  : '#e0e0e0',
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1.5em',
                fontWeight: 'bold',
                marginBottom: '10px',
                transition: 'all 0.3s',
                boxShadow: step >= s.num ? '0 4px 12px rgba(102, 126, 234, 0.3)' : 'none'
              }}>
                {step > s.num ? '✓' : s.icon}
              </div>
              <div style={{
                fontSize: '0.9em',
                fontWeight: step >= s.num ? '600' : '400',
                color: step >= s.num ? '#667eea' : '#999'
              }}>
                {s.label}
              </div>
            </div>
          ))}
        </div>

      <div style={{padding: '40px'}}>
        {step === 1 && (
          <section>
            <h2 style={{marginBottom: '30px', color: '#2c3e50', fontSize: '1.8em'}}>기본 정보</h2>
            <div style={{marginBottom: '24px'}}>
              <label style={{display: 'block', marginBottom: '10px', fontWeight: '600', color: '#34495e'}}>
                캐릭터 이름
              </label>
              <input
                type="text"
                placeholder="예: 사만다, 루나..."
                value={character.name}
                onChange={(e) => setCharacter({...character, name: e.target.value})}
                style={{
                  width: '100%',
                  padding: '14px',
                  borderRadius: '12px',
                  border: '2px solid #e0e0e0',
                  fontSize: '1.05em',
                  transition: 'border-color 0.3s'
                }}
                onFocus={(e) => e.currentTarget.style.borderColor = '#667eea'}
                onBlur={(e) => e.currentTarget.style.borderColor = '#e0e0e0'}
              />
            </div>

            <div style={{marginBottom: '24px'}}>
              <label style={{display: 'block', marginBottom: '10px', fontWeight: '600', color: '#34495e'}}>
                성별
              </label>
              <select
                value={character.gender}
                onChange={(e) => setCharacter({...character, gender: e.target.value})}
                style={{
                  width: '100%',
                  padding: '14px',
                  borderRadius: '12px',
                  border: '2px solid #e0e0e0',
                  fontSize: '1.05em',
                  background: 'white'
                }}
              >
                <option value="female">여성</option>
                <option value="male">남성</option>
              </select>
            </div>

            <div style={{marginBottom: '30px'}}>
              <label style={{display: 'block', marginBottom: '10px', fontWeight: '600', color: '#34495e'}}>
                나이
              </label>
              <input
                type="number"
                min="18"
                max="99"
                value={character.age}
                onChange={(e) => setCharacter({...character, age: parseInt(e.target.value)})}
                style={{
                  width: '100%',
                  padding: '14px',
                  borderRadius: '12px',
                  border: '2px solid #e0e0e0',
                  fontSize: '1.05em'
                }}
              />
            </div>

            <button
              onClick={() => setStep(2)}
              style={{
                width: '100%',
                padding: '16px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '12px',
                fontSize: '1.1em',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.3s',
                boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
              }}
              onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
              onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
            >
              다음 단계로 →
            </button>
          </section>
        )}

        {step === 2 && !character.customizationType && (
          <section>
            <h2 style={{marginBottom: '30px', color: '#2c3e50', fontSize: '1.8em', textAlign: 'center'}}>
              캐릭터 외형 선택
            </h2>
            <p style={{textAlign: 'center', color: '#7f8c8d', marginBottom: '40px'}}>
              원하는 방식으로 캐릭터를 만들어보세요
            </p>

            <div style={{display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '30px', maxWidth: '600px', margin: '0 auto'}}>
              {/* Ready Player Me */}
              <div
                onClick={() => setCharacter({...character, customizationType: 'rpm'})}
                style={{
                  padding: '40px 30px',
                  border: '3px solid #e0e0e0',
                  borderRadius: '16px',
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.3s',
                  background: 'white'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = '#667eea'
                  e.currentTarget.style.transform = 'translateY(-5px)'
                  e.currentTarget.style.boxShadow = '0 8px 20px rgba(102, 126, 234, 0.3)'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = '#e0e0e0'
                  e.currentTarget.style.transform = 'translateY(0)'
                  e.currentTarget.style.boxShadow = 'none'
                }}
              >
                <div style={{fontSize: '5em', marginBottom: '20px'}}>🎮</div>
                <h3 style={{margin: '0 0 15px 0', color: '#2c3e50', fontSize: '1.3em'}}>3D 캐릭터 생성</h3>
                <p style={{margin: '0 0 10px 0', color: '#667eea', fontWeight: '600'}}>MATE.AI</p>
                <p style={{margin: 0, color: '#7f8c8d', fontSize: '0.95em', lineHeight: '1.5'}}>
                  고품질 3D 캐릭터를<br/>
                  디테일하게 커스터마이징<br/>
                  <span style={{color: '#27ae60', fontWeight: '600'}}>✨ 추천!</span>
                </p>
              </div>

              {/* 이미지 업로드 */}
              <div
                style={{
                  padding: '40px 30px',
                  border: '3px solid #e0e0e0',
                  borderRadius: '16px',
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.3s',
                  background: 'white',
                  position: 'relative'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = '#667eea'
                  e.currentTarget.style.transform = 'translateY(-5px)'
                  e.currentTarget.style.boxShadow = '0 8px 20px rgba(102, 126, 234, 0.3)'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = '#e0e0e0'
                  e.currentTarget.style.transform = 'translateY(0)'
                  e.currentTarget.style.boxShadow = 'none'
                }}
              >
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => {
                    const file = e.target.files?.[0]
                    if (file) handleImageUpload(file)
                  }}
                  style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    opacity: 0,
                    cursor: 'pointer'
                  }}
                />
                <div style={{fontSize: '5em', marginBottom: '20px'}}>📷</div>
                <h3 style={{margin: '0 0 15px 0', color: '#2c3e50', fontSize: '1.3em'}}>이미지 업로드</h3>
                <p style={{margin: '0 0 10px 0', color: '#95a5a6', fontWeight: '600'}}>간편한 방법</p>
                <p style={{margin: 0, color: '#7f8c8d', fontSize: '0.95em', lineHeight: '1.5'}}>
                  원하는 이미지를<br/>
                  직접 업로드
                </p>
              </div>
            </div>

            <button
              onClick={() => setStep(1)}
              style={{
                marginTop: '40px',
                padding: '12px 30px',
                background: '#95a5a6',
                color: 'white',
                border: 'none',
                borderRadius: '10px',
                fontSize: '1em',
                fontWeight: '600',
                cursor: 'pointer',
                display: 'block',
                margin: '40px auto 0'
              }}
            >
              ← 이전
            </button>
          </section>
        )}

        {step === 2 && character.customizationType === 'rpm' && (
          <section>
            <h2 style={{marginBottom: '20px', color: '#2c3e50', fontSize: '1.8em'}}>
              MATE.AI 캐릭터 생성
            </h2>
            <ReadyPlayerMeCustomizer onSave={handleRPMSave} />
            <button
              onClick={() => setCharacter({...character, customizationType: ''})}
              style={{
                marginTop: '20px',
                padding: '12px 30px',
                background: '#95a5a6',
                color: 'white',
                border: 'none',
                borderRadius: '10px',
                fontSize: '1em',
                fontWeight: '600',
                cursor: 'pointer'
              }}
            >
              ← 다른 방법 선택
            </button>
          </section>
        )}

        {step === 3 && (
          <section className="step-section">
            <h2>성격 & 말투</h2>
            <div className="form-group">
              <label>성격 특성</label>
              {['친절함', '장난기', '지적', '감성적', '활발함', '차분함'].map(trait => (
                <button
                  key={trait}
                  onClick={() => {
                    const newPersonality = character.personality.includes(trait)
                      ? character.personality.filter(t => t !== trait)
                      : [...character.personality, trait]
                    setCharacter({...character, personality: newPersonality})
                  }}
                  style={{
                    background: character.personality.includes(trait) ? '#667eea' : '#e0e0e0',
                    color: character.personality.includes(trait) ? 'white' : 'black',
                    margin: '5px', padding: '10px', border: 'none', borderRadius: '8px'
                  }}
                >
                  {trait}
                </button>
              ))}
            </div>
            <div className="form-group">
              <label>말투 스타일</label>
              <select value={character.speechStyle} onChange={(e) => setCharacter({...character, speechStyle: e.target.value})}>
                <option value="친근하고 다정함">친근하고 다정함</option>
                <option value="공손하고 정중함">공손하고 정중함</option>
                <option value="쿨하고 직설적">쿨하고 직설적</option>
              </select>
            </div>
            <button onClick={() => setStep(2)}>← 이전</button>
            <button onClick={() => setStep(4)}>다음 →</button>
          </section>
        )}

        {step === 4 && (
          <section className="step-section">
            <h2>배경설정 (매우 중요!)</h2>
            <p>캐릭터의 과거, 성장 배경, 가치관, 꿈 등을 자유롭게 작성하세요.</p>
            <div className="form-group">
              <label>
                배경 스토리 (최소 100자)
                <span style={{color: wordCount < 100 ? 'red' : 'green', marginLeft: '10px'}}>
                  {wordCount}자
                </span>
              </label>
              <textarea
                placeholder="예: 시골 마을에서 자랐다. 부모님은 작은 카페를 운영하셨고..."
                value={character.backstory}
                onChange={(e) => updateBackstory(e.target.value)}
                rows={20}
                style={{width: '100%', padding: '15px', fontSize: '1.05em'}}
              />
            </div>
            <button onClick={() => setStep(3)}>← 이전</button>
            <button
              onClick={handleSubmit}
              disabled={isCreating || wordCount < 100}
              style={{
                background: isCreating || wordCount < 100 ? '#ccc' : '#f5576c',
                color: 'white',
                padding: '15px 30px',
                border: 'none',
                borderRadius: '8px',
                fontSize: '1.2em',
                cursor: isCreating || wordCount < 100 ? 'not-allowed' : 'pointer'
              }}
            >
              {isCreating ? '생성 중...' : `${character.name} 만들기 ✨`}
            </button>
          </section>
        )}
      </div>
      </div>
    </div>
  )
}
