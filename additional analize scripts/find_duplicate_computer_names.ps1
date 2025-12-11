<#
Find duplicate "Computer Name" entries in the tab-delimited file
`Data export/020_all.txt`. Outputs a table of duplicates and counts.

Usage:
  powershell -ExecutionPolicy Bypass -File find_duplicate_computer_names.ps1
#>

$path = "D:\BigFix and ILMT analizer\Data export\020_all.txt"

if (-not (Test-Path -Path $path)) {
    Write-Error "File not found: $path"
    exit 1
}

# Import as tab-separated; treat empty as null
$data = Import-Csv -Path $path -Delimiter "`t"

# Group by Computer Name and select those with more than one occurrence
$dupes = $data |
    Group-Object -Property 'Computer Name' |
    Where-Object { $_.Count -gt 1 } |
    Select-Object @{Name = 'Computer Name'; Expression = { $_.Name } }, Count

if ($dupes) {
    Write-Output "Found duplicate Computer Name values:"
    $dupes | Format-Table -AutoSize
} else {
    Write-Output "No duplicates found."
}

# Optional: export details of the duplicate rows to a CSV for inspection.
# Uncomment to enable.
# $data |
#     Group-Object -Property 'Computer Name' |
#     Where-Object { $_.Count -gt 1 } |
#     ForEach-Object { $_.Group } |
#     Export-Csv -Path "D:\BigFix and ILMT analizer\Data export\020_all_duplicates.csv" -NoTypeInformation

