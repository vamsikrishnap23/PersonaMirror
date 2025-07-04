import json

def extract_required_cookies(input_file='raw_cookies.json', output_file='cookies.json'):
    with open(input_file, 'r', encoding='utf-8') as f:
        browser_cookies = json.load(f)

    required_keys = ['auth_token', 'ct0']
    twikit_cookies = {}

    for cookie in browser_cookies:
        name = cookie.get('name')
        value = cookie.get('value')
        if name in required_keys:
            twikit_cookies[name] = value

    if len(twikit_cookies) != len(required_keys):
        print("❌ Missing required cookies. Found:", list(twikit_cookies.keys()))
        print("✅ Make sure you're logged in to Twitter/X and export cookies *after* logging in.")
        return

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(twikit_cookies, f, indent=4)

    print(f"✅ Reformatted cookies saved to `{output_file}`")
    print("📎 Contents:", twikit_cookies)


if __name__ == "__main__":
    extract_required_cookies()
