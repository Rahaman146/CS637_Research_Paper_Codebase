$pptxPath = Convert-Path "presentation/CS637_Project_Presentation.pptx"
$pdfPath = [System.IO.Path]::ChangeExtension($pptxPath, ".pdf")
$rootPdfPath = Convert-Path "CS637_Project_Presentation.pptx"
$rootPdfPath = [System.IO.Path]::ChangeExtension($rootPdfPath, ".pdf")
$slidesDir = Join-Path (Split-Path $pptxPath) "slides"
if (-not (Test-Path $slidesDir)) { New-Item -ItemType Directory -Path $slidesDir | Out-Null }

$ppt = New-Object -ComObject PowerPoint.Application
# Open read-only, untitled=false, withwindow=false
$pres = $ppt.Presentations.Open($pptxPath, -1, 0, 0)
$pres.SaveAs($pdfPath, 32) # 32 = ppSaveAsPDF
Copy-Item $pdfPath $rootPdfPath

$i = 1
foreach ($slide in $pres.Slides) {
    $slideImg = Join-Path $slidesDir (("slide_{0:D2}.png") -f $i)
    $slide.Export($slideImg, "PNG", 1920, 1080)
    $i++
}
$pres.Close()
$ppt.Quit()
Write-Host "Exported PDF and" ($i - 1) "slides!"
