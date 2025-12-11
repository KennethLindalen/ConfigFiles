# Build project to only show errors
function dbe {
    dotnet build --consoleLoggerParameters:ErrorsOnly
}

# Build project to only show warnings
function dbw {
    dotnet build --verbosity minimal 2>&1 | Select-String -Pattern "warning"
}

# Create new database migration
function dbm {
    param (
        [Parameter(Mandatory=$true)]
        [string]$migrationName
    )
    dotnet ef migrations add $migrationName
}

# Update database dotnet ef database update 
function dbu {
     dotnet ef database update
}

function dbscaffold {
    param (
        [Parameter(Mandatory = $true, Position = 0)]
        [string]$connectionString,

        [Parameter(Mandatory = $true, Position = 1)]
        [string]$context,

        [Parameter(Mandatory = $false, Position = 2)]
        [string[]]$schemas
    )

    # Basis-argumenter til dotnet ef
    $args = @(
        "ef", "dbcontext", "scaffold",
        $connectionString,
        "Microsoft.EntityFrameworkCore.SqlServer",
        "--context", $context,
        "--output-dir", "Data/Entities"
    )

    # Hvis schema(er) er angitt, legg på --schema for hver
    if ($schemas -and $schemas.Length -gt 0) {

        # Støtt evt. 'MDW,ODS,SRC' som én streng
        if ($schemas.Count -eq 1 -and $schemas[0] -like "*,*") {
            $schemas = $schemas[0].Split(",") | ForEach-Object { $_.Trim() }
        }

        foreach ($schema in $schemas) {
            if (-not [string]::IsNullOrWhiteSpace($schema)) {
                $args += @("--schema", $schema)
            }
        }
    }

    dotnet @args
}

# Show help for all database commands
function dbhelp {
    Write-Host "Available Commands:"
    Write-Host "-------------------"
    Write-Host "dbe       : Builds the project showing only errors"
    Write-Host "            dotnet build --consoleLoggerParameters:ErrorsOnly"
    Write-Host ""
    Write-Host "dbw       : Builds the project and prints only warnings"
    Write-Host "            dotnet build --verbosity minimal 2>&1 | Select-String -Pattern 'warning'"
    Write-Host ""
    Write-Host "dbm       : Creates a new database migration"
    Write-Host "            Usage: dbm <migrationName>"
    Write-Host "            dotnet ef migrations add <migrationName>"
    Write-Host ""
    Write-Host "lpt       : Lists NuGet packages (including transitive dependencies)"
    Write-Host "            dotnet list package --include-transitive"
    Write-Host ""
    Write-Host "dbu       : Updates the database using the default connection"
    Write-Host "            dotnet ef database update"
    Write-Host ""
    Write-Host "dbussf    : Updates the database using the NSSF dev SQL connection string"
    Write-Host "            dotnet ef database update --connection <connection-string>"
    Write-Host ""
    Write-Host "dbscaffold: Scaffolds DbContext and entity classes using EF Core"
    Write-Host "            Usage:"
    Write-Host "              dbscaffold \"<connectionString>\" <ContextName> MDW ODS SRC"
    Write-Host "              dbscaffold \"<connectionString>\" <ContextName> \"MDW,ODS,SRC\""
    Write-Host ""
    Write-Host "            Example:"
    Write-Host "              dbscaffold \"Server=.;Database=MyDb;Trusted_Connection=True\" MyDbContext MDW ODS"
    Write-Host ""
    Write-Host "            This runs:"
    Write-Host "              dotnet ef dbcontext scaffold <connectionString> Microsoft.EntityFrameworkCore.SqlServer"
    Write-Host "                 --context <ContextName>"
    Write-Host "                 --output-dir Data/Entities"
    Write-Host "                 --schema <schema> ..."
}

