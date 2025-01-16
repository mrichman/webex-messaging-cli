#!/usr/bin/env python3.13

import requests
import os

from dotenv import load_dotenv

class WebexMessenger:
    def __init__(self):
        
        print("loading .env")
        load_dotenv()

        # Get token from environment variable for security
        self.token = os.environ.get('WEBEX_ACCESS_TOKEN')
        print(self.token)
        if not self.token:
            raise ValueError("WEBEX_ACCESS_TOKEN environment variable not set")
        
        self.base_url = "https://webexapis.com/v1"
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def send_message(self, room_id=None, person_email=None, text=None):
        """
        Send a message to either a room or a person
        """
        endpoint = f"{self.base_url}/messages"
        
        payload = {}
        if room_id:
            payload['roomId'] = room_id
        elif person_email:
            payload['toPersonEmail'] = person_email
        else:
            raise ValueError("Either room_id or person_email must be provided")
            
        if text:
            payload['text'] = text
        else:
            raise ValueError("Message text must be provided")

        response = requests.post(endpoint, headers=self.headers, json=payload)
        return response.json()

    def list_rooms(self):
        """
        List all rooms the authenticated user is in
        """
        endpoint = f"{self.base_url}/rooms"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()

def main():
    try:
        messenger = WebexMessenger()
        
        # Example: List rooms
        rooms = messenger.list_rooms()

        print(rooms)

        print("Your Rooms:")
        for room in rooms.get('items', []):
            print(f"Room ID: {room['id']}")
            print(f"Room Title: {room['title']}\n")

            # Example: Send a message to a specific email
            # messenger.send_message(person_email="recipient@example.com", text="Hello from CLI!")
            
            # Example: Send a message to a room
            messenger.send_message(room_id=room['id'], text="Hello room!")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
