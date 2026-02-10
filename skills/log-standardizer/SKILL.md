---
name: "log-standardizer"
description: "Standardize logging in Dart files by replacing print/debugPrint/log with LogUtil methods. Invoke when user wants to clean up logs or enforce logging standards."
---

# Log Standardizer

This skill helps standardize logging across the project by replacing ad-hoc logging statements with the structured `LogUtil` class.

## Goal
Replace `print`, `debugPrint`, and `dart:developer`'s `log` with appropriate methods from `LogUtil` (`package:mm/util/log_util.dart`).

## Logic for Replacement

1.  **Target Selection**: 
    - Apply to the directory specified by the user. If no directory is specified, ask for one or default to the current active file's directory.
    - Scan all `.dart` files in the target directory.

2.  **Import Management**:
    - Ensure `import 'package:mm/util/log_util.dart';` is present in the file.
    - If missing, add it to the imports section.

3.  **Method Mapping**:
    Analyze the context of each logging statement to choose the correct `LogUtil` method:

    | Original | Context / Keyword | Replacement |
    | :--- | :--- | :--- |
    | `print(e)` / `debugPrint(e)` | Inside `catch` block or contains "error", "exception", "fail" | `LogUtil.error(e)` (pass error/stackTrace if available) |
    | `print(msg)` | Contains "warn", "warning", "alert" | `LogUtil.warning(msg)` |
    | `print(msg)` | Contains "info", "success", "start", "end" | `LogUtil.info(msg)` |
    | `debugPrint(msg)` | General debug info | `LogUtil.debug(msg)` |
    | `print(msg)` | General usage | `LogUtil.print(msg)` |
    | `log(msg)` | `dart:developer` log | `LogUtil.log(msg)` |

4.  **Special Handling**:
    - **Error Handling**: When replacing inside a `catch (e, s)` block, prefer `LogUtil.error(message, error: e, stackTrace: s)`.
    - **Tags**: If the original code used a custom tag (e.g., `log('msg', name: 'MyTag')`), preserve it using the `tag` parameter: `LogUtil.log('msg', name: 'MyTag')` or `LogUtil.info('msg', tag: 'MyTag')`.

## Execution Steps for the Agent

1.  **Identify Files**: List `.dart` files in the target directory.
2.  **Read & Analyze**: Read the content of the files.
3.  **Refactor**: Apply the replacements using `SearchReplace` or `Write` tools.
    - *Tip*: Use regex or AST-aware parsing (conceptually) to identify log statements.
    - *Tip*: Be careful not to replace `print` inside comments or strings.
4.  **Verify**: Check if `LogUtil` is imported and used correctly.

## Example

**Before:**
```dart
import 'package:flutter/foundation.dart';

void main() {
  print("App started");
  try {
    doSomething();
  } catch (e) {
    debugPrint("Failed: $e");
  }
}
```

**After:**
```dart
import 'package:flutter/foundation.dart';
import 'package:mm/util/log_util.dart';

void main() {
  LogUtil.info("App started");
  try {
    doSomething();
  } catch (e) {
    LogUtil.error("Failed", error: e);
  }
}
```
