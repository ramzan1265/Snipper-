import requests

# CONFIGURATION
HELIX_API = '8cc47cf5-2ea2-4755-bb35-abfcdf15bfcc'
TELEGRAM_BOT_TOKEN = '7316108703:AAG2MPm9aolD5sdxKBo78uN4EnJaedhjx4Q'
TELEGRAM_CHAT_ID = '5377764075'

def get_wallets():
    url = 'https://api.helix.com/v1/wallets'
    headers = {'Authorization': f'Bearer {HELIX_API}'}
    response = requests.get(url, headers=headers)
    return response.json()

def filter_wallets(wallets):
    filtered = []
    for w in wallets:
        try:
            if (w['roi']['1d'] >= 10 and
                w['roi']['7d'] >= 70 and
                w['roi']['30d'] >= 300 and
                w['win_rate'] >= 90 and
                w['active']):
                filtered.append(w)
        except:
            continue
    return filtered

def send_to_telegram(wallet):
    message = f"""
Wallet: {wallet['address']}
Daily ROI: {wallet['roi']['1d']}x
Weekly ROI: {wallet['roi']['7d']}x
Monthly ROI: {wallet['roi']['30d']}x
Win Rate: {wallet['win_rate']}%
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    requests.post(url, data=data)

def main():
    wallets = get_wallets()
    top_wallets = filter_wallets(wallets)
    if top_wallets:
        for wallet in top_wallets[:10]:
            send_to_telegram(wallet)
    else:
        send_to_telegram({
            "address": "No wallet matched",
            "roi": {'1d': 0, '7d': 0, '30d': 0},
            "win_rate": 0
        })

if __name__ == "__main__":
    main()
