# Create a session to maintain cookies
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession

# Login
Write-Host "Logging in..."
$loginResult = Invoke-RestMethod -Uri "http://localhost:8001/api/auth/login" -Method POST -WebSession $session
Write-Host "Login Result:"
$loginResult | ConvertTo-Json

# Get user info
Write-Host "`nGetting user info..."
$userResult = Invoke-RestMethod -Uri "http://localhost:8001/api/auth/user" -WebSession $session
Write-Host "User Info:"
$userResult | ConvertTo-Json 