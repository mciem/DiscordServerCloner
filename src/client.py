from tls_client import Session

def buildClient(proxy: str) -> None:
    headers = {
			"accept":             "*/*",
			"accept-language":    "en-US;q=0.8,en;q=0.7",
			"content-type":       "application/json",
            "connection":         "keep-alive",
			"host":               "discord.com",
			"origin":             "https://discord.com",
			"sec-ch-ua":          '"Chromium";v="117", "Google Chrome";v="117", "Not;A=Brand";v="99"',
			"sec-ch-ua-mobile":   "?0",
			"sec-ch-ua-platform": '"Windows"',
			"sec-fetch-dest":     "empty",
			"sec-fetch-mode":     "cors",
			"sec-fetch-site":     "same-origin",
			"user-agent":         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }
        
    session = Session(random_tls_extension_order=True, client_identifier='chrome_117', header_order=['accept', 'accept-language', 'accept-encoding', 'authorization', 'content-type', 'connection', 'cookie', 'host', 'origin', 'sec-ch-ua', 'sec-ch-ua-mobile', 'sec-ch-ua-platform', 'sec-fetch-dest', 'sec-fetch-mode', 'sec-fetch-site', 'user-agent', 'x-captcha-key', 'x-context-properties', 'x-debug-options', 'x-discord-locale', 'x-discord-timezone', 'x-fingerprint', 'x-track', 'x-super-properties'])
    session.proxies = f"http://{proxy}" if proxy != "" else None
    session.headers = headers
        
    session.cookies["locale"] = "pl"
        
    session.headers |= {
            "cookie": "; ".join(f"{k}={v}" for k,v in session.cookies.items()),
            "x-debug-options":    "bugReporterEnabled",
            "x-discord-locale":   "en-US",
            "x-discord-timezone": "Europe/Warsaw"
    }
        
    return session