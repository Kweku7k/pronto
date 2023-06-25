import asyncio

import urllib.request, urllib.parse


async def send_sms(phone,message, senderId):
    api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
    params = {"key":api_key,"to":phone,"msg":message,"sender_id":senderId}
    url = 'https://apps.mnotify.net/smsapi?'+ urllib.parse.urlencode(params)
    content = urllib.request.urlopen(url).read()
    print(content)
    print(url)
    print(f"Sending SMS to {phone}")

async def send_bulk_sms(recipients,message, senderId):
    tasks = []
    for recipient in recipients:
        tasks.append(send_sms(recipient,message, senderId))
    await asyncio.gather(*tasks)

# List of recipients

# # Run the event loop
# loop = asyncio.get_event_loop()
# loop.run_until_complete(send_bulk_sms(recipients))
# loop.close()
