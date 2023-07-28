class Ironman:
    ### on screen coordinates ###
    humane_icon = (40, 677)
    setting_icon = (750, 670)
    wifi_setting = (150, 150)
    wifi_icon = (170, 100)
    bluetooth_icon = (400, 100)
    accept_icon = (545, 580)
    reject_icon = (260, 575)
    end_call_icon = (406, 570)

    def __init__(self, device):
        self.dut = device
        # self.dut.go_to_ironman_ui()

    def switch_wifi_status(self):
        self.dut.long_press(self.humane_icon[0], self.humane_icon[1])
        self.dut.click(self.wifi_icon[0], self.wifi_icon[1])

    def accept_incoming_call(self):
        self.dut.click(self.accept_icon[0], self.accept_icon[1])
    
    def reject_incoming_call(self):
        self.dut.click(self.reject_icon[0], self.reject_icon[1])
    
    def end_ongoing_call(self):
        self.dut.click(self.end_call_icon[0], self.end_call_icon[1])