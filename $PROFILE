# Build project to only show errors
function db {
    dotnet build --verbosity quiet
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

# Show help for all database commands
function dbhelp {
    Write-Host "Available Commands:"
    Write-Host "-------------------"
    Write-Host "db   : Builds the project showing only errors (dotnet build --verbosity quiet)"
    Write-Host "dbw  : Builds the project showing only warnings (dotnet build --verbosity minimal 2>&1 | Select-String -Pattern 'warning')"
    Write-Host "dbm  : Creates a new database migration. Usage: dbm <migrationName> (dotnet ef migrations add <migrationName>)"
    Write-Host "dbu  : Updates the database (dotnet ef database update)"
}
