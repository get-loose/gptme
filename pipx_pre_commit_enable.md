# Enabling pre-commit in the pipx editable environment for gptme

This document describes how to enable and configure pre-commit hooks when using the pipx editable installation of gptme. It also highlights common pitfalls and how to avoid them.

---

## Background

- You have gptme installed as an editable package via pipx.
- You want to use pre-commit hooks to automatically check and fix code before commits.
- Pre-commit must be installed and configured in the same environment where you run git commands that trigger the hooks.
- The pipx editable environment is separate from your poetry environment, so tools installed in poetry are not available in pipx and vice versa.

---

## Step-by-step instructions

### 1. Confirm your pipx editable install name

Run:

```bash
pipx list
```

Look for the package name of your editable gptme install (likely `gptme`).

---

### 2. Inject pre-commit into the pipx editable environment

Run:

```bash
pipx inject gptme pre-commit
```

This installs `pre-commit` into the pipx environment where gptme is installed.

---

### 3. Install the git hooks using pre-commit

From your project root (where `.git` is), run:

```bash
pipx run --spec gptme pre-commit install
```

or if you want to be explicit:

```bash
pipx run gptme pre-commit install
```

This sets up the git hooks to use the pre-commit installed in the pipx environment.

---

### 4. Verify pre-commit works

Run:

```bash
pipx run gptme pre-commit run --all-files
```

This runs all pre-commit hooks on all files and shows any issues.

---

## Common pitfalls and notes

- **Environment mismatch:** Running pre-commit from poetry environment while hooks are installed from pipx environment (or vice versa) can cause confusion. Always run pre-commit commands from the same environment where hooks are installed.

- **Hooks run in isolated environments:** pre-commit creates isolated virtual environments for each hook based on `.pre-commit-config.yaml`. This means hooks are mostly independent of your main environment, but the pre-commit tool itself must be installed in the environment running the git hooks.

- **Editable install path:** If you reinstall or update the pipx editable install, you may need to re-inject pre-commit or reinstall hooks.

- **File changes:** pre-commit hooks modify files on disk. These changes are visible regardless of environment, so no risk of environment-specific file states.

- **Running git commands:** When committing, git will invoke pre-commit hooks from the installed environment. Make sure your git commands run in a shell where the pipx environment is accessible (usually the default shell).

---

## Summary

- Use `pipx inject` to add pre-commit to your pipx editable environment.
- Use `pipx run` to run pre-commit commands from that environment.
- Install git hooks with `pre-commit install` from the pipx environment.
- Avoid mixing environments when running pre-commit commands.

---

If you want, you can open a shell inside the pipx environment for interactive use:

```bash
pipx run --spec gptme bash
```

Then run pre-commit commands normally inside that shell.

---

This setup ensures your pre-commit hooks work seamlessly with your pipx editable gptme install.
