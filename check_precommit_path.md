# Ensuring pre-commit is Available in Your Shell PATH

When using pre-commit installed inside a pipx editable environment (such as for gptme), you may encounter situations where the `pre-commit` command is not found, even after activating the virtual environment.

This document explains why this happens and how to ensure `pre-commit` is available in your shell PATH for convenient use.

---

## Why `pre-commit` May Not Be Found

- The pipx editable environment creates a virtual environment in a directory like:
