#!/usr/bin/env python3
"""
Caesar Cipher - Standalone Implementation
A simple command-line Caesar cipher tool for encryption and decryption.
"""

import string
import argparse
import sys

class CaesarCipher:
    """
    A class to handle Caesar cipher encryption and decryption operations.
    """
    
    def __init__(self):
        self.alphabet = string.ascii_lowercase
        self.alphabet_upper = string.ascii_uppercase
    
    def encrypt(self, text, shift):
        """
        Encrypt text using Caesar cipher with given shift.
        
        Args:
            text (str): The text to encrypt
            shift (int): The number of positions to shift (1-25)
            
        Returns:
            str: The encrypted text
        """
        return self._process_text(text, shift)
    
    def decrypt(self, text, shift):
        """
        Decrypt text using Caesar cipher with given shift.
        
        Args:
            text (str): The text to decrypt
            shift (int): The number of positions to shift (1-25)
            
        Returns:
            str: The decrypted text
        """
        return self._process_text(text, -shift)
    
    def _process_text(self, text, shift):
        """
        Process text with the given shift value.
        
        Args:
            text (str): The text to process
            shift (int): The shift value (positive for encrypt, negative for decrypt)
            
        Returns:
            str: The processed text
        """
        result = []
        
        for char in text:
            if char.islower():
                # Handle lowercase letters
                shifted_pos = (ord(char) - ord('a') + shift) % 26
                result.append(chr(shifted_pos + ord('a')))
            elif char.isupper():
                # Handle uppercase letters
                shifted_pos = (ord(char) - ord('A') + shift) % 26
                result.append(chr(shifted_pos + ord('A')))
            else:
                # Keep non-alphabetic characters unchanged
                result.append(char)
        
        return ''.join(result)
    
    def analyze_text(self, text):
        """
        Analyze the given text and return statistics.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Statistics about the text
        """
        stats = {
            'total_chars': len(text),
            'letters': sum(1 for c in text if c.isalpha()),
            'uppercase': sum(1 for c in text if c.isupper()),
            'lowercase': sum(1 for c in text if c.islower()),
            'digits': sum(1 for c in text if c.isdigit()),
            'spaces': sum(1 for c in text if c.isspace()),
            'punctuation': sum(1 for c in text if c in string.punctuation),
            'letter_frequency': {}
        }
        
        # Calculate letter frequency
        for char in text.lower():
            if char.isalpha():
                stats['letter_frequency'][char] = stats['letter_frequency'].get(char, 0) + 1
        
        return stats
    
    def brute_force_decrypt(self, text):
        """
        Attempt to decrypt text using all possible shifts (1-25).
        
        Args:
            text (str): The text to decrypt
            
        Returns:
            list: List of tuples (shift, decrypted_text)
        """
        results = []
        for shift in range(1, 26):
            decrypted = self.decrypt(text, shift)
            results.append((shift, decrypted))
        return results
    
    def interactive_mode(self):
        """
        Run the Caesar cipher in interactive mode.
        """
        print("🔐 Caesar Cipher Interactive Mode")
        print("=" * 40)
        
        while True:
            print("\nOptions:")
            print("1. Encrypt text")
            print("2. Decrypt text")
            print("3. Brute force decrypt")
            print("4. Analyze text")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                self._encrypt_interactive()
            elif choice == '2':
                self._decrypt_interactive()
            elif choice == '3':
                self._brute_force_interactive()
            elif choice == '4':
                self._analyze_interactive()
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 5.")
    
    def _encrypt_interactive(self):
        """Interactive encryption mode."""
        text = input("Enter text to encrypt: ")
        if not text:
            print("❌ No text provided.")
            return
        
        try:
            shift = int(input("Enter shift value (1-25): "))
            if shift < 1 or shift > 25:
                print("❌ Shift must be between 1 and 25.")
                return
        except ValueError:
            print("❌ Invalid shift value. Please enter a number.")
            return
        
        encrypted = self.encrypt(text, shift)
        print(f"\n✅ Original:  {text}")
        print(f"🔒 Encrypted: {encrypted}")
    
    def _decrypt_interactive(self):
        """Interactive decryption mode."""
        text = input("Enter text to decrypt: ")
        if not text:
            print("❌ No text provided.")
            return
        
        try:
            shift = int(input("Enter shift value (1-25): "))
            if shift < 1 or shift > 25:
                print("❌ Shift must be between 1 and 25.")
                return
        except ValueError:
            print("❌ Invalid shift value. Please enter a number.")
            return
        
        decrypted = self.decrypt(text, shift)
        print(f"\n✅ Original:  {text}")
        print(f"🔓 Decrypted: {decrypted}")
    
    def _brute_force_interactive(self):
        """Interactive brute force mode."""
        text = input("Enter text to brute force decrypt: ")
        if not text:
            print("❌ No text provided.")
            return
        
        print(f"\n🔍 Brute force decryption results for: {text}")
        print("-" * 50)
        
        results = self.brute_force_decrypt(text)
        for shift, decrypted in results:
            print(f"Shift {shift:2d}: {decrypted}")
    
    def _analyze_interactive(self):
        """Interactive text analysis mode."""
        text = input("Enter text to analyze: ")
        if not text:
            print("❌ No text provided.")
            return
        
        stats = self.analyze_text(text)
        
        print(f"\n📊 Text Analysis for: {text}")
        print("-" * 50)
        print(f"Total characters: {stats['total_chars']}")
        print(f"Letters: {stats['letters']}")
        print(f"Uppercase: {stats['uppercase']}")
        print(f"Lowercase: {stats['lowercase']}")
        print(f"Digits: {stats['digits']}")
        print(f"Spaces: {stats['spaces']}")
        print(f"Punctuation: {stats['punctuation']}")
        
        if stats['letter_frequency']:
            print("\nLetter frequency:")
            for letter, count in sorted(stats['letter_frequency'].items()):
                print(f"  {letter}: {count}")

