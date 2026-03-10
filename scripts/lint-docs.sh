#!/usr/bin/env bash
# =============================================================================
# Doc Standard Linter
# Validates markdown files against the documentation standard defined in
# design-bible/PROJECT_CONVENTIONS.md Section 9.
#
# Usage:
#   ./scripts/lint-docs.sh                    # Lint all .md files in design-bible/
#   ./scripts/lint-docs.sh design-bible/      # Lint specific directory
#   ./scripts/lint-docs.sh path/to/file.md    # Lint single file
#
# Exit codes:
#   0 = all files compliant
#   1 = one or more files non-compliant
#
# Required header fields: Doc ID, Name, Purpose, Owner, Status, Author, Version,
#                         Created, Last Modified
# Required footer: Modification History table with at least one row
# Version consistency: header Version must match latest Modification History row
# =============================================================================

set -o pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BOLD='\033[1m'
NC='\033[0m'

ERRORS=0
FILES_CHECKED=0
FILES_PASSED=0
FILES_FAILED=0

# Determine what to lint
TARGET="${1:-design-bible/}"

# Collect files
if [[ -f "$TARGET" ]]; then
    FILES=("$TARGET")
elif [[ -d "$TARGET" ]]; then
    FILES=()
    while IFS= read -r -d '' f; do
        FILES+=("$f")
    done < <(find "$TARGET" -name "*.md" -type f -print0 | sort -z)
else
    echo -e "${RED}Error: $TARGET is not a file or directory${NC}"
    exit 1
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
    echo -e "${YELLOW}No .md files found in $TARGET${NC}"
    exit 0
fi

# Exclude agent-comm/ — coordination data files, not design documents (see §10.1)
FILTERED=()
for f in "${FILES[@]}"; do
    if [[ "$f" != *"/agent-comm/"* ]]; then
        FILTERED+=("$f")
    fi
done
FILES=("${FILTERED[@]}")

# ---------------------------------------------------------------------------
# Validation functions
# ---------------------------------------------------------------------------

# Extract the header region (first 25 lines) to avoid false matches in body content
get_header() {
    head -25 "$1"
}

check_field() {
    local file="$1"
    local field="$2"

    if ! get_header "$file" | grep -q "\*\*${field}\*\*"; then
        echo -e "  ${RED}MISSING${NC}: **${field}** not found in header"
        return 1
    fi
    return 0
}

check_field_value() {
    local file="$1"
    local field="$2"

    # Extract the value from the third column of the markdown table row
    local value
    value=$(get_header "$file" | grep "\*\*${field}\*\*" | head -1 | awk -F'|' '{print $3}' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

    if [[ -z "$value" ]]; then
        echo -e "  ${RED}EMPTY${NC}: **${field}** has no value"
        return 1
    fi
    return 0
}

lint_file() {
    local file="$1"
    local file_errors=0

    FILES_CHECKED=$((FILES_CHECKED + 1))

    echo -e "\n${BOLD}Checking:${NC} $file"

    # --- Required header fields ---
    local required_fields=("Doc ID" "Name" "Purpose" "Owner" "Status" "Author" "Version" "Created" "Last Modified")

    for field in "${required_fields[@]}"; do
        if ! check_field "$file" "$field"; then
            file_errors=$((file_errors + 1))
        else
            if ! check_field_value "$file" "$field"; then
                file_errors=$((file_errors + 1))
            fi
        fi
    done

    # --- Doc ID format check ---
    local doc_id
    doc_id=$(get_header "$file" | grep "\*\*Doc ID\*\*" | grep -oE 'DB-[A-Z][0-9]{2}-[0-9]{3}')
    if [[ -n "$doc_id" ]]; then
        # Valid format
        :
    elif get_header "$file" | grep -q "\*\*Doc ID\*\*"; then
        echo -e "  ${YELLOW}WARNING${NC}: Doc ID does not match DB-VNN-SSS format"
    fi

    # --- Status value check (header only, not body) ---
    local status_value
    status_value=$(get_header "$file" | grep "\*\*Status\*\*" | head -1)
    if [[ -n "$status_value" ]]; then
        if ! echo "$status_value" | grep -qE '(draft|active|deprecated|superseded)'; then
            echo -e "  ${RED}INVALID${NC}: Status must be one of: draft, active, deprecated, superseded"
            file_errors=$((file_errors + 1))
        fi
    fi

    # --- Modification History table ---
    if ! grep -q "## Modification History" "$file"; then
        echo -e "  ${RED}MISSING${NC}: Modification History section not found"
        file_errors=$((file_errors + 1))
    else
        # Check for at least one data row (starts with | v)
        if ! sed -n '/## Modification History/,$ p' "$file" | grep -qE '^\| v[0-9]'; then
            echo -e "  ${RED}EMPTY${NC}: Modification History has no entries"
            file_errors=$((file_errors + 1))
        fi
    fi

    # --- Version consistency check ---
    local header_version
    header_version=$(get_header "$file" | grep "\*\*Version\*\*" | grep -oE 'v[0-9]+' | head -1)

    local latest_history_version
    latest_history_version=$(sed -n '/## Modification History/,$ p' "$file" | grep -oE '^\| v[0-9]+' | tail -1 | grep -oE 'v[0-9]+')

    if [[ -n "$header_version" && -n "$latest_history_version" ]]; then
        if [[ "$header_version" != "$latest_history_version" ]]; then
            echo -e "  ${RED}MISMATCH${NC}: Header version ($header_version) != latest history version ($latest_history_version)"
            file_errors=$((file_errors + 1))
        fi
    fi

    # --- Superseded-by check: if status is superseded, Superseded by must not be N/A ---
    # Only check if the HEADER status field contains 'superseded' (not body text)
    if echo "$status_value" | grep -qw "superseded"; then
        local superseded_by
        superseded_by=$(get_header "$file" | grep "\*\*Superseded by\*\*")
        if echo "$superseded_by" | grep -q "N/A"; then
            echo -e "  ${RED}INVALID${NC}: Status is 'superseded' but 'Superseded by' is N/A"
            file_errors=$((file_errors + 1))
        fi
    fi

    # --- Result ---
    if [[ $file_errors -eq 0 ]]; then
        echo -e "  ${GREEN}PASS${NC}"
        FILES_PASSED=$((FILES_PASSED + 1))
    else
        echo -e "  ${RED}FAIL${NC} ($file_errors issue(s))"
        FILES_FAILED=$((FILES_FAILED + 1))
        ERRORS=$((ERRORS + file_errors))
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

echo -e "${BOLD}=== Doc Standard Linter ===${NC}"
echo -e "Standard: design-bible/PROJECT_CONVENTIONS.md Section 9"
echo -e "Target: $TARGET"

for file in "${FILES[@]}"; do
    lint_file "$file"
done

echo -e "\n${BOLD}=== Summary ===${NC}"
echo -e "Files checked: $FILES_CHECKED"
echo -e "Passed: ${GREEN}$FILES_PASSED${NC}"
echo -e "Failed: ${RED}$FILES_FAILED${NC}"
echo -e "Total issues: $ERRORS"

if [[ $ERRORS -gt 0 ]]; then
    echo -e "\n${RED}${BOLD}LINT FAILED${NC} — $ERRORS issue(s) found"
    exit 1
else
    echo -e "\n${GREEN}${BOLD}ALL DOCS COMPLIANT${NC}"
    exit 0
fi
