name: test

on:
push:
workflow_dispatch:

jobs:
test:
runs-on: ubuntu-24.04

```
steps:
  - name: Checkout repo
    uses: actions/checkout@v4
    with:
      submodules: recursive

  - name: Install iverilog
    shell: bash
    run: |
      sudo apt-get update
      sudo apt-get install -y iverilog

  - name: Setup python
    uses: actions/setup-python@v5
    with:
      python-version: '3.11'

  - name: Install Python packages
    shell: bash
    run: |
      python -m pip install -r test/requirements.txt

  # Install Typst explicitly
  - name: Install Typst
    shell: bash
    run: |
      set -e
      export TYPST_INSTALL="$HOME/.typst"
      curl -fsSL https://install.typst.community/install.sh | sh
      echo "$HOME/.typst/bin" >> "$GITHUB_PATH"
      export PATH="$HOME/.typst/bin:$PATH"
      typst --version
      which typst

  # Run Verilog tests
  - name: Run tests
    shell: bash
    run: |
      cd test
      make clean
      make
      # Check test results
      ! grep failure results.xml

  # Publish test results
  - name: Test Summary
    uses: test-summary/action@v2.3
    with:
      paths: "test/results.xml"
    if: always()

  # Upload VCD and test results
  - name: upload vcd
    if: success() || failure()
    uses: actions/upload-artifact@v4
    with:
      name: test-vcd
      path: |
        test/tb.vcd
        test/results.xml
      if-no-files-found: warn

  # Confirm Typst is available before PDF generation
  - name: Verify Typst before PDF
    shell: bash
    run: |
      set -e
      which typst
      typst --version

  # Generate project datasheet PDF
  - name: Create PDF
    shell: bash
    run: |
      set -e
      ./tt/tt_tool.py --create-pdf

  # Upload generated PDF
  - name: Upload datasheet PDF
    if: success() || failure()
    uses: actions/upload-artifact@v4
    with:
      name: datasheet-pdf
      path: datasheet.pdf
      if-no-files-found: warn
```
