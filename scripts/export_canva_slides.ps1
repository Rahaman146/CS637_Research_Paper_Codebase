$pptxPath = Convert-Path "presentation/CS637_Project_Presentation_Canva_Style.pptx"
$pdfPath = [System.IO.Path]::ChangeExtension($pptxPath, ".pdf")
$rootPdfPath = Join-Path (Get-Location) "CS637_Project_Presentation_Canva_Style.pdf"
$slidesDir = Join-Path (Split-Path $pptxPath) "slides_canva"
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
Write-Host "Exported Canva PDF and" ($i - 1) "slides to $slidesDir"
