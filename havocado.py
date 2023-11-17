import subprocess
import telebot

# Initialize Telegram bot
bot_token = 'your_telegram_token'
bot = telebot.TeleBot(bot_token)
chat_id = 'your_telegram_chat_id'

# Function to send message to Telegram
def send_telegram_message(message):
    bot.send_message(chat_id, message)

# Function to monitor real-time output
def monitor_output():
    process = subprocess.Popen(['./havoc', 'server', '--profile', './profiles/havoc.yaotl', '-v', '--debug'],
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.STDOUT,
                               text=True)
    
    capture = False
    captured_text = ""
    line_count = 0

    for line in iter(process.stdout.readline, ''):
        line = line.strip()
        print(line)
        if "[DBUG] [agent.ParseDemonRegisterRequest:382]" in line:
            capture = True
            captured_text = ""
            line_count = 0
            continue

        if capture:
            if line_count < 5:  # Capture the next 4 lines
                captured_text += line + '\n'
                line_count += 1
            else:  # After 4 lines, send the message and stop capturing
                send_telegram_message('Got a new connection Sir!\n'+captured_text.strip())
                capture = False

# Run the output monitoring
monitor_output()
