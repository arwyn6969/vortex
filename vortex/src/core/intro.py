"""Introduction sequence handler for Vortex of Enlightenment."""

import time
from typing import Optional
from dataclasses import dataclass
from .crypto.wallet import BitcoinWallet, WalletInfo

@dataclass
class PlayerProfile:
    """Basic player profile information."""
    name: str
    wallet: Optional[WalletInfo] = None
    questionnaire_complete: bool = False
    
class IntroSequence:
    """Handles the game's introduction sequence."""
    
    def __init__(self):
        """Initialize the introduction sequence."""
        self.profile: Optional[PlayerProfile] = None
        self.wallet_handler = BitcoinWallet()
        
    def _slow_print(self, text: str, delay: float = 0.03):
        """Print text slowly for dramatic effect."""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
        
    def _get_yes_no_input(self, prompt: str) -> bool:
        """Get a yes/no input from the user."""
        while True:
            response = input(f"{prompt} (yes/no): ").lower().strip()
            if response in ['yes', 'y']:
                return True
            if response in ['no', 'n']:
                return False
            print("Please answer 'yes' or 'no'.")
            
    def start_game_prompt(self) -> bool:
        """Display the initial game prompt."""
        self._slow_print("\nWould you like to play a game?")
        return self._get_yes_no_input("")
        
    def show_disclaimers(self) -> bool:
        """Display important disclaimers and warnings."""
        disclaimer = """
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

3. CRYPTOCURRENCY NOTICE
   - You may provide your own Bitcoin wallet or receive a new one
   - All transactions are recorded on the public blockchain
   - Never share your private keys with anyone
"""
        self._slow_print(disclaimer)
        return self._get_yes_no_input("\nDo you acknowledge and accept these terms?")
        
    def get_player_name(self) -> str:
        """Get the player's chosen name."""
        self._slow_print("""
In this realm, you may be known by any name you choose.
Names hold power. Choose wisely.
""")
        while True:
            name = input("\nWhat name shall we know you by? ").strip()
            if name:
                return name
            print("A name must be provided.")
            
    def handle_crypto_integration(self) -> WalletInfo:
        """Handle cryptocurrency wallet integration."""
        self._slow_print("""
The ancient ledgers await...
Do you possess a Bitcoin private key you wish to bind to your journey?
""")
        
        if self._get_yes_no_input(""):
            self._slow_print("""
Please enter your private key in WIF format.
Warning: Never share your private key with anyone else.
Your key will be used only to verify ownership and check balance.
""")
            key = input("Private key: ").strip()
            wallet, message = self.wallet_handler.process_wallet_input(key)
        else:
            wallet, message = self.wallet_handler.process_wallet_input()
            
        self._slow_print(f"\n{message}")
        
        if wallet.balance > 0:
            self._slow_print(f"\nDetected balance: {wallet.balance} BTC")
            self._slow_print("Your journey will be enriched by your existing resources...")
        else:
            self._slow_print("\nYour journey begins with an empty vessel...")
            self._slow_print("But fear not, for wealth comes in many forms...")
            
        return wallet
            
    def show_voight_kampff_intro(self):
        """Display the Voight-Kampff questionnaire introduction."""
        intro_text = """
In the year 2019, the Tyrell Corporation developed a test...
A test of empathy, consciousness, and being.
Today, we present you with our own version.
Not to determine if you're human...
But to understand WHO you are.

"Have you ever retired a human by mistake?" - Blade Runner, 2019
"""
        self._slow_print(intro_text)
        input("\nPress Enter to begin the questionnaire...")
        
    def run_sequence(self) -> Optional[PlayerProfile]:
        """Run the complete introduction sequence."""
        if not self.start_game_prompt():
            self._slow_print("Perhaps another time. Farewell.")
            return None
            
        if not self.show_disclaimers():
            self._slow_print("We understand. Until next time.")
            return None
            
        name = self.get_player_name()
        wallet = self.handle_crypto_integration()
        
        self.profile = PlayerProfile(name=name, wallet=wallet)
        
        self.show_voight_kampff_intro()
        # TODO: Implement actual questionnaire
        
        return self.profile 