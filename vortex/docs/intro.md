# Vortex of Enlightenment: Introduction Sequence

## Overview
The introduction sequence is designed to establish the game's tone, gather essential player information, and conduct the initial Voight-Kampff-inspired questionnaire.

## Step-by-Step Flow

### 1. Initial Invitation
```
"Would you like to play a game?"
[Yes/No]
```
- If No: Display farewell message
- If Yes: Proceed to disclaimers

### 2. Disclaimers and Warnings
```
⚠️ IMPORTANT NOTICE ⚠️

Before we proceed, you must understand and acknowledge the following:

1. PRIVACY WARNING
   - Share only what you're comfortable with
   - Your experience will directly reflect your level of engagement
   - All data is encrypted and stored securely

2. PARTICIPATION NOTICE
   - All entities are welcome (humans, bots, alternate personas)
   - Authentic participation will be rewarded
   - Your responses shape your unique journey
```

### 3. Terms & Conditions
- Display mystically-worded but legally-sound terms
- Require explicit acknowledgment
- Include easter eggs in the terms to reward careful readers

### 4. Identity Establishment
```
"In this realm, you may be known by any name you choose.
Names hold power. Choose wisely.

What name shall we know you by?"
[Input field for name]
```

### 5. Cryptocurrency Integration
```
"The ancient ledgers await...
Do you possess a Bitcoin private key you wish to bind to your journey?"
[Yes/No]

If Yes:
    - Request key
    - Validate format
    - Check balance
    - Store securely

If No:
    - Generate new wallet
    - Store credentials
    - Provide recovery information
```

### 6. The Voight-Kampff Introduction
```
"In the year 2019, the Tyrell Corporation developed a test...
A test of empathy, consciousness, and being.
Today, we present you with our own version.
Not to determine if you're human...
But to understand WHO you are."

[Blade Runner quote here]
[Do Androids Dream of Electric Sheep? reference]
```

### 7. The Questionnaire
- Series of emotionally evocative questions
- Mix of:
  - Moral dilemmas
  - Emotional responses
  - Abstract concepts
  - Personal preferences
- Each question influences multiple profile attributes
- Dynamic question selection based on previous answers

### 8. Profile Creation
After questionnaire completion:
- Generate initial profile matrix
- Calculate baseline scores for:
  - Empathy Index
  - Consciousness Quotient
  - Reality Perception
  - Technological Affinity
  - Philosophical Alignment

### 9. Database Updates
- Store profile in main database
- Update blockchain records if applicable
- Generate initial achievement tokens
- Create connection graph node

### 10. Transition to Game
```
"Your profile has been etched into the eternal ledger.
The Vortex awaits your exploration.
Welcome to the beginning of your journey..."
```

## Technical Implementation Notes

### Required Components
1. `ProfileManager` class
2. `QuestionnaireEngine` class
3. `CryptoWallet` integration
4. `DatabaseConnector` class
5. `ProfileMatrix` calculator

### Data Storage
- Encrypted local storage for session data
- Blockchain integration for permanent records
- Distributed database for profile metrics

### Security Considerations
- End-to-end encryption for all personal data
- Secure key storage
- Privacy-preserving analytics

### Next Steps
1. Implement `intro.py` module
2. Create question database
3. Set up profile storage system
4. Integrate cryptocurrency functionality
5. Design and implement UI for questionnaire 