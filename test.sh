#!/usr/bin/env bash

# test.sh - Test runner for .agents project
# Runs the full test suite with progress display

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                   🧪 .AGENTS TEST SUITE 🧪                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo -e "${RED}❌ Poetry is not installed. Please install it first.${NC}"
    echo -e "${YELLOW}Run: curl -sSL https://install.python-poetry.org | python3 -${NC}"
    exit 1
fi

echo -e "${BLUE}📦 Installing dependencies...${NC}"
poetry install --no-interaction --quiet

echo ""
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🏃 Running Test Suite${NC}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Function to run tests with a label
run_test_group() {
    local label=$1
    local test_path=$2
    local marker=$3
    
    echo -e "${CYAN}▶ ${label}${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if [ -n "$marker" ]; then
        poetry run pytest "$test_path" -m "$marker" -v --tb=short || {
            echo -e "${RED}❌ $label failed!${NC}"
            return 1
        }
    else
        poetry run pytest "$test_path" -v --tb=short || {
            echo -e "${RED}❌ $label failed!${NC}"
            return 1
        }
    fi
    
    echo -e "${GREEN}✓ $label passed!${NC}"
    echo ""
}

# Test execution flag
all_passed=true

# Run different test groups
run_test_group "Unit Tests" "tests/" "unit" || all_passed=false

echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}📊 Full Test Suite (with Coverage)${NC}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Run all tests with coverage
poetry run pytest tests/ \
    --cov=src \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    -v \
    --tb=short || all_passed=false

echo ""
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [ "$all_passed" = true ]; then
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              ✅ ALL TESTS PASSED SUCCESSFULLY! ✅            ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${CYAN}📈 Coverage report generated in htmlcov/index.html${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                  ❌ SOME TESTS FAILED ❌                     ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${YELLOW}Please review the errors above and fix the failing tests.${NC}"
    echo ""
    exit 1
fi
