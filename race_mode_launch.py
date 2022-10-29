#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-
import rospy
import os
import time

def toggle_terminal_window_size():
    os.system("wmctrl -r ':ACTIVE:' -b toggle,fullscreen")

def clear_screen():
    os.system('clear')

def change_terminal_to_wsu_colors():#Change terminal to WSU colors.
    purple = "echo \"\033]10;#A200FF\007\""
    black = "echo \"\033]11;#000000\007\""
    os.system(purple)
    os.system(black)
    clear_screen()

def print_title_logo():
    title_logo = ("\t ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄\n"+
                  "\t▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌▐░░░░░░░░░░░▌\n"+
                  "\t▐░▌       ▐░▌ ▀▀▀▀█░█▀▀▀▀ ▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀█░█▀▀▀▀      ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░▌░▌     ▐░▌▐░█▀▀▀▀▀▀▀▀▀ \n"+
                  "\t▐░▌       ▐░▌     ▐░▌     ▐░▌          ▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌     ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌               ▐░▌     ▐░▌▐░▌    ▐░▌▐░▌          \n"+
                  "\t▐░▌   ▄   ▐░▌     ▐░▌     ▐░▌          ▐░▌       ▐░▌▐░▌          ▐░█▄▄▄▄▄▄▄█░▌     ▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌               ▐░▌     ▐░▌ ▐░▌   ▐░▌▐░▌ ▄▄▄▄▄▄▄▄ \n"+
                  "\t▐░▌  ▐░▌  ▐░▌     ▐░▌     ▐░▌          ▐░▌       ▐░▌▐░▌          ▐░░░░░░░░░░░▌     ▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌               ▐░▌     ▐░▌  ▐░▌  ▐░▌▐░▌▐░░░░░░░░▌\n"+
                  "\t▐░▌ ▐░▌░▌ ▐░▌     ▐░▌     ▐░▌          ▐░▌       ▐░▌▐░▌          ▐░█▀▀▀▀▀▀▀█░▌     ▐░▌          ▐░█▀▀▀▀█░█▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░▌               ▐░▌     ▐░▌   ▐░▌ ▐░▌▐░▌ ▀▀▀▀▀▀█░▌\n"+
                  "\t▐░▌▐░▌ ▐░▌▐░▌     ▐░▌     ▐░▌          ▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌     ▐░▌          ▐░▌     ▐░▌  ▐░▌       ▐░▌▐░▌               ▐░▌     ▐░▌    ▐░▌▐░▌▐░▌       ▐░▌\n"+
                  "\t▐░▌░▌   ▐░▐░▌ ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌     ▐░▌          ▐░▌      ▐░▌ ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄  ▄▄▄▄█░█▄▄▄▄ ▐░▌     ▐░▐░▌▐░█▄▄▄▄▄▄▄█░▌\n"+
                  "\t▐░░▌     ▐░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░▌       ▐░▌     ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌      ▐░░▌▐░░░░░░░░░░░▌\n"+
                  "\t ▀▀       ▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀       ▀            ▀         ▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀ \n"+
                  "==================================================================================================================================================================================================\n")
    print(title_logo)

