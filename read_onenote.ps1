$OneNote = New-Object -ComObject OneNote.Application
$xml = ""
$OneNote.GetHierarchy("", 4, [ref]$xml)
$xml | Out-File -FilePath "onenote_hierarchy.xml"
