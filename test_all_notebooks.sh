#!/bin/bash
# Test all notebooks in the repository

set -e

echo "Testing all notebooks..."
echo "=================================================================================="

# Find all notebooks (excluding .executed ones)
notebooks=$(find . -name "*.ipynb" -not -name "*.executed.ipynb" | sort)

success_count=0
fail_count=0
failed_notebooks=""

for notebook in $notebooks; do
    echo ""
    echo "Testing: $notebook"

    output_file="/tmp/test_$(basename "$notebook")"

    if uv run jupyter nbconvert --to notebook --execute \
        --ExecutePreprocessor.timeout=120 \
        --ExecutePreprocessor.allow_errors=False \
        "$notebook" --output "$output_file" 2>&1 | grep -q "Writing"; then
        echo "  [OK] Success"
        ((success_count++))
    else
        echo "  [FAIL] Execution failed"
        ((fail_count++))
        failed_notebooks="$failed_notebooks\n  - $notebook"
    fi
done

echo ""
echo "=================================================================================="
echo "SUMMARY"
echo "=================================================================================="
echo "Total notebooks: $((success_count + fail_count))"
echo "Success: $success_count"
echo "Failed: $fail_count"

if [ $fail_count -gt 0 ]; then
    echo ""
    echo "Failed notebooks:"
    echo -e "$failed_notebooks"
    exit 1
fi

echo ""
echo "All notebooks executed successfully!"
exit 0
