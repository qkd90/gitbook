Go 中任意 goroutine 出现未被 `recover` 捕获的 `panic`，通常都会导致整个进程退出，不只是当前 goroutine。

服务是否“重启”，取决于部署环境：

- Kubernetes：Pod 内进程退出后，通常会按 `restartPolicy` 重启容器。
- systemd / Supervisor / Docker：配置了自动重启策略就会重启。
- 直接运行 Go 程序：进程退出，不会自行重启。

建议在 goroutine、HTTP 中间件、消息消费者等入口处统一捕获：

```
func safeGo(fn func()) {
	go func() {
		defer func() {
			if err := recover(); err != nil {
				log.Printf("panic recovered: %v\n%s", err, debug.Stack())
			}
		}()
		fn()
	}()
}
```

需要注意：

1. `recover()` 必须在发生 `panic` 的同一个 goroutine 中调用。
2. 只能在 `defer` 中有效执行。
3. 捕获后必须记录完整堆栈，否则问题会被隐藏。
4. 不建议所有 `panic` 都强行恢复；如果内部状态已经不可信，让进程退出并由 Kubernetes 等重新拉起可能更安全。
5. `fatal error`、内存耗尽、`SIGKILL` 等情况通常不能依靠 `recover` 处理。

因此排查“服务重启”时，应先看重启前日志中是否存在：

```
panic:
goroutine ...
```

以及 Kubernetes 中的退出码、`Restart Count` 和 `Last State`。常见的 panic 来源包括空指针、数组越界、并发写 Map、类型断言失败，以及关闭已关闭的 channel。