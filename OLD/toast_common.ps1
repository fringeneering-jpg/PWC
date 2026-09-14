# Shared helpers for the security-alert toast popups (show_popup.ps1 / show_image_popup.ps1).
# Handles bottom-right stacking so multiple simultaneous alerts don't overlap.

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$Script:ToastW = 320
$Script:MarginRight = 16
$Script:MarginBottom = 16
$Script:Gap = 10
$Script:DurationMs = 30000

function Request-ToastSlot {
    $slotDir = Join-Path $env:TEMP "alert_toasts"
    New-Item -ItemType Directory -Path $slotDir -Force | Out-Null
    $mutex = New-Object System.Threading.Mutex($false, "Global\AlertToastSlotMutex")
    $hasLock = $false
    try {
        $hasLock = $mutex.WaitOne()
    } catch [System.Threading.AbandonedMutexException] {
        # The mutex was abandoned by a crashed process, but the current thread still acquired it.
        $hasLock = $true
    }
    try {
        $slot = 0
        while ($true) {
            $lockFile = Join-Path $slotDir "slot_$slot.lock"
            if (-not (Test-Path $lockFile)) { break }
            $ownerPid = Get-Content $lockFile -ErrorAction SilentlyContinue
            $alive = $false
            if ($ownerPid) { $alive = [bool](Get-Process -Id $ownerPid -ErrorAction SilentlyContinue) }
            if (-not $alive) { break }
            $slot++
        }
        Set-Content -Path (Join-Path $slotDir "slot_$slot.lock") -Value $PID
        return $slot
    } finally {
        if ($hasLock) {
            $mutex.ReleaseMutex() | Out-Null
        }
        $mutex.Dispose()
    }
}

function Unlock-ToastSlot([int]$Slot) {
    $lockFile = Join-Path $env:TEMP "alert_toasts\slot_$Slot.lock"
    Remove-Item $lockFile -ErrorAction SilentlyContinue
}

function New-ToastForm {
    $form = New-Object System.Windows.Forms.Form
    $form.FormBorderStyle = "None"
    $form.TopMost = $true
    $form.ShowInTaskbar = $false
    $form.StartPosition = "Manual"
    $form.BackColor = [System.Drawing.Color]::FromArgb(32, 32, 32)
    return $form
}

function Move-ToastForm($Form, [int]$Slot) {
    $workArea = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
    $Form.Left = $workArea.Right - $Form.Width - $Script:MarginRight
    $Form.Top = $workArea.Bottom - $Form.Height - $Script:MarginBottom - ($Slot * ($Form.Height + $Script:Gap))
}

function Show-ToastForm($Form, [int]$Slot) {
    $dismiss = { $Form.Close() }.GetNewClosure()
    $Form.Add_Click($dismiss)
    foreach ($ctrl in $Form.Controls) {
        $ctrl.Add_Click($dismiss)
        $ctrl.Cursor = [System.Windows.Forms.Cursors]::Hand
    }

    $timer = New-Object System.Windows.Forms.Timer
    $timer.Interval = $Script:DurationMs
    $timer.Add_Tick({ $timer.Stop(); $Form.Close() }.GetNewClosure())
    $timer.Start()

    $Form.Add_FormClosed({ Unlock-ToastSlot $Slot }.GetNewClosure())
    $Form.Add_Shown({ $Form.Activate() })
    [void]$Form.ShowDialog()
}
