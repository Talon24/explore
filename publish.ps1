if ("y" -eq (Read-Host -Prompt "Rebuild Project? (y)"))
{
    Write-Host -ForegroundColor Yellow "Removing old dist..."
    if (Test-Path dist) {
        Remove-Item dist -Recurse
        } else {
            Write-Host -ForegroundColor Yellow "Dist folder not found."
        }
    Write-Host -ForegroundColor Yellow "Building new dist..."
    python setup.py sdist bdist_wheel
    Write-Host -ForegroundColor DarkGreen "Finished Build"
}
if ("y" -eq (Read-Host -Prompt "Upload to Test PyPi? (y)"))
{
    Write-Host -ForegroundColor Yellow "Uploading to Test PyPi..."
    twine upload -r testpypi dist/* --verbose
    Write-Host -ForegroundColor DarkGreen "Finished!"
}
if ("y" -eq (Read-Host -Prompt "Upload to Productive PyPi? (y)"))
{
    Write-Host -ForegroundColor Yellow "Uploading to Test PyPi..."
    twine upload -r pypi dist/* --verbose
    Write-Host -ForegroundColor DarkGreen "Finished!"
}