# Parsing of .toml Configuration Files in gptme

## Overview

The gptme project uses several .toml configuration files for different purposes:

- **Global user config:** `~/.config/gptme/config.toml`
- **Project/workspace config:** `gptme.toml` in the workspace or `.github` directory
- **Chat config:** `config.toml` in the log directory or workspace

## Global Config Loading

- The global config path is defined as `~/.config/gptme/config.toml`.
- The function `_load_config_doc` loads the config file from the given path or creates a default one if it does not exist.
- The default config structure (`default_config`) includes sections like `[prompt]` and `[env]`.
- The global config is loaded by `load_user_config`, which is used as the default user config in the `Config` class.
- The global config should be loaded by default when `get_config()` is called, unless overridden.

## Workspace Config Override

- In the CLI main function, `set_config_from_workspace(workspace_path)` is called before `get_config()`.
- This likely loads or overrides the config with workspace-specific settings.
- The chat config is also loaded or created from the log directory and applied to the main config.

## Potential Reasons Global Config May Not Be Parsed

- The workspace config or chat config may override the global config.
- The global config file may not be at the expected path or may have permission issues.
- The config keys or structure may not match the expected schema.
- The config loading logic may prioritize workspace or chat configs over the global config.

## Next Steps

- Investigate the implementation of `set_config_from_workspace` to understand how workspace config affects the global config.
- Verify the precedence and merging strategy of global, workspace, and chat configs.
## Detailed Config Loading and Merging

- The global user config is loaded from `~/.config/gptme/config.toml` by `load_user_config` via `_load_config_doc`.
- The project config is loaded from `gptme.toml` in the workspace or `.github` directory by `get_project_config`.
- The chat config is loaded from `config.toml` in the log directory by `ChatConfig.from_logdir`.
- The `Config` class combines user, project, and chat configs.
- The `get_env` method in `Config` checks environment variables, then chat, project, and user env configs in that order.
- The CLI calls `set_config_from_workspace(workspace_path)` which sets the config to include the project config from the workspace.
- This means the global config is loaded but can be overridden or supplemented by workspace/project and chat configs.
- Your global config at `~/.config/gptme/config.toml` should be loaded unless overridden or if the workspace/project config or chat config has conflicting or missing keys.
- The config loading code creates the global config file with defaults if it does not exist.

### Recommendations if Global Config is Not Parsed

- Check the workspace/project config files for overrides.
- Check the chat config in the log directory.
- Verify the structure and keys in your global config file.
- Confirm the workspace path passed to CLI is as expected.