def print_developers_logo():
    software_logo = ("\t███████  ██████  ███████ ████████ ██     ██  █████  ██████  ███████        ████████ ██████  ███████ ██    ██ ██ ███    ██     ██       █████  ██   ██ ███████\n"+
                    "\t██      ██    ██ ██         ██    ██     ██ ██   ██ ██   ██ ██      ██        ██    ██   ██ ██      ██    ██ ██ ████   ██     ██      ██   ██ ██  ██  ██     \n"+
                    "\t███████ ██    ██ █████      ██    ██  █  ██ ███████ ██████  █████             ██    ██████  █████   ██    ██ ██ ██ ██  ██     ██      ███████ █████   █████  \n"+
                    "\t     ██ ██    ██ ██         ██    ██ ███ ██ ██   ██ ██   ██ ██      ██        ██    ██   ██ ██       ██  ██  ██ ██  ██ ██     ██      ██   ██ ██  ██  ██     \n"+
                    "\t███████  ██████  ██         ██     ███ ███  ██   ██ ██   ██ ███████           ██    ██   ██ ███████   ████   ██ ██   ████     ███████ ██   ██ ██   ██ ███████\n")
    hardware_logo = ("\t██   ██  █████  ██████  ██████  ██     ██  █████  ██████  ███████        ██████  ██    ██  █████  ███    ██     ██████  ███████ ██ ██████  ██   ██ ███████  █████  ██████ \n"+
                     "\t██   ██ ██   ██ ██   ██ ██   ██ ██     ██ ██   ██ ██   ██ ██      ██     ██   ██  ██  ██  ██   ██ ████   ██     ██   ██ ██      ██ ██   ██ ██   ██ ██      ██   ██ ██   ██\n"+
                     "\t███████ ███████ ██████  ██   ██ ██  █  ██ ███████ ██████  █████          ██████    ████   ███████ ██ ██  ██     ██████  █████   ██ ██   ██ ███████ █████   ███████ ██   ██\n"+
                     "\t██   ██ ██   ██ ██   ██ ██   ██ ██ ███ ██ ██   ██ ██   ██ ██      ██     ██   ██    ██    ██   ██ ██  ██ ██     ██   ██ ██      ██ ██   ██ ██   ██ ██      ██   ██ ██   ██\n"+
                     "\t██   ██ ██   ██ ██   ██ ██████   ███ ███  ██   ██ ██   ██ ███████        ██   ██    ██    ██   ██ ██   ████     ██   ██ ███████ ██ ██████  ██   ██ ███████ ██   ██ ██████\n")
    underline = ("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print(software_logo)
    print(hardware_logo)
    print(underline)

def get_launch():
    launch_menu_title = ("--------------------------\n"+
                        "       Launch Modes       \n"+
                        "--------------------------")
    launch_menu_options = ("1. Race\n" +
                           "2. Test\n" +
                           "3. Keyboard Teleop\n" +
                           "4. Exit The Program\n")
    print(launch_menu_title)
    print(launch_menu_options)
    launch_option = input("Please Enter a number corresponding to the desired Launch Mode: ")
    return launch_option
#This function takes an integer launch_option as a parameter and launches
#The corresponding option. 1 = Race, 2 = Test, 3 = Keyboard Teleop.
def launch_select(launch_option):
    launch_option = launch_option -1
    # Function to convert number into string
    # Switcher is dictionary data type here
    def numbers_to_launchmodes(argument):
        switcher = {
            0: "gnome-terminal -x sh -c \"roslaunch --wait wildcat_racing race.launch; bash\" && rosrun teleop_twist_keyboard teleop_twist_keyboard.py",
            1: "gnome-terminal -x sh -c \"roslaunch --wait wildcat_racing test.launch; bash\" && rosrun teleop_twist_keyboard teleop_twist_keyboard.py",
            2: "gnome-terminal -x sh -c \"roslaunch --wait wildcat_racing teleop.launch; bash\" && rosrun teleop_twist_keyboard teleop_twist_keyboard.py",
            3: "exit",
        }

        # get() method of dictionary data type returns
        # value of passed argument if it is present
        # in dictionary otherwise second argument will
        # be assigned as default value of passed argument
        return switcher.get(argument, "invalid")

    mode = numbers_to_launchmodes(launch_option)
    if mode != "invalid":
        if "race" in mode:
            print("Initiating Race Mode....")
        if "test" in mode:
            print("Initiating Test Mode....")
        if "teleop" in mode:
            print("initiating Keyboard Teleop Mode")
        if mode != "exit":
            #launch roscore if not exiting.
            os.system("gnome-terminal -x sh -c \"roscore; bash\"")
            #launch rosnodes via launch file corresponding with mode
            os.system(mode)
        else:
            kill_ros()
            time.sleep(1)
            exit()

    else:
        print("Invalid Launch Argument")
        time.sleep(1)
        clear_screen()
        launch_option = get_launch()
        launch_select(launch_option)

def kill_ros():
        os.system("rosnode kill -a")
        time.sleep(1)
        os.system("killall roscore")
        print("Command to kill roscore sent.")
        time.sleep(1)
        os.system("killall bash")

#global boolean flag for whether this is the first run of main.
app_first_run = True
def main():
    #allowing this function to modify the global variable.
    global app_first_run
    clear_screen()
    if app_first_run:
        app_first_run = False
        toggle_terminal_window_size()
        change_terminal_to_wsu_colors()
    print_title_logo()
    print_developers_logo()
    launch_option = int(get_launch())
    clear_screen()
    launch_select(launch_option)
    input("\nPress Enter to Kill ROS")
    kill_ros()
    app_first_run = False
    main()

if __name__ == '__main__':
    main()
