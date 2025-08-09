#!/bin/bash

# Script to run a specific test in the Life360 project
# Usage: ./scripts/runTest.sh <test_target> [--repetitions|-r <count>]
# Example: ./scripts/runTest.sh Life360Tests/AddATileInteractorTests
# Example: ./scripts/runTest.sh Life360Tests/AddATileInteractorTests --repetitions 1000
# Example: ./scripts/runTest.sh Life360Tests/AddATileInteractorTests -r 5

# Default values
TEST_TARGET=""
REPETITIONS=1

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --repetitions|-r)
            REPETITIONS="$2"
            shift 2
            ;;
        *)
            if [ -z "$TEST_TARGET" ]; then
                TEST_TARGET="$1"
            else
                echo "Error: Unexpected argument: $1"
                echo "Usage: $0 <test_target> [--repetitions|-r <count>]"
                echo "Example: $0 Life360Tests/AddATileInteractorTests --repetitions 1000"
                exit 1
            fi
            shift
            ;;
    esac
done

# Check if test target argument is provided
if [ -z "$TEST_TARGET" ]; then
    echo "Error: No test target provided"
    echo "Usage: $0 <test_target> [--repetitions|-r <count>]"
    echo "Example: $0 Life360Tests/AddATileInteractorTests"
    echo "Example: $0 Life360Tests/AddATileInteractorTests --repetitions 1000"
    echo "Example: $0 Life360Tests/AddATileInteractorTests -r 5"
    exit 1
fi

fixlint () {
  git diff --name-only | grep '\.swift$' | while read -r filename; do
    if [ -f "$filename" ]; then
      echo "Linting $filename"
      swiftlint lint "$filename" --fix
    fi
  done
}


echo "Running test: $TEST_TARGET"
if [ $REPETITIONS -gt 1 ]; then
    echo "Repetitions: $REPETITIONS"
fi
echo "=============================="

# Run the test with the same configuration as provided
fixlint && xcodebuild test \
    -workspace Life360.xcworkspace \
    -scheme Life360 \
    -destination "platform=iOS Simulator,OS=18.4,name=iPhone 16e,arch=arm64" \
    -only-testing:"$TEST_TARGET" \
    -resultBundlePath "/tmp/test_results_$(date +%Y%m%d_%H%M%S).xcresult" \
    | xcbeautify -qq --is-ci \
    | grep -v "module 'ExperimentController' in AST file"

# Capture the exit code to pass through
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "✅ Test passed: $TEST_TARGET"
else
    echo "❌ Test failed: $TEST_TARGET"
fi

exit $exit_code 
