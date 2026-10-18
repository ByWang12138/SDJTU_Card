$ErrorActionPreference='Stop'
try {
    if ($args.Count -gt 0) { throw 'This launcher does not accept generation arguments.' }
    $recordPath=Join-Path $PSScriptRoot 'config\INSTALLATION.local.md'
    if (-not (Test-Path -LiteralPath $recordPath -PathType Leaf)) { throw 'Missing config/INSTALLATION.local.md. Read MANUAL_SETUP.md and complete the Markdown record manually.' }
    $record=Get-Content -LiteralPath $recordPath -Raw -Encoding UTF8
    $fields=@{}
    $fieldPattern='(?m)^- `([a-z][a-z0-9_]*)`: `([^`\r\n]*)`[ \t]*\r?$'
    foreach($match in [regex]::Matches($record,$fieldPattern)) {
        $key=$match.Groups[1].Value
        if ($fields.ContainsKey($key)) { throw "Duplicate Markdown field: $key" }
        $fields[$key]=$match.Groups[2].Value.Trim()
    }
    $python=$fields['python_executable']
    if ([string]::IsNullOrWhiteSpace($python) -or $python -eq 'REQUIRED' -or -not [IO.Path]::IsPathRooted($python)) { throw 'Manually enter an absolute python_executable path in the Markdown record.' }
    if (-not (Test-Path -LiteralPath $python -PathType Leaf)) { throw 'Configured Python executable not found.' }
    $expected=$fields['python_executable_sha256']
    $hasher=[Security.Cryptography.SHA256]::Create()
    try { $actualHash=([BitConverter]::ToString($hasher.ComputeHash([IO.File]::ReadAllBytes($python)))).Replace('-','') }
    finally { $hasher.Dispose() }
    if ($expected -notmatch '^[0-9a-fA-F]{64}$' -or $actualHash -ine $expected) { throw 'The Python executable hash does not match the manually completed record.' }
    if ($fields['schema_version'] -ne '2') { throw 'The Markdown schema_version must be 2.' }
    $installation=$fields['installation_root']
    if ([string]::IsNullOrWhiteSpace($installation) -or -not [IO.Path]::IsPathRooted($installation) -or [IO.Path]::GetFullPath($installation).TrimEnd('\') -ine [IO.Path]::GetFullPath($PSScriptRoot).TrimEnd('\')) { throw 'Manually set installation_root to the absolute path of this installation.' }
    & $python (Join-Path $PSScriptRoot 'app.py')
    exit $LASTEXITCODE
} catch {
    Add-Type -AssemblyName System.Windows.Forms
    [Windows.Forms.MessageBox]::Show($_.Exception.Message,'Manual Markdown Configuration Required','OK','Error')|Out-Null
    exit 1
}
