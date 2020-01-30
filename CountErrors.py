class CountErrors:
    MEMORY = "Memory"

    WDT = "WDT is worked"
    STM_START = "STM Start"
    SH_START = "CPUi6 Start"
    BUFFER_FILL = "Buffer fill"
    UNRESET_DEVICE = "Unreset CPUi6"
    TIMEOUT_SPI = "Timeout SPI"
    MACHINE = "MACHINE"
    INVALID_OPCODE = "Invalid OPCODE"

    errors_count = {"Memory": 0}

    errors_flags = {"Memory": False}

    events_count = {"WDT is worked": 0,
                    "STM Start": 0,
                    "Buffer fill": 0,
                    "Unreset CPUi6": 0,
                    "CPUi6 Start": 0,
                    "Timeout SPI": 0,
                    "MACHINE": 0,
                    "Invalid OPCODE": 0}

    def error_flag_set(self, item):
        self.errors_flags[item] = True

    def error_inc(self, number):
        for key, value in self.errors_flags.items():
            if value is True:
                self.errors_count[key] += number
                self.errors_flags[key] = False

    def event_inc(self, item):
        self.events_count[item] += 1
