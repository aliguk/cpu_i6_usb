class CountErrors:
    MEMORY = "Memory"
    UART = "Uart"
    ALU = "Alu"

    WDT = "WDT is worked"
    STM_START = "STM Start"
    SH_START = "CPUi6 Start"
    BUFFER_FILL = "Buffer fill"
    UNRESET_DEVICE = "Unreset CPUi6"
    TIMEOUT_SPI = "Timeout SPI"
    MACHINE = "MACHINE"
    INVALID_OPCODE = "Invalid OPCODE"

    errors_count = {MEMORY: 0,
                    UART: 0,
                    ALU: 0}

    # errors_flags = {MEMORY: False,
    #                 UART: False,
    #                 ALU: False}

    events_count = {WDT: 0,
                    STM_START: 0,
                    BUFFER_FILL: 0,
                    UNRESET_DEVICE: 0,
                    SH_START: 0,
                    TIMEOUT_SPI: 0,
                    MACHINE: 0,
                    INVALID_OPCODE: 0}

    # def error_flag_set(self, item):
    #     self.errors_flags[item] = True

    def error_inc(self, key, number):
        self.errors_count[key] += number
        # for key, value in self.errors_flags.items():
        #     if value is True:
        #         self.errors_count[key] += number
        #         self.errors_flags[key] = False

    def event_inc(self, item):
        self.events_count[item] += 1
