#!/bin/bash
set -euo pipefail

# Configuration
SRC="../sbox-common"
DEST="../sboxmgr/src/sboxmgr"
LOG_FILE="sync.log"
VERSION_FILE=".schema_version"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

# Check if source directory exists
if [[ ! -d "$SRC" ]]; then
    error "Source directory $SRC does not exist"
fi

# Check if destination directory exists
if [[ ! -d "$DEST" ]]; then
    warn "Destination directory $DEST does not exist, creating..."
    mkdir -p "$DEST"
fi

log "Starting schema synchronization from $SRC to $DEST"

# Create destination directories
mkdir -p "$DEST/schemas" "$DEST/protocols"

# Function to get file hash
get_file_hash() {
    sha256sum "$1" | cut -d' ' -f1
}

# Function to check if file changed
file_changed() {
    local src_file="$1"
    local dest_file="$2"
    
    if [[ ! -f "$dest_file" ]]; then
        return 0  # File doesn't exist, consider it changed
    fi
    
    local src_hash=$(get_file_hash "$src_file")
    local dest_hash=$(get_file_hash "$dest_file")
    
    [[ "$src_hash" != "$dest_hash" ]]
}

# Sync schemas
log "Syncing schemas..."
SCHEMA_CHANGES=0
for schema in "$SRC"/schemas/*.json; do
    if [[ -f "$schema" ]]; then
        filename=$(basename "$schema")
        dest_file="$DEST/schemas/$filename"
        
        if file_changed "$schema" "$dest_file"; then
            cp -v "$schema" "$dest_file"
            log "Updated schema: $filename"
            ((SCHEMA_CHANGES++))
        else
            log "Schema unchanged: $filename"
        fi
    fi
done

# Sync protocols
log "Syncing protocols..."
PROTOCOL_CHANGES=0
for protocol in "$SRC"/protocols/*.json; do
    if [[ -f "$protocol" ]]; then
        filename=$(basename "$protocol")
        dest_file="$DEST/protocols/$filename"
        
        if file_changed "$protocol" "$dest_file"; then
            cp -v "$protocol" "$dest_file"
            log "Updated protocol: $filename"
            ((PROTOCOL_CHANGES++))
        else
            log "Protocol unchanged: $filename"
        fi
    fi
done

# Update version file
TOTAL_CHANGES=$((SCHEMA_CHANGES + PROTOCOL_CHANGES))
if [[ $TOTAL_CHANGES -gt 0 ]]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $TOTAL_CHANGES files updated" > "$VERSION_FILE"
    log "Synchronization completed: $TOTAL_CHANGES files updated"
else
    log "Synchronization completed: No changes detected"
fi

# Validate JSON files
log "Validating JSON files..."
for json_file in "$DEST"/schemas/*.json "$DEST"/protocols/*.json; do
    if [[ -f "$json_file" ]]; then
        if ! python3 -m json.tool "$json_file" > /dev/null 2>&1; then
            error "Invalid JSON in $json_file"
        fi
    fi
done

log "JSON validation passed"

# Show git status if in git repository
if git rev-parse --git-dir > /dev/null 2>&1; then
    log "Git status:"
    git status --porcelain "$DEST" || true
fi

log "Schema synchronization completed successfully" 