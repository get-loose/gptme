# Error: [Errno 21] Is a directory

This error occurs when a file operation is attempted on a directory path instead of a file path.

Common causes:
- Using a directory path where a file path is expected.
- Incorrect command usage that treats a directory as a file.
- Misconfiguration in scripts or tools that handle file paths.

In the context of patching or writing files:
- Ensure the target path is a file, not a directory.
- Use absolute paths to avoid ambiguity.
- When patching, specify the exact file path.
- If patching fails repeatedly, consider overwriting the file directly.

This document was created to record the occurrence of this error during patch attempts in the gptme project.
