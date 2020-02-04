import datetime
import time
import curses
import ComPort
import PrintMessage
import CountErrors

PORTNAME = "COM11"
THRESHOLD_ERRORS = 128

COM_WDT = "FFDA8000"
COM_UNRESET_DEVICE = "FFDA6000"
COM_TIMEOUT_SPI = "FFDAB000"
COM_STM_START = "FFDAF000"
COM_BUFFER_FILL = "FFDAF100"
COM_MACHINE = "FFDAD000"

SH_MEM_0 = "F0DA1000"
SH_MEM_1 = "F0DA1001"
SH_START = "F0DA2000"

print_mes = PrintMessage.PrintMessage()
com_port = ComPort.ComPort(portname=PORTNAME)
errors = CountErrors.CountErrors()

win = curses.initscr()
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)
win.addstr(3, 2, "Errors:")
win.addstr(6, 2, "Events:")
win.addstr(26, 2, " -- To Exit, press ESC -- ")

key = 0
number_errors = 0
count_errors = 0
count_package = 0

f_number_errors = False
f_errors = False

start_time = time.time()
try:
    while key != 27:
        key = win.getch()

        win.addstr(1, 2, datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        win.addstr(1, 24, "{0:.0f} seconds".format(time.time() - start_time))

        i = 4
        for name, value in errors.errors_count.items():
            win.addstr(i, 4, "{0:<8s} {1:<4d}".format(name, value))
            i += 1

        i = 7
        for name, value in errors.events_count.items():
            win.addstr(i, 4, "{0:<15s} {1:<4d}".format(name, value))
            i += 1

        win.addstr(17, 2, "{0:<17s} {1:<4d}".format("Packages", count_package))

        data = com_port.read()

        # print(data)

        if data == SH_START:
            print_mes.info(data, "Start CPUi6")
            errors.event_inc(errors.SH_START)
            number_errors = 0
            count_errors = 0
            f_number_errors = False
            f_errors = False

        elif data == COM_STM_START:
            print_mes.info(data, "Start STM32")
            errors.event_inc(errors.STM_START)

        elif data == COM_BUFFER_FILL:
            print_mes.error(data, "Buffer STM32 fill")
            errors.event_inc(errors.BUFFER_FILL)
            number_errors = 0
            count_errors = 0
            f_number_errors = False
            f_errors = False

        elif data == COM_WDT:
            print_mes.error(data, "WDT is worked")
            errors.event_inc(errors.WDT)

        elif data == COM_TIMEOUT_SPI:
            print_mes.error(data, "Timeout SPI")
            errors.event_inc(errors.TIMEOUT_SPI)

        elif data == COM_UNRESET_DEVICE:
            print_mes.error(data, "Unreset CPUi6")
            errors.event_inc(errors.UNRESET_DEVICE)
            number_errors = 0
            count_errors = 0
            f_number_errors = False
            f_errors = False

        elif data == COM_MACHINE:
            print_mes.error(data, "Machine Error")
            errors.event_inc(errors.MACHINE)

        elif data == SH_MEM_0:
            print_mes.info(data, "Memory 0")
            f_number_errors = True
            errors.error_flag_set(errors.MEMORY)

        elif data == SH_MEM_1:
            print_mes.info(data, "Memory 1")
            f_number_errors = True
            errors.error_flag_set(errors.MEMORY)

        elif f_number_errors is True:
            f_number_errors = False
            count_package += 1
            if int(data, 16) == 0:
                print_mes.info(data, "Number errors: 0")
            else:
                print_mes.error(data, "Number errors: {0:d}".format(int(data, 16)))
                number_errors = int(data, 16) * 2 if int(data, 16) < THRESHOLD_ERRORS else THRESHOLD_ERRORS * 2
                f_errors = True
                errors.error_inc(int(data, 16))

        elif f_errors is True:
            print_mes.error(data, "Error")
            count_errors += 1
            if count_errors == number_errors:
                count_errors = 0
                f_errors = False

        else:
            print_mes.error(data, "Invalid OPCODE")
            errors.event_inc(errors.INVALID_OPCODE)

finally:
    curses.endwin()
