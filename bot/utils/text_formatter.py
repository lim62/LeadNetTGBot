from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from bot.database.requests import get_all_users

async def format_database(session_maker: async_sessionmaker[AsyncSession]) -> None:
    users: list[dict] = await get_all_users(session_maker=session_maker)
    headers = ["ID", "Username", "Date", "Stage", "Messages", "Offer", "Stories", "FromRef"]
    rows = [headers]
    for u in users:
        rows.append([
            str(u["telegram_id"]),
            str(u["username"]),
            str(u["date"]),
            str(u["stage"]),
            str(u["messages"]),
            str(u["offer"]),
            str(u["stories"]),
            str(u["from_ref"]),
        ])
    col_widths = [max(len(row[i]) for row in rows) for i in range(len(headers))]
    lines = []
    for row in rows:
        line = " | ".join(row[i].ljust(col_widths[i]) for i in range(len(headers)))
        lines.append(line)
    table_text = "\n".join(lines)
    with open(('bot/media/database.txt'), 'w') as file:
        file.write(table_text)