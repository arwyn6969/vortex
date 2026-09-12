#!/usr/bin/env python3
"""Retired key-taking helper: signing belongs in the user's wallet."""
import sys

def main():
    print("This helper is retired. Create a challenge at Kingdom in VORTEX, "
          "sign the exact message in your own wallet, and paste back only its signature. "
          "Never pass a private key to this program.", file=sys.stderr)
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
