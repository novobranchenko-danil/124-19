import console_handler as ch
import data_handler as dh
import utils as u


while True:
    ch.print_prompt()
    source = input().lower()
    if u.handle_special_commands(source):
        continue
    elif source == "loc":
        dh.get_loc_info(source)
    elif source == "zip":
        dh.get_zip_info(source)
    elif source == "dist":
        dh.get_dist_info(source)
    else:
        ch.print_invalid_command()
        ch.print_newline()
        continue
