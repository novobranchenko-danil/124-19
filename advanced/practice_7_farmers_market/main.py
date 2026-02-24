import utils as u
import console_handler as ch

while True:
    ch.print_prompt()
    user_input = input().lower()
    u.handle_special_commands(user_input)
    u.command_processing(user_input)
