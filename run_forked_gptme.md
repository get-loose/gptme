# Running gptme from a Local Fork with Poetry

This guide explains how to run the `gptme` tool from your local fork of the repository using Poetry, ensuring you use the local code and dependencies instead of a globally installed version.

## Prerequisites

- You have cloned the `gptme` repository locally.
- You have Poetry installed and have created a virtual environment for the project.
- You have activated the Poetry environment or will use `poetry run` to execute commands.

## Steps

1. **Navigate to your local fork directory**

   ```bash
   cd /path/to/your/gptme/fork
   ```

2. **Install dependencies and create the virtual environment**

   If you haven't already done this, run:

   ```bash
   poetry install
   ```

   This will install all required dependencies in an isolated virtual environment.

3. **Activate the Poetry virtual environment (optional)**

   You can activate the Poetry shell to work inside the environment:

   ```bash
   poetry shell
   ```

   After this, running `gptme` will use the local fork's environment.

4. **Run gptme using Poetry**

   If you prefer not to activate the shell, you can run `gptme` commands prefixed with `poetry run`:

   ```bash
   poetry run gptme [OPTIONS] [PROMPTS]...
   ```

   This ensures the command runs inside the Poetry virtual environment.

5. **Verify the gptme executable path**

   To confirm you are running the local fork's `gptme`, check the path:

   ```bash
   which gptme
   ```

   - If inside the Poetry shell, this should point to the virtual environment's `bin/gptme`.
   - If outside, use `poetry run which gptme` to check.

6. **Check Playwright and gptme versions**

   To check the installed Playwright version in the Poetry environment:

   ```bash
   poetry run pip show playwright
   ```

   To check the installed gptme version:

   ```bash
   poetry run pip show gptme
   ```

## Notes

- Running `gptme` directly from the shell without activating the Poetry environment or using `poetry run` will likely invoke the globally installed version (e.g., via pipx).
- Using the Poetry environment ensures you are testing and running your local fork with the correct dependencies and code.

---

This setup helps avoid version mismatches and ensures your changes in the fork are used when running `gptme`.
