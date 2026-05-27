$OneNote = New-Object -ComObject OneNote.Application
[xml]$Hierarchy = ""
$OneNote.GetHierarchy("", 4, [ref]$Hierarchy)

$ns = @{one="http://schemas.microsoft.com/office/onenote/2013/onenote"}

$pages = Select-Xml -Xml $Hierarchy -XPath "//one:Page" -Namespace $ns

$output = @()

foreach ($page in $pages) {
    $pageId = $page.Node.ID
    $pageName = $page.Node.name
    $sectionName = $page.Node.ParentNode.name
    
    $notebookNode = $page.Node.ParentNode.ParentNode
    if ($notebookNode.LocalName -eq "SectionGroup") {
        $notebookNode = $notebookNode.ParentNode
    }
    $notebookName = $notebookNode.name

    # Skip recycle bin
    if ($page.Node.isInRecycleBin -eq "true") { continue }

    [xml]$pageContent = ""
    try {
        $OneNote.GetPageContent($pageId, [ref]$pageContent, 0)
        # We need to extract CDATA or text from one:T nodes
        $textNodes = Select-Xml -Xml $pageContent -XPath "//one:T" -Namespace $ns
        $text = ($textNodes | ForEach-Object { 
            # In OneNote XML, text is usually in CDATA section inside one:T
            if ($_.Node.HasChildNodes) {
                $_.Node.InnerText -replace "<[^>]+>","" # Strip embedded HTML like <span...>
            }
        }) -join "`n"
        
        if (![string]::IsNullOrWhiteSpace($text)) {
            $output += "Notebook: $notebookName | Section: $sectionName | Page: $pageName"
            $output += "--------------------------------------------------------"
            $output += $text
            $output += "`n"
        }
    } catch {}
}

$output | Out-File -FilePath "onenote_content.txt" -Encoding UTF8
