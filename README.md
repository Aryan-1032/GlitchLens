
```markdown
## Running tests locally

### One browser test
`python -m pytest tests\browser\test_saleor_smoke.py -v`

### Smoke suite
`python -m pytest -m smoke -v`

### Regression suite
`python -m pytest -m regression -v`

### Negative suite
`python -m pytest -m negative -v`

### Visual suite
`python -m pytest -m visual -v`

### All tests
`python -m pytest -v`

### Headed browser mode
`$env:PW_HEADLESS="false"`

Reset:
`Remove-Item Env:PW_HEADLESS -ErrorAction SilentlyContinue`

### Playwright trace
`python -m playwright show-trace artifacts\playwright\test_product_listing_loads\trace.zip`