import time
import datetime
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.clock import Clock
from kivy.core.window import Window

class NeonPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 16
        self.spacing = 12
        self.size_hint = (0.92, 0.82)

        # Draw Neon Glowing Background Card
        with self.canvas.before:
            # Card Background
            Color(0.05, 0.08, 0.12, 0.95)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20, 20, 20, 20])
            # Glowing Cyan Border
            Color(0.0, 0.9, 0.8, 1)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 20), width=2.2)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, 20)


class SGODFloatingApp(App):
    def build(self):
        Window.clearcolor = (0.02, 0.03, 0.05, 1)

        root = AnchorLayout(anchor_x='center', anchor_y='center')
        panel = NeonPanel()

        # 1. Header Bar (Title & Close Button)
        header = BoxLayout(size_hint_y=0.10, spacing=5)
        lbl_title = Label(
            text="[b][color=#00E5FF]⚡ S_GOD X NUMBER PANEL[/color][/b]",
            markup=True,
            font_size="15sp",
            halign="left",
            valign="middle"
        )
        lbl_title.bind(size=lbl_title.setter('text_size'))

        btn_close = Button(
            text="✖",
            font_size="14sp",
            size_hint=(0.15, 1),
            background_normal="",
            background_color=(0.1, 0.2, 0.25, 0.8)
        )
        header.add_widget(lbl_title)
        header.add_widget(btn_close)
        panel.add_widget(header)

        # 2. Target Period & Countdown Section
        period_box = BoxLayout(orientation='vertical', size_hint_y=0.20, spacing=2)
        lbl_target_tag = Label(
            text="[color=#FFD700]⏳ TARGET PERIOD[/color]",
            markup=True,
            font_size="12sp"
        )
        self.lbl_period = Label(
            text="[b][color=#FFFFFF]20260825100010001[/color][/b]",
            markup=True,
            font_size="17sp"
        )
        self.lbl_timer = Label(
            text="[color=#00E5FF]TIMER: 00:60[/color]",
            markup=True,
            font_size="13sp"
        )
        period_box.add_widget(lbl_target_tag)
        period_box.add_widget(self.lbl_period)
        period_box.add_widget(self.lbl_timer)
        panel.add_widget(period_box)

        # 3. Status Pill
        self.lbl_status = Label(
            text="[b][color=#00FFA3]● SCAN ACTIVE[/color]  [color=#AAAAAA]LAST: 8 (BIG)[/color][/b]",
            markup=True,
            font_size="12sp",
            size_hint_y=0.08
        )
        panel.add_widget(self.lbl_status)

        # 4. Signal Waves & Prediction Box
        pred_box = BoxLayout(orientation='vertical', size_hint_y=0.28, spacing=4)
        lbl_sig_tag = Label(
            text="[color=#FF5252]● SIGNAL PREDICTION[/color]",
            markup=True,
            font_size="11sp"
        )
        
        self.lbl_waves = Label(
            text="[b][color=#00E5FF] ▂ ▄ █ ▄ ▂ [/color][/b]",
            markup=True,
            font_size="24sp"
        )
        
        self.lbl_result = Label(
            text="[b][color=#FF1744]BIG / SMALL[/color][/b]",
            markup=True,
            font_size="20sp"
        )

        self.lbl_target_nums = Label(
            text="[b][color=#00E5FF]🎯 TARGET: [/color][color=#FFD700][ ... ][/color][/b]",
            markup=True,
            font_size="13sp"
        )

        pred_box.add_widget(lbl_sig_tag)
        pred_box.add_widget(self.lbl_waves)
        pred_box.add_widget(self.lbl_result)
        pred_box.add_widget(self.lbl_target_nums)
        panel.add_widget(pred_box)

        # 5. Scan Action Button
        self.btn_scan = Button(
            text="[b][color=#000000]⚡ SCANNING LIVE DATA...[/color][/b]",
            markup=True,
            font_size="14sp",
            size_hint_y=0.15,
            background_normal="",
            background_color=(0.0, 0.9, 0.7, 1)
        )
        self.btn_scan.bind(on_release=self.trigger_manual_scan)
        panel.add_widget(self.btn_scan)

        # 6. Bottom Brand Tag
        lbl_footer = Label(
            text="[color=#555555]◆ S_GOD VIP ENGINE • ACTIVE ◆[/color]",
            markup=True,
            font_size="10sp",
            size_hint_y=0.06
        )
        panel.add_widget(lbl_footer)

        root.add_widget(panel)

        # Real-time Loops
        self.is_scanning = False
        Clock.schedule_interval(self.update_period_and_timer, 1.0)
        Clock.schedule_interval(self.animate_wave_bars, 0.4)

        return root

    def update_period_and_timer(self, dt):
        now = datetime.datetime.utcnow()
        # Calculate Current Minute & Seconds
        seconds = 60 - now.second
        self.lbl_timer.text = f"[color=#00E5FF]TIMER: 00:{seconds:02d}[/color]"

        # Generate exact period string: YYYYMMDD10001XXXX
        total_minute_of_day = now.hour * 60 + now.minute + 1
        period_str = f"{now.strftime('%Y%m%d')}10001{total_minute_of_day:04d}"
        self.lbl_period.text = f"[b][color=#FFFFFF]{period_str}[/color][/b]"

        # Auto-Predict at start of round
        if seconds == 59 and not self.is_scanning:
            self.run_prediction_logic()

    def animate_wave_bars(self, dt):
        if self.is_scanning:
            wave_frames = [
                "  ▂ ▃ ▄ ▅ ▆ ▇ ",
                " ▇ ▆ ▅ ▄ ▃ ▂   ",
                " ▂ ▄ █ ▆ ▄ ▂ █ ",
                " █ ▄ ▂ ▄ █ ▄ ▂ "
            ]
            self.lbl_waves.text = f"[b][color=#00E5FF]{random.choice(wave_frames)}[/color][/b]"

    def trigger_manual_scan(self, instance):
        self.is_scanning = True
        self.btn_scan.text = "[b][color=#000000]🔄 ANALYZING DATA STREAM...[/color][/b]"
        self.lbl_target_nums.text = "[b][color=#00E5FF]🎯 TARGET: [/color][color=#FFAB40][ SCANNING... ][/color][/b]"
        Clock.schedule_once(self.finish_scan, 2.0)

    def finish_scan(self, dt):
        self.run_prediction_logic()
        self.is_scanning = False
        self.btn_scan.text = "[b][color=#000000]⚡ SCAN AGAIN[/color][/b]"

    def run_prediction_logic(self):
        choice = random.choice(["BIG", "SMALL"])
        if choice == "BIG":
            self.lbl_result.text = "[b][color=#00E5FF]BIG[/color][/b]"
            nums = [5, 6, 7, 8, 9]
            random.shuffle(nums)
            selected = sorted(nums[:3])
            self.lbl_target_nums.text = f"[b][color=#00E5FF]🎯 NUMBERS: [/color][color=#FFD700]{selected}[/color][/b]"
        else:
            self.lbl_result.text = "[b][color=#FF1744]SMALL[/color][/b]"
            nums = [0, 1, 2, 3, 4]
            random.shuffle(nums)
            selected = sorted(nums[:3])
            self.lbl_target_nums.text = f"[b][color=#00E5FF]🎯 NUMBERS: [/color][color=#FFD700]{selected}[/color][/b]"

if __name__ == '__main__':
    SGODFloatingApp().run()
