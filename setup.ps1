# Check if Node.js is installed
$nodeVersion = node --version 2>$null
if (-not $nodeVersion) {
    Write-Host "Node.js is not installed. Please follow these steps:"
    Write-Host "1. Visit https://nodejs.org/"
    Write-Host "2. Download and install the LTS version"
    Write-Host "3. Restart your terminal/PowerShell"
    Write-Host "4. Run this script again"
    exit 1
}

Write-Host "Node.js version: $nodeVersion"

# Check if npm is installed
$npmVersion = npm --version 2>$null
if (-not $npmVersion) {
    Write-Host "npm is not installed. Please reinstall Node.js to include npm."
    exit 1
}

Write-Host "npm version: $npmVersion"

# Install project dependencies
Write-Host "Installing project dependencies..."
npm install

# Verify installation
if ($LASTEXITCODE -eq 0) {
    Write-Host "Setup completed successfully!"
    Write-Host "You can now run 'npm start' to start the development server."
} else {
    Write-Host "Error: Failed to install dependencies. Please check the error messages above."
    exit 1
} 