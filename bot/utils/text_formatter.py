from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from bot.database.requests import get_all_users, get_all_accounts

async def format_database(session_maker: async_sessionmaker[AsyncSession]) -> None:
    users: list[dict] = await get_all_users(session_maker=session_maker)
    headers = ["ID", "Username", "Status", "Date", "Stage", "Messages", "Credit", "Prepared", "FromRef"]
    rows = [headers]
    for u in users:
        rows.append([
            str(u["telegram_id"]),
            str(u["username"]),
            str(u["status"]),
            str(u["date"]),
            str(u["stage"]),
            str(u["messages"]),
            str(u["credit"]),
            str(u["have_prepared"]),
            str(u["from_ref"]),
        ])
    col_widths = [max(len(row[i]) for row in rows) for i in range(len(headers))]
    lines = [" | ".join(row[i].ljust(col_widths[i]) for i in range(len(headers))) for row in rows]
    table_text = "\n".join(lines)
    with open('bot/media/database.txt', 'w') as file:
        file.write(table_text)
    
async def format_accounts_db(session_maker: async_sessionmaker[AsyncSession]) -> None:
    accounts: list[dict] = await get_all_accounts(session_maker=session_maker)
    headers = [
        "Phone", "API_ID", "API_Hash", "App_Version", "Device_Model",
        "System_Version", "Lang_Code", "Password", "Proxy_Scheme",
        "Proxy_Hostname", "Proxy_Port", "Proxy_Username", "Proxy_Password"
    ]
    rows = [headers]
    for acc in accounts:
        rows.append([
            str(acc["phone"]),
            str(acc["api_id"]),
            str(acc["api_hash"]),
            str(acc["app_version"]),
            str(acc["device_model"]),
            str(acc["system_version"]),
            str(acc["lang_code"]),
            str(acc["password"]),
            str(acc["proxy_scheme"]),
            str(acc["proxy_hostname"]),
            str(acc["proxy_port"]),
            str(acc["proxy_username"]),
            str(acc["proxy_password"]),
        ])
    col_widths = [max(len(row[i]) for row in rows) for i in range(len(headers))]
    lines = []
    for row in rows:
        line = " | ".join(row[i].ljust(col_widths[i]) for i in range(len(headers)))
        lines.append(line)
    table_text = "\n".join(lines)
    with open('bot/media/accounts_database.txt', 'w') as file:
        file.write(table_text)