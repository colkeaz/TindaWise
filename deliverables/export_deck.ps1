$ErrorActionPreference = 'Stop'
$deckPath = Join-Path $PSScriptRoot 'TindaWise_Pitch_Deck_Revised.pptx'
$pdfPath = Join-Path $PSScriptRoot 'TindaWise_Pitch_Deck_Revised.pdf'
$previewPath = Join-Path $PSScriptRoot 'reviews'
New-Item -ItemType Directory -Force -Path $previewPath | Out-Null
$powerpoint = New-Object -ComObject PowerPoint.Application
$presentation = $null
try {
    $presentation = $powerpoint.Presentations.Open($deckPath, $true, $false, $false)
    $presentation.SaveAs($pdfPath, 32)
    $presentation.Export($previewPath, 'PNG', 1600, 900)
    Write-Output "Exported PDF and $($presentation.Slides.Count) slide previews."
} finally {
    if ($null -ne $presentation) { $presentation.Close() }
    $powerpoint.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($powerpoint) | Out-Null
}
