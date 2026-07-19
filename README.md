
# WizLib

⚠️ DISCLAIMER: This is a hobby/personal project. Not a commercial product. Not for production use.

## Build configurable CLI tools easily in Python (a framework)

**NOTE** Usage documentation lives in the `docs/` directory of the repo, published at https://wizlib.steamwiz.io.

## Development setup

Requires Python 3.11 or higher. Uses [Dyngle](https://pypi.org/project/dyngle/) for administration (installed separately)

- `dyngle run init` - Create the virtual environment and install poetry
- `dyngle run dependencies` - Install the required packages using poetry
- `dyngle run test` - Run tests and report coverage (same as CI/CD)
- `dyngle run style` - Run style checks (same as CI/CD)
- `dyngle run build` - Create a test build

GitHub Actions performs the entire build/test/release cycle for production.
