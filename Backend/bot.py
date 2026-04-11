"""
bot.py — VTU Genius AI Telegram Bot
Run:  python bot.py

Commands:
  /start              — Welcome message
  /subjects <sem>     — List subjects for Sem N (2022 scheme)
  /notes <subject>    — Get notes for a subject
  /important <sub>    — Important questions for a subject
  /ask <question>     — AI-powered answer (with RAG)
  /exam <subject>     — Start a mock exam
  /help               — Show all commands
"""

import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv(override=True)

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
except ImportError:
    print("❌  python-telegram-bot not installed.")
    print("    Run:  pip install python-telegram-bot")
    sys.exit(1)

# ── Config ─────────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_BASE        = os.getenv("BOT_API_BASE", "http://127.0.0.1:8000")

if not TELEGRAM_TOKEN:
    print("❌  TELEGRAM_BOT_TOKEN not set in .env")
    print("    Add this line to Backend/.env:")
    print("    TELEGRAM_BOT_TOKEN=<your_token_from_@BotFather>")
    sys.exit(1)

# ── Helpers ────────────────────────────────────────────────────────────────────
async def post(endpoint: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.post(f"{API_BASE}{endpoint}", json=payload)
        return r.json()

async def get(endpoint: str) -> dict:
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get(f"{API_BASE}{endpoint}")
        return r.json()

def bullet(items: list[str]) -> str:
    return "\n".join(f"• {i}" for i in items)

# ── Handlers ───────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🧠 *VTU Genius AI* — Your Smart Study Buddy!\n\n"
        "I help VTU students with notes, questions, and AI tutoring.\n\n"
        "*Commands:*\n"
        "📚 `/subjects <sem>` — List subjects _(e.g. /subjects 3)_\n"
        "📘 `/notes <subject>` — Get notes _(e.g. /notes DSA)_\n"
        "⭐ `/important <sub>` — Important questions\n"
        "🔮 `/expected <sub>` — Expected exam questions\n"
        "📄 `/pyq <sub>` — Previous year questions\n"
        "🚀 `/aptitude <company>` — Company Aptitude PYQs\n"
        "🎤 `/mock <company> <role>` — Mock Interview Questions\n"
        "📝 `/exam <sub>` — Start a mock exam\n"
        "🤖 `/ask <question>` — Ask the AI anything\n"
        "❓ `/help` — Show this message again\n\n"
        "_Placement Features now active!_"
    )
    await update.message.reply_markdown(msg)


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await cmd_start(update, ctx)


async def cmd_subjects(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /subjects <sem_number>  — e.g. /subjects 3")
        return

    sem = ctx.args[0]
    try:
        data = await get(f"/subjects?scheme=2022&sem={sem}")
        subs = data.get("subjects", [])
        if not subs:
            await update.message.reply_text(f"❌ No subjects found for Sem {sem} (2022 scheme).")
            return
        text = f"📚 *Subjects — Sem {sem} (2022):*\n\n" + bullet(subs)
        await update.message.reply_markdown(text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Backend error: {e}")


async def cmd_notes(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /notes <subject>  — e.g. /notes DSA")
        return

    subject = " ".join(ctx.args)
    try:
        data  = await post("/get-content", {"subject": subject})
        notes = data.get("notes", "No notes available.")
        text  = f"📘 *Notes — {subject}:*\n\n{notes[:3000]}"
        await update.message.reply_markdown(text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")


async def cmd_important(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /important <subject>  — e.g. /important OS")
        return

    subject = " ".join(ctx.args)
    try:
        data = await post("/important-questions", {"subject": subject})
        qs   = data.get("questions", [])
        if not qs:
            await update.message.reply_text(f"❌ No important questions for {subject}.")
            return
        text = f"⭐ *Important Questions — {subject}:*\n\n" + bullet(qs)
        await update.message.reply_markdown(text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")


async def cmd_expected(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /expected <subject>  — e.g. /expected DBMS")
        return

    subject = " ".join(ctx.args)
    try:
        data = await post("/expected-questions", {"subject": subject, "scheme": "2022", "sem": "4"})
        qs   = data.get("questions", [])
        if not qs:
            await update.message.reply_text(f"❌ No expected questions for {subject}.")
            return
        text = f"🔮 *Expected Questions — {subject}:*\n\n" + bullet(qs)
        await update.message.reply_markdown(text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")


async def cmd_pyq(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /pyq <subject>  — e.g. /pyq CN")
        return

    subject = " ".join(ctx.args)
    try:
        data = await post("/generate", {"subject": subject})
        qs   = data.get("questions", [])
        if not qs:
            await update.message.reply_text(f"❌ No PYQs found for {subject}.")
            return
        text = f"📄 *Previous Year Questions — {subject}:*\n\n" + "\n".join(f"{i+1}. {q}" for i,q in enumerate(qs))
        await update.message.reply_markdown(text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")


async def cmd_exam(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /exam <subject>  — e.g. /exam TOC")
        return

    subject = " ".join(ctx.args)
    try:
        data = await post("/exam/start", {"subject": subject})
        qs   = data.get("questions", [])
        if not qs:
            await update.message.reply_text(f"❌ No exam questions for {subject}.")
            return
        text = (
            f"📝 *Mock Exam — {subject}*\n"
            "_Answer each question briefly in your own words:_\n\n"
            + "\n\n".join(f"*Q{i+1}.* {q}" for i,q in enumerate(qs))
        )
        await update.message.reply_markdown(text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")


async def cmd_ask(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("Usage: /ask <your question>  — e.g. /ask What is BFS?")
        return

    question = " ".join(ctx.args)
    await update.message.reply_text("🤖 Thinking…")

    try:
        data   = await post("/ask", {"question": question, "subject": ""})
        answer = data.get("answer", "No response.")
        # Telegram has 4096 char limit
        for chunk in [answer[i:i+4000] for i in range(0, len(answer), 4000)]:
            await update.message.reply_text(chunk)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")


# Fallback for plain messages
async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text:
        await update.message.reply_text("🤖 Thinking…")
        try:
            data   = await post("/ask", {"question": text, "subject": ""})
            answer = data.get("answer", "No response.")
            for chunk in [answer[i:i+4000] for i in range(0, len(answer), 4000)]:
                await update.message.reply_text(chunk)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Error reaching AI: {e}")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("🚀 VTU Genius AI Bot starting…")
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start",     cmd_start))
    app.add_handler(CommandHandler("help",      cmd_help))
    app.add_handler(CommandHandler("subjects",  cmd_subjects))
    app.add_handler(CommandHandler("notes",     cmd_notes))
    app.add_handler(CommandHandler("important", cmd_important))
    app.add_handler(CommandHandler("expected",  cmd_expected))
    app.add_handler(CommandHandler("pyq",       cmd_pyq))
    app.add_handler(CommandHandler("aptitude",  cmd_aptitude))
    app.add_handler(CommandHandler("mock",      cmd_mock))
    app.add_handler(CommandHandler("exam",      cmd_exam))
    app.add_handler(CommandHandler("ask",       cmd_ask))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
