# login.py
import asyncio
from twikit import Client

async def main():
    client = Client(language='en-US')

    await client.login(  # ✅ Await login
        auth_info_1="your_username_or_email",
        auth_info_2="your_username_or_email",
        password="your_password"
    )

    client.save_cookies("cookies.json")  # ✅ Do NOT await this — it's a regular function
    print("✅ Cookies saved.")

if __name__ == "__main__":
    asyncio.run(main())
