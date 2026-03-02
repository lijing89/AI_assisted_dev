---
name: timer-stream-dispose
description: 修复 Dart/Flutter 项目中 Timer 与 StreamSubscription 的内存泄漏，确保在组件/控制器销毁时统一取消并释放。在用户或代码审查要求「修复 Timer/StreamSubscription 泄漏」「释放 Timer/订阅」「dispose/cancel 定时器或流」时使用。
---

# Timer / StreamSubscription 释放规范

## 原则

- 每个 **Timer**（含 `Timer.periodic`、`Timer()`）必须在不再需要时调用 **`.cancel()`**。
- 每个 **StreamSubscription**（来自 `stream.listen(...)`）必须在不再需要时调用 **`.cancel()`**。
- 释放必须在对应的生命周期里执行，避免对象已销毁但定时器/订阅仍在运行导致泄漏或崩溃。

## 工作流

1. **定位**：在目标目录（如 `lib/`）搜索 `Timer\.`, `Timer.periodic`, `StreamSubscription`, `.listen(`。
2. **对每个使用点**：
   - 若为 **StatefulWidget**：将 Timer/StreamSubscription 存为 State 的成员（如 `Timer? _timer;`），在 `dispose()` 中 `_timer?.cancel(); _timer = null;` 或 `_sub?.cancel(); _sub = null;`。
   - 若为 **GetxController / 其他 Controller**：存为成员，在 `onClose()`（或等价析构）里 cancel 并置 null。
   - 若为 **静态/全局**：确保在应用或模块关闭/登出时有一次性的 cancel 逻辑，避免常驻进程泄漏。
3. **listen 返回值**：`stream.listen(...)` 必须把返回值赋给变量并在 dispose/onClose 里 cancel，不能忽略返回值。

## 代码模式

### StatefulWidget

```dart
class _MyState extends State<MyPage> {
  Timer? _timer;
  StreamSubscription? _sub;

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {});
    _sub = someStream.listen((_) {});
  }

  @override
  void dispose() {
    _timer?.cancel();
    _timer = null;
    _sub?.cancel();
    _sub = null;
    super.dispose();
  }
}
```

### GetxController

```dart
class MyController extends GetxController {
  Timer? _timer;
  StreamSubscription? _sub;

  @override
  void onClose() {
    _timer?.cancel();
    _timer = null;
    _sub?.cancel();
    _sub = null;
    super.onClose();
  }
}
```

### 局部 Subscription 需在适当时机 cancel

若在异步回调里 `stream.listen(...)` 且不存成成员，需在完成或错误路径上调用返回的 `StreamSubscription.cancel()`，或改为存成成员并在 dispose/onClose 中统一 cancel。

## 检查清单

- [ ] 所有 `Timer`/`Timer.periodic` 都有对应的 `cancel()` 调用。
- [ ] 所有 `stream.listen(...)` 的返回值都被保存并在生命周期内 `cancel()`。
- [ ] 静态/全局 Timer 或 Subscription 在模块或应用退出/登出时有释放逻辑。
- [ ] `dispose`/`onClose` 中先 cancel 再置 null，且不重复 cancel（可先判 null 或 `isActive`）。
