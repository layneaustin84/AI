using System;
using System.Collections.Generic;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TurboController
{
    public partial class MainForm : Form
    {
        private readonly Dictionary<string, ushort> _virtualKeys = new()
        {
            { "Left Mouse", 0x01 },
            { "Right Mouse", 0x02 },
            { "Middle Mouse", 0x04 },
            { "Space", 0x20 },
            { "Tab", 0x09 },
            { "Enter", 0x0D },
            { "Shift", 0x10 },
            { "Ctrl", 0x11 },
            { "Alt", 0x12 },
            { "Q", 0x51 },
            { "E", 0x45 },
            { "R", 0x52 },
            { "F", 0x46 },
            { "1", 0x31 },
            { "2", 0x32 },
            { "3", 0x33 },
            { "4", 0x34 },
            { "5", 0x35 },
            { "6", 0x36 },
        };

        private readonly Dictionary<string, ushort> _triggerKeys = new()
        {
            { "Left Mouse", 0x01 },
            { "Right Mouse", 0x02 },
            { "Middle Mouse", 0x04 },
            { "Ctrl", 0x11 },
            { "Shift", 0x10 },
            { "Alt", 0x12 },
            { "Space", 0x20 },
            { "Tab", 0x09 },
            { "Caps Lock", 0x14 },
            { "Q", 0x51 },
            { "E", 0x45 },
            { "R", 0x52 },
            { "F", 0x46 },
        };

        private const int HotkeyId = 1;
        private const uint ModAlt = 0x1;
        private const uint ModControl = 0x2;
        private const int WmHotkey = 0x0312;

        private readonly NotifyIcon _trayIcon;
        private readonly ContextMenuStrip _trayMenu;
        private CancellationTokenSource? _cancellationSource;
        private Task? _turboTask;
        private bool _turboEnabled;

        private Label _statusLabel = null!;
        private ComboBox _triggerSelect = null!;
        private ComboBox _virtualSelect = null!;
        private TrackBar _speedSlider = null!;
        private NumericUpDown _speedNumeric = null!;
        private Button _startButton = null!;
        private Button _stopButton = null!;
        private Button _aboutButton = null!;

        public MainForm()
        {
            InitializeComponent();

            _trayMenu = new ContextMenuStrip();
            _trayMenu.Items.Add("Toggle Turbo", null, (_, _) => ToggleTurbo());
            _trayMenu.Items.Add("Exit", null, (_, _) => Application.Exit());

            _trayIcon = new NotifyIcon
            {
                Icon = SystemIcons.Application,
                Visible = true,
                Text = "Turbo Controller",
                ContextMenuStrip = _trayMenu
            };
        }

        protected override void OnLoad(EventArgs e)
        {
            base.OnLoad(e);
            RegisterHotkey();
        }

        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            base.OnFormClosing(e);
            UnregisterHotkey();
            StopTurbo();
            _trayIcon.Visible = false;
        }

        protected override void WndProc(ref Message m)
        {
            if (m.Msg == WmHotkey && m.WParam.ToInt32() == HotkeyId)
            {
                ToggleTurbo();
            }

            base.WndProc(ref m);
        }

        private void InitializeComponent()
        {
            Text = "Turbo Controller";
            MinimumSize = new Size(480, 380);
            StartPosition = FormStartPosition.CenterScreen;

            var header = new Label
            {
                Text = "Turbo Controller",
                Font = new Font("Segoe UI", 16, FontStyle.Bold),
                AutoSize = true,
                Location = new Point(20, 15)
            };

            var description = new Label
            {
                Text = "Hold a trigger key to auto-press a virtual key. Toggle globally with Ctrl+Alt+T.",
                AutoSize = true,
                MaximumSize = new Size(420, 0),
                Location = new Point(20, 50)
            };

            _statusLabel = new Label
            {
                Text = "Status: Idle",
                AutoSize = true,
                ForeColor = Color.DarkRed,
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                Location = new Point(20, 85)
            };

            var triggerLabel = new Label
            {
                Text = "Trigger button (hold):",
                AutoSize = true,
                Location = new Point(20, 120)
            };

            _triggerSelect = new ComboBox
            {
                Location = new Point(200, 115),
                Width = 200,
                DropDownStyle = ComboBoxStyle.DropDownList
            };
            _triggerSelect.Items.AddRange(new List<string>(_triggerKeys.Keys).ToArray());
            _triggerSelect.SelectedIndex = 0;

            var virtualLabel = new Label
            {
                Text = "Virtual button (sent):",
                AutoSize = true,
                Location = new Point(20, 155)
            };

            _virtualSelect = new ComboBox
            {
                Location = new Point(200, 150),
                Width = 200,
                DropDownStyle = ComboBoxStyle.DropDownList
            };
            _virtualSelect.Items.AddRange(new List<string>(_virtualKeys.Keys).ToArray());
            _virtualSelect.SelectedIndex = 3; // Space

            var speedLabel = new Label
            {
                Text = "Turbo speed (ms):",
                AutoSize = true,
                Location = new Point(20, 190)
            };

            _speedSlider = new TrackBar
            {
                Minimum = 10,
                Maximum = 200,
                TickFrequency = 10,
                Value = 60,
                Location = new Point(200, 185),
                Width = 200
            };
            _speedSlider.ValueChanged += (_, _) => _speedNumeric.Value = _speedSlider.Value;

            _speedNumeric = new NumericUpDown
            {
                Minimum = 10,
                Maximum = 200,
                Increment = 5,
                Value = 60,
                Location = new Point(410, 185),
                Width = 60
            };
            _speedNumeric.ValueChanged += (_, _) => _speedSlider.Value = (int)_speedNumeric.Value;

            _startButton = new Button
            {
                Text = "Start (Ctrl+Alt+T)",
                Location = new Point(20, 235),
                Width = 180,
                Height = 35,
                BackColor = Color.FromArgb(0, 122, 204),
                ForeColor = Color.White
            };
            _startButton.Click += (_, _) => StartTurbo();

            _stopButton = new Button
            {
                Text = "Stop",
                Location = new Point(210, 235),
                Width = 90,
                Height = 35,
                Enabled = false
            };
            _stopButton.Click += (_, _) => StopTurbo();

            _aboutButton = new Button
            {
                Text = "About",
                Location = new Point(310, 235),
                Width = 90,
                Height = 35
            };
            _aboutButton.Click += (_, _) => ShowAbout();

            var minimizeButton = new Button
            {
                Text = "Minimize to tray",
                Location = new Point(20, 280),
                Width = 180,
                Height = 30
            };
            minimizeButton.Click += (_, _) =>
            {
                Hide();
                _trayIcon.ShowBalloonTip(1500, "Turbo Controller", "Running in the background.", ToolTipIcon.Info);
            };

            Controls.AddRange(new Control[]
            {
                header, description, _statusLabel, triggerLabel, _triggerSelect, virtualLabel,
                _virtualSelect, speedLabel, _speedSlider, _speedNumeric, _startButton,
                _stopButton, _aboutButton, minimizeButton
            });
        }

        private void RegisterHotkey()
        {
            if (!RegisterHotKey(Handle, HotkeyId, ModControl | ModAlt, (int)Keys.T))
            {
                MessageBox.Show("Unable to register hotkey Ctrl+Alt+T", "Hotkey", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void UnregisterHotkey()
        {
            UnregisterHotKey(Handle, HotkeyId);
        }

        private void ToggleTurbo()
        {
            if (_turboEnabled)
            {
                StopTurbo();
            }
            else
            {
                StartTurbo();
            }
        }

        private void StartTurbo()
        {
            if (_turboEnabled)
            {
                return;
            }

            _turboEnabled = true;
            _statusLabel.Text = "Status: Active";
            _statusLabel.ForeColor = Color.ForestGreen;
            _startButton.Enabled = false;
            _stopButton.Enabled = true;

            _cancellationSource = new CancellationTokenSource();
            _turboTask = Task.Run(() => RunTurboLoop(_cancellationSource.Token));
        }

        private void StopTurbo()
        {
            if (!_turboEnabled)
            {
                return;
            }

            _turboEnabled = false;
            _statusLabel.Text = "Status: Idle";
            _statusLabel.ForeColor = Color.DarkRed;
            _startButton.Enabled = true;
            _stopButton.Enabled = false;

            _cancellationSource?.Cancel();
            _turboTask = null;
        }

        private void RunTurboLoop(CancellationToken token)
        {
            var triggerKey = _triggerKeys[(string)_triggerSelect.InvokeUi(() => _triggerSelect.SelectedItem!)];
            var virtualKey = _virtualKeys[(string)_virtualSelect.InvokeUi(() => _virtualSelect.SelectedItem!)];

            while (!token.IsCancellationRequested)
            {
                if (IsTriggerPressed(triggerKey))
                {
                    SendTurboKey(virtualKey);
                }
                Thread.Sleep(5);
            }
        }

        private void SendTurboKey(ushort key)
        {
            int delay;
            try
            {
                delay = (int)_speedNumeric.InvokeUi(() => _speedNumeric.Value);
            }
            catch (InvalidOperationException)
            {
                delay = 60;
            }

            var down = new INPUT
            {
                type = InputType.INPUT_KEYBOARD,
                U = new InputUnion { ki = new KEYBDINPUT { wVk = key } }
            };

            var up = new INPUT
            {
                type = InputType.INPUT_KEYBOARD,
                U = new InputUnion { ki = new KEYBDINPUT { wVk = key, dwFlags = 0x0002 } }
            };

            SendInput(1, new[] { down }, Marshal.SizeOf<INPUT>());
            Thread.Sleep(delay);
            SendInput(1, new[] { up }, Marshal.SizeOf<INPUT>());
            Thread.Sleep(delay);
        }

        private bool IsTriggerPressed(ushort key)
        {
            short state = GetAsyncKeyState(key);
            return (state & 0x8000) != 0;
        }

        private void ShowAbout()
        {
            var info = "Turbo Controller\n" +
                       "- Hold a trigger key to repeatedly send a virtual key.\n" +
                       "- Adjust speed between 10-200ms.\n" +
                       "- Use Ctrl+Alt+T to toggle anywhere.";
            MessageBox.Show(info, "About", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        #region Win32

        [DllImport("user32.dll")]
        private static extern bool RegisterHotKey(IntPtr hWnd, int id, uint fsModifiers, int vk);

        [DllImport("user32.dll")]
        private static extern bool UnregisterHotKey(IntPtr hWnd, int id);

        [DllImport("user32.dll")]
        private static extern short GetAsyncKeyState(int vKey);

        [DllImport("user32.dll", SetLastError = true)]
        private static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);

        [StructLayout(LayoutKind.Sequential)]
        private struct INPUT
        {
            public InputType type;
            public InputUnion U;
        }

        [StructLayout(LayoutKind.Explicit)]
        private struct InputUnion
        {
            [FieldOffset(0)] public MOUSEINPUT mi;
            [FieldOffset(0)] public KEYBDINPUT ki;
            [FieldOffset(0)] public HARDWAREINPUT hi;
        }

        [StructLayout(LayoutKind.Sequential)]
        private struct MOUSEINPUT
        {
            public int dx;
            public int dy;
            public int mouseData;
            public int dwFlags;
            public uint time;
            public IntPtr dwExtraInfo;
        }

        [StructLayout(LayoutKind.Sequential)]
        private struct KEYBDINPUT
        {
            public ushort wVk;
            public ushort wScan;
            public uint dwFlags;
            public uint time;
            public IntPtr dwExtraInfo;
        }

        [StructLayout(LayoutKind.Sequential)]
        private struct HARDWAREINPUT
        {
            public int uMsg;
            public short wParamL;
            public short wParamH;
        }

        private enum InputType
        {
            INPUT_MOUSE = 0,
            INPUT_KEYBOARD = 1,
            INPUT_HARDWARE = 2
        }

        #endregion
    }

    internal static class ControlExtensions
    {
        public static T InvokeUi<T>(this Control control, Func<T> func)
        {
            if (control.InvokeRequired)
            {
                return (T)control.Invoke(func);
            }
            return func();
        }
    }
}
