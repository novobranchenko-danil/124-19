import app_controler as u
import console_handler as ch

command = ""
while command != "q":
    ch.print_prompt()
    command = input().lower().strip()
    u.command_processing(command)


