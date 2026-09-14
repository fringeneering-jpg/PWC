param(
    [string]$Title,
    [string]$Message,
    [string]$ImagePath
)
. (Join-Path $PSScriptRoot "toast_common.ps1")

$slot = Request-ToastSlot
$form = New-ToastForm

$pad = 12
$maxImgH = 160
$img = [System.Drawing.Image]::FromFile($ImagePath)
$scale = [Math]::Min(1.0, [Math]::Min(($Script:ToastW - 2 * $pad) / $img.Width, $maxImgH / $img.Height))
$picW = [int]($img.Width * $scale)
$picH = [int]($img.Height * $scale)

$picBox = New-Object System.Windows.Forms.PictureBox
$picBox.Image = $img
$picBox.SizeMode = "Zoom"
$picBox.Width = $picW
$picBox.Height = $picH
$picBox.Top = $pad
$picBox.Left = [int](($Script:ToastW - $picW) / 2)
$form.Controls.Add($picBox)

$titleLbl = New-Object System.Windows.Forms.Label
$titleLbl.Text = $Title
$titleLbl.ForeColor = [System.Drawing.Color]::White
$titleLbl.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)
$titleLbl.AutoSize = $false
$titleLbl.Width = $Script:ToastW - 2 * $pad
$titleLbl.Height = 18
$titleLbl.Top = $picBox.Bottom + 8
$titleLbl.Left = $pad
$form.Controls.Add($titleLbl)

$msgLbl = New-Object System.Windows.Forms.Label
$msgLbl.Text = $Message
$msgLbl.ForeColor = [System.Drawing.Color]::Gainsboro
$msgLbl.Font = New-Object System.Drawing.Font("Segoe UI", 9)
$msgLbl.AutoSize = $true
$msgLbl.MaximumSize = New-Object System.Drawing.Size(($Script:ToastW - 2 * $pad), 0)
$msgLbl.Top = $titleLbl.Bottom + 4
$msgLbl.Left = $pad
$form.Controls.Add($msgLbl)

$form.Width = $Script:ToastW
$form.Height = $msgLbl.Bottom + $pad

Move-ToastForm $form $slot

$form.Add_FormClosed({
    $img.Dispose()
    Remove-Item $ImagePath -ErrorAction SilentlyContinue
}.GetNewClosure())

Show-ToastForm $form $slot
