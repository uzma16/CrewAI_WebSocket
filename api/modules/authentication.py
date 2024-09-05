import httpx
from dotenv import load_dotenv
import os
load_dotenv()

class Authentication:
    def __init__(self, headers: dict = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}) -> None:
        self.base_url = os.getenv("BASE_URL")
        self.headers = headers

class SignUp(Authentication):
    def __init__(self) -> None:
        """
        Initializes the SignUp instance.
        """
        super().__init__()

    def signup_base(self, email: str) -> dict:
        """
        Sends a POST request to the signup endpoint of the API with the provided email.
        
        Args:
            email (str): The email of the user signing up.
        
        Returns:
            dict: A dictionary containing the status code of the response and the JSON response.

        Sample Response:
        {
            "success": true,
            "message": "OTP sent to your email. Please verify to complete registration."
        }
        """
        payload = {
            "email": str(email)
        }
        print(payload)
        response = httpx.post(
            f"{self.base_url}/api/v1/auth/signup",
            json=payload,
            headers=self.headers
        )
        return {
            "status": response.status_code,
            "response": response.json()
        }
    
    def signup_otp(self, email: str, otp: int) -> dict:
        """
        Sends a POST request to verify the OTP for a given email.
        
        Args:
            email (str): The email of the user for OTP verification.
            otp (int): The OTP to be verified.
        
        Returns:
            dict: A dictionary containing the status code of the response and the JSON response.
        
        Sample Response:
        {
            "success": true,
            "message": "OTP verified, proceed to set your password"
        }
        """
        payload = {
            "email": email,
            "otp": otp
        }
        response = httpx.post(
            f"{self.base_url}/api/v1/auth/verify-otp",
            json=payload,
            headers=self.headers
        )
        return {
            "status": response.status_code,
            "response": response.json()
        }
    
    def add_password(self, email: str, password: str) -> dict:
        """
        Sends a POST request to create a password for a given email.

        Args:
            email (str): The email of the user for password creation.
            password (str): The password to be created.

        Returns:
            dict: A dictionary containing the status code of the response and the JSON response.

        Sample Response:
        {
            "success": true,
            "message": "Registration complete. You can now login."
        }
        """
        payload = {
            "email": email,
            "password": password
        }
        response = httpx.post(
            f"{self.base_url}/api/v1/auth/create-password",
            json=payload,
            headers=self.headers
        )
        return {
            "status": response.status_code,
            "response": response.json() 
        }

class Login(Authentication):
    def __init__(self) -> None:
        """
        Initializes the Login instance.
        """
        super().__init__()

    def login_base(self, email: str, password: str) -> dict:
        """
        Sends a POST request to the login endpoint of the API with the provided email and password.

        Args:
            email (str): The email of the user logging in.
            password (str): The password of the user logging in.

        Returns:
            dict: A dictionary containing the status code of the response and the JSON response.

        Sample Response:
        {
            "success": true,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjYzOTUxYzhhZDA2YmJmOTJkYmMyM2ExIn0sImlhdCI6MTcxNTAzMjU0OSwiZXhwIjoxNzE1MDUwNTQ5fQ.oN4elhxPaSMNMSY2wjGd3MxjejSmtc6VPuNlJLnFEOs",
            "user": {
                "_id": "663951c8ad06bbf92dbc23a1",
                "email": "deep.shanky@gmail.com",
                "isVerified": true,
                "status": "active",
                "role": "USER",
                "isDeleted": false,
                "createdAt": "2024-05-06T21:55:20.677Z",
                "updatedAt": "2024-05-06T21:55:20.677Z",
                "__v": 0,
                "password": "$2a$10$T4quiKZKMyNcrElcQXRk7eiVpnLbJh7iPqxhdRHZq3.CgP9JcQ4tu"
            }
        }
        """
        payload = {
            "email": email,
            "password": password
        }
        response = httpx.post(
            f"{self.base_url}/api/v1/auth/login",
            json=payload,
            headers=self.headers
        )
        return {
            "status": response.status_code,
            "response": response.json() 
        }

