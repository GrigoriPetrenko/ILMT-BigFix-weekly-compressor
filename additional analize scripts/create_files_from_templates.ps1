
$targetPath = $PSScriptRoot

$filesToCreate = @(
    "001_Delayed Data Upload.txt",
    "005_Failed Scan.txt",
    "006_Missing Scan.txt",
    "007_Scan Not Uploaded.txt",
    "009_No Scan Data.txt",
    "011_No VM Manager Data.txt",
    "012_Outdated VM Manager Data.txt",
    "013_Outeted Scan.txt",
    "020_all.txt",
    "021_notrep.txt",
    "022_ILMT_computers_list.txt",
    "023_CMDB_active.txt",
    "024_unlocated_servers.txt",
    "099_Capacity Scan.txt"
)

foreach ($fileName in $filesToCreate) {
    New-Item -Path (Join-Path $targetPath $fileName) -ItemType File -Force | Out-Null
}