def main():
    """Main function to run the Caesar cipher."""
    parser = argparse.ArgumentParser(description='Caesar Cipher Tool')
    parser.add_argument('--text', '-t', type=str, help='Text to process')
    parser.add_argument('--shift', '-s', type=int, help='Shift value (1-25)')
    parser.add_argument('--encrypt', '-e', action='store_true', help='Encrypt the text')
    parser.add_argument('--decrypt', '-d', action='store_true', help='Decrypt the text')
    parser.add_argument('--brute-force', '-b', action='store_true', help='Brute force decrypt')
    parser.add_argument('--analyze', '-a', action='store_true', help='Analyze text')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    cipher = CaesarCipher()
    
    if args.interactive:
        cipher.interactive_mode()
        return
    
    if not args.text:
        print("❌ Please provide text using --text or use --interactive mode")
        print("Use --help for more information")
        sys.exit(1)
    
    if args.brute_force:
        print(f"🔍 Brute force decryption results for: {args.text}")
        print("-" * 50)
        results = cipher.brute_force_decrypt(args.text)
        for shift, decrypted in results:
            print(f"Shift {shift:2d}: {decrypted}")
    
    elif args.analyze:
        stats = cipher.analyze_text(args.text)
        print(f"📊 Text Analysis for: {args.text}")
        print("-" * 50)
        print(f"Total characters: {stats['total_chars']}")
        print(f"Letters: {stats['letters']}")
        print(f"Uppercase: {stats['uppercase']}")
        print(f"Lowercase: {stats['lowercase']}")
        print(f"Digits: {stats['digits']}")
        print(f"Spaces: {stats['spaces']}")
        print(f"Punctuation: {stats['punctuation']}")
        
        if stats['letter_frequency']:
            print("\nLetter frequency:")
            for letter, count in sorted(stats['letter_frequency'].items()):
                print(f"  {letter}: {count}")
    
    elif args.encrypt:
        if not args.shift:
            print("❌ Please provide a shift value using --shift")
            sys.exit(1)
        
        if args.shift < 1 or args.shift > 25:
            print("❌ Shift must be between 1 and 25")
            sys.exit(1)
        
        encrypted = cipher.encrypt(args.text, args.shift)
        print(f"✅ Original:  {args.text}")
        print(f"🔒 Encrypted: {encrypted}")
    
    elif args.decrypt:
        if not args.shift:
            print("❌ Please provide a shift value using --shift")
            sys.exit(1)
        
        if args.shift < 1 or args.shift > 25:
            print("❌ Shift must be between 1 and 25")
            sys.exit(1)
        
        decrypted = cipher.decrypt(args.text, args.shift)
        print(f"✅ Original:  {args.text}")
        print(f"🔓 Decrypted: {decrypted}")
    
    else:
        print("❌ Please specify an operation: --encrypt, --decrypt, --brute-force, --analyze, or --interactive")
        print("Use --help for more information")

if __name__ == '__main__':
    main() 