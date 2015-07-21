$source = $octgn_coc_source + "\o8g"
$definitionxml = $source + "\definition.xml"
$o8build = $o8build_location + "\o8build.exe"

$version = "version"

function obuild
{
    $loc = Get-Location
    Set-Location $source
    
	[xml]$def = (Get-Content $definitionxml) 
    
    $version_number = [version]($def.game.version)
       
    $prev_version = "{0}.{1}.{2}.{3}" -f $version_number.Major, $version_number.Minor, $version_number.Build, $version_number.Revision
    $new_version = "{0}.{1}.{2}.{3}" -f $version_number.Major, $version_number.Minor, $version_number.Build, ($version_number.Revision + 1)
    
    echo ("Changing version number from {0} to {1}" -f $prev_version, $new_version)

    $def.game.version = $new_version
    $def.Save($definitionxml)
    
    
    & $o8build -i -d=($source)
    
    Set-Location $loc
}

function ob
{
    obuild
}