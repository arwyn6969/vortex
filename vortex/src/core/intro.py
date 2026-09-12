"""Introduction sequence handler for Vortex of Enlightenment."""

import secrets
import time
from typing import Optional
from dataclasses import dataclass
from .crypto.wallet import BitcoinWallet, WalletInfo
from .lattice import Lattice, LatticeError


@dataclass
class PlayerProfile:
    """Basic player profile information."""
    name: str
    wallet: Optional[WalletInfo] = None
    questionnaire_complete: bool = False
    bound_address: Optional[str] = None


class IntroSequence:
    """Handles the game's introduction sequence."""

    def __init__(self):
        self.profile: Optional[PlayerProfile] = None
        self.wallet_handler = BitcoinWallet()
        self.lattice = Lattice()

    def _slow_print(self, text: str, delay: float = 0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def _get_yes_no_input(self, prompt: str) -> bool:
        while True:
            response = input(f"{prompt} (yes/no): ").lower().strip()
            if response in ['yes', 'y']:
                return True
            if response in ['no', 'n']:
                return False
            print("Please answer 'yes' or 'no'.")

    def start_game_prompt(self) -> bool:
        self._slow_print("\nWould you like to play a game?")
        return self._get_yes_no_input("")

    def show_disclaimers(self) -> bool:
        disclaimer = """
\u26a0\ufe0f IMPORTANT NOTICE \u26a0\ufe0f

Before we proceed, you must understand and acknowledge the following:

1. PRIVACY WARNING
   - Share only what you're comfortable with
   - Your experience will directly reflect your level of engagement
   - Local saves are not encrypted; never enter secrets

2. PARTICIPATION NOTICE
   - All entities are welcome (humans, bots, alternate personas)
   - Authentic participation will be rewarded
   - Your responses shape your unique journey

3. LEDGER NOTICE
   - Binding a Bitcoin address is optional and happens in Kingdom (Malkhut)
   - Prove the address by signing a challenge — never paste a private key
   - Vortex does not take custody of keys, seeds, or WIF
   - Public holdings may later color multipliers at the ledger floor
"""
        self._slow_print(disclaimer)
        return self._get_yes_no_input("\nDo you acknowledge and accept these terms?")

    def get_player_name(self) -> str:
        self._slow_print("""
In this realm, you may be known by any name you choose.
Names hold power. Choose wisely.
""")
        while True:
            name = input("\nWhat name shall we know you by? ").strip()
            if name:
                return name
            print("A name must be provided.")

    def handle_crypto_integration(
        self,
        current_pond: str = "Crown Pond",
    ) -> Optional[WalletInfo]:
        """Note an address only. Keys never enter this process."""
        self._slow_print("""
The ancient ledgers await, but they belong to Kingdom — Malkhut —
not to the first gate.

You may leave an address as a name on the door.
You will prove it later by signing a challenge with your own wallet.
Never paste a private key, WIF, or seed here.
""")
        if not self._get_yes_no_input("Leave an address to bind later?"):
            self._slow_print("\nThe ledger can wait. The tree still opens.")
            return None
        address = input("\nBitcoin address: ").strip()
        if not address:
            self._slow_print("No address given. Continuing unbound.")
            return None
        if _looks_like_secret(address):
            self._slow_print(
                "\nThat looks like a key, not an address. "
                "Rejected. Do not paste secrets into the Vortex."
            )
            return None
        challenge = secrets.token_hex(16)
        self._slow_print(
            f"\nRemember this challenge for Kingdom Pond:\n  {challenge}"
        )
        self._slow_print(
            "Sign it with your wallet when you reach Malkhut. "
            f"Address noted: {address}"
        )
        return _address_only_wallet(address)

    def show_voight_kampff_intro(self):
        intro_text = """
In the year 2019, the Tyrell Corporation developed a test...
A test of empathy, consciousness, and being.
Today, we present you with our own version.
Not to determine if you're human...
But to understand WHO you are.

\"Have you ever retired a human by mistake?\" - Blade Runner, 2019
"""
        self._slow_print(intro_text)
        input("\nPress Enter to begin the questionnaire...")

    def run_sequence(self) -> Optional[PlayerProfile]:
        if not self.start_game_prompt():
            self._slow_print("Perhaps another time. Farewell.")
            return None
        if not self.show_disclaimers():
            self._slow_print("We understand. Until next time.")
            return None
        name = self.get_player_name()
        wallet = self.handle_crypto_integration(current_pond="Crown Pond")
        bound = wallet.address if wallet else None
        self.profile = PlayerProfile(
            name=name,
            wallet=wallet,
            bound_address=bound,
        )
        self.show_voight_kampff_intro()
        return self.profile


def _looks_like_secret(value: str) -> bool:
    text = value.strip()
    if " " in text and len(text.split()) in {12, 15, 18, 21, 24}:
        return True
    if text[:1] in {"5", "K", "L", "c", "9"} and 50 <= len(text) <= 53:
        return True
    if len(text) in {64, 66} and all(c in "0123456789abcdefABCDEF" for c in text):
        return True
    return False


def _address_only_wallet(address: str) -> WalletInfo:
    from .crypto.wallet import AddressType
    guessed = AddressType.LEGACY
    lowered = address.lower()
    if lowered.startswith("bc1p"):
        guessed = AddressType.TAPROOT
    elif lowered.startswith("bc1q") or lowered.startswith("tb1q"):
        guessed = AddressType.SEGWIT_NATIVE
    elif address.startswith("3") or address.startswith("2"):
        guessed = AddressType.SEGWIT_NESTED
    return WalletInfo(
        address=address,
        address_type=guessed,
        private_key=None,
        mnemonic=None,
    )
