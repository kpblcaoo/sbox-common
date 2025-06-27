# INTEGRATION-02: Runtime

**Дата создания:** 2025-06-27  
**Статус:** 📋 **ПЛАНИРОВАНИЕ**  
**Приоритет:** ВЫСОКИЙ  
**Версия:** 1.0

## 🎯 ЦЕЛЬ ФАЗЫ

Реализовать runtime интеграцию между sboxmgr и sboxagent:
- Stdout Capture
- Configuration Synchronization
- Health Monitoring

## 📋 ЗАДАЧИ

### 2.1 Stdout Capture

#### 2.1.1 Process Management
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Реализовать запуск sboxmgr через sboxagent
- [ ] Перехват stdout/stderr процессов
- [ ] Управление жизненным циклом процессов
- [ ] Graceful shutdown процессов

**Реализация в sboxagent:**
```go
// internal/integration/process_manager.go
type ProcessManager struct {
    processes map[string]*Process
    mu        sync.RWMutex
}

type Process struct {
    ID       string
    Command  []string
    Process  *os.Process
    Stdout   io.ReadCloser
    Stderr   io.ReadCloser
    Status   ProcessStatus
    StartTime time.Time
}

func (pm *ProcessManager) StartProcess(id string, command []string) error {
    // Запуск процесса с перехватом stdout/stderr
    cmd := exec.Command(command[0], command[1:]...)
    stdout, err := cmd.StdoutPipe()
    if err != nil {
        return err
    }
    
    stderr, err := cmd.StderrPipe()
    if err != nil {
        return err
    }
    
    if err := cmd.Start(); err != nil {
        return err
    }
    
    process := &Process{
        ID:        id,
        Command:   command,
        Process:   cmd.Process,
        Stdout:    stdout,
        Stderr:    stderr,
        Status:    ProcessRunning,
        StartTime: time.Now(),
    }
    
    pm.mu.Lock()
    pm.processes[id] = process
    pm.mu.Unlock()
    
    // Запуск goroutines для чтения stdout/stderr
    go pm.readOutput(process, stdout, "stdout")
    go pm.readOutput(process, stderr, "stderr")
    
    return nil
}
```

#### 2.1.2 Log Parsing
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Парсинг структурированных логов sboxmgr
- [ ] Извлечение событий из логов
- [ ] Фильтрация и форматирование логов
- [ ] Сохранение логов в log aggregator

**Log Parser:**
```go
// internal/integration/log_parser.go
type LogParser struct {
    patterns map[string]*regexp.Regexp
}

type ParsedLog struct {
    Timestamp time.Time
    Level     string
    Message   string
    Fields    map[string]interface{}
    Event     *Event
}

func (lp *LogParser) ParseLine(line string) (*ParsedLog, error) {
    // Парсинг JSON логов sboxmgr
    var logEntry map[string]interface{}
    if err := json.Unmarshal([]byte(line), &logEntry); err != nil {
        return nil, err
    }
    
    parsed := &ParsedLog{
        Fields: logEntry,
    }
    
    // Извлечение timestamp
    if ts, ok := logEntry["timestamp"].(string); ok {
        if t, err := time.Parse(time.RFC3339, ts); err == nil {
            parsed.Timestamp = t
        }
    }
    
    // Извлечение level
    if level, ok := logEntry["level"].(string); ok {
        parsed.Level = level
    }
    
    // Извлечение message
    if msg, ok := logEntry["message"].(string); ok {
        parsed.Message = msg
    }
    
    // Генерация события
    parsed.Event = lp.generateEvent(parsed)
    
    return parsed, nil
}
```

#### 2.1.3 Event Generation
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Генерация событий из логов
- [ ] Маппинг логов на event types
- [ ] Добавление метаданных к событиям
- [ ] Отправка событий в event dispatcher

### 2.2 Configuration Synchronization

#### 2.2.1 Config Watcher
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Мониторинг изменений конфигураций
- [ ] Hot-reload конфигурации агента
- [ ] Валидация конфигураций при изменении
- [ ] Rollback при ошибках валидации

**Config Watcher:**
```go
// internal/integration/config_watcher.go
type ConfigWatcher struct {
    configPath string
    watcher    *fsnotify.Watcher
    reloadChan chan struct{}
    validator  *ConfigValidator
}

func (cw *ConfigWatcher) Start() error {
    watcher, err := fsnotify.NewWatcher()
    if err != nil {
        return err
    }
    
    cw.watcher = watcher
    
    // Добавление файлов для мониторинга
    if err := watcher.Add(cw.configPath); err != nil {
        return err
    }
    
    go cw.watchLoop()
    return nil
}

func (cw *ConfigWatcher) watchLoop() {
    for {
        select {
        case event := <-cw.watcher.Events:
            if event.Op&fsnotify.Write == fsnotify.Write {
                // Файл изменен, запуск reload
                cw.reloadChan <- struct{}{}
            }
        case err := <-cw.watcher.Errors:
            log.Printf("Config watcher error: %v", err)
        }
    }
}
```

#### 2.2.2 Config Validator
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Валидация конфигурации через JSON схемы
- [ ] Проверка зависимостей конфигурации
- [ ] Валидация путей и разрешений
- [ ] Генерация ошибок валидации

#### 2.2.3 Config Reloader
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Graceful reload конфигурации
- [ ] Сохранение состояния при reload
- [ ] Уведомление компонентов об изменениях
- [ ] Rollback при ошибках

### 2.3 Health Monitoring

#### 2.3.1 Process Health Checker
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Мониторинг состояния процессов sboxmgr
- [ ] Проверка доступности процессов
- [ ] Мониторинг ресурсов процессов
- [ ] Генерация health events

**Health Checker:**
```go
// internal/integration/health_checker.go
type ProcessHealthChecker struct {
    processManager *ProcessManager
    interval       time.Duration
    checks         map[string]HealthCheck
}

type HealthCheck struct {
    ProcessID string
    Type      string
    Status    HealthStatus
    LastCheck time.Time
    Error     error
}

func (phc *ProcessHealthChecker) Start() {
    ticker := time.NewTicker(phc.interval)
    defer ticker.Stop()
    
    for range ticker.C {
        phc.checkAllProcesses()
    }
}

func (phc *ProcessHealthChecker) checkAllProcesses() {
    phc.processManager.mu.RLock()
    processes := make(map[string]*Process)
    for id, process := range phc.processManager.processes {
        processes[id] = process
    }
    phc.processManager.mu.RUnlock()
    
    for id, process := range processes {
        status := phc.checkProcess(process)
        phc.updateHealthStatus(id, status)
    }
}

func (phc *ProcessHealthChecker) checkProcess(process *Process) HealthStatus {
    // Проверка, что процесс еще жив
    if process.Process == nil {
        return HealthStatusDead
    }
    
    // Проверка состояния процесса
    if err := process.Process.Signal(syscall.Signal(0)); err != nil {
        return HealthStatusDead
    }
    
    // Проверка ресурсов процесса
    if phc.checkProcessResources(process) {
        return HealthStatusHealthy
    }
    
    return HealthStatusDegraded
}
```

#### 2.3.2 Service Health Checker
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Проверка доступности HTTP API
- [ ] Проверка состояния базы данных
- [ ] Проверка сетевых соединений
- [ ] Мониторинг системных ресурсов

#### 2.3.3 Alerting System
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Генерация алертов при проблемах
- [ ] Настройка порогов для алертов
- [ ] Уведомления о критических событиях
- [ ] Escalation при длительных проблемах

## 🔧 ТЕХНИЧЕСКИЕ ДЕТАЛИ

### Структура файлов

```
sboxagent/internal/integration/
├── process_manager.go
├── log_parser.go
├── event_generator.go
├── config_watcher.go
├── config_validator.go
├── config_reloader.go
├── health_checker.go
├── alerting.go
└── types.go

sboxmgr/src/sboxmgr/
├── logging/
│   ├── structured_logger.py
│   └── event_emitter.py
└── config/
    ├── watcher.py
    └── validator.py
```

### Configuration Structure

```yaml
# /etc/sboxagent/integration.yaml
integration:
  sboxmgr:
    enabled: true
    command: ["sboxmgr", "update"]
    interval: "30m"
    timeout: "5m"
    stdout_capture: true
    working_dir: "/var/lib/sboxagent"
    environment:
      SBOXAGENT_INTEGRATION: "true"
      SBOXAGENT_LOG_LEVEL: "info"
    
    health_check:
      enabled: true
      interval: "60s"
      timeout: "10s"
      retries: 3
      
    logging:
      structured: true
      level: "info"
      format: "json"
      
    config_sync:
      enabled: true
      watch_paths:
        - "/etc/sboxmgr/config.yaml"
        - "/etc/sboxagent/config.yaml"
      reload_delay: "5s"
      validation: true
```

### Event Flow

```
sboxmgr process
    ↓ (stdout/stderr)
Process Manager
    ↓ (raw logs)
Log Parser
    ↓ (parsed logs)
Event Generator
    ↓ (events)
Event Dispatcher
    ↓ (events)
Log Aggregator
    ↓ (events)
Health Checker
```

## 🚀 ПЛАН РЕАЛИЗАЦИИ

### День 1-2: Process Management
- [ ] Реализовать ProcessManager
- [ ] Добавить stdout/stderr capture
- [ ] Реализовать graceful shutdown
- [ ] Добавить process lifecycle management

### День 3-4: Log Parsing
- [ ] Реализовать LogParser
- [ ] Добавить structured log parsing
- [ ] Реализовать event generation
- [ ] Интегрировать с event dispatcher

### День 5-6: Configuration Sync
- [ ] Реализовать ConfigWatcher
- [ ] Добавить ConfigValidator
- [ ] Реализовать ConfigReloader
- [ ] Добавить hot-reload functionality

### День 7: Health Monitoring
- [ ] Реализовать HealthChecker
- [ ] Добавить process health checks
- [ ] Реализовать alerting system
- [ ] Интегрировать с event system

## 🧪 ТЕСТИРОВАНИЕ

### Process Management Tests
- [ ] Process start/stop works correctly
- [ ] Stdout/stderr capture works
- [ ] Graceful shutdown works
- [ ] Process lifecycle management works

### Log Parsing Tests
- [ ] Structured log parsing works
- [ ] Event generation from logs works
- [ ] Log filtering works correctly
- [ ] Performance is acceptable

### Configuration Sync Tests
- [ ] Config file watching works
- [ ] Hot-reload works without downtime
- [ ] Config validation works
- [ ] Rollback on invalid config works

### Health Monitoring Tests
- [ ] Health checks work correctly
- [ ] Alerts are generated properly
- [ ] Process monitoring works
- [ ] Resource monitoring works

## 🔍 КРИТЕРИИ УСПЕХА

### Функциональные
- [ ] sboxagent перехватывает stdout sboxmgr
- [ ] Логи парсятся и структурируются
- [ ] Конфигурации синхронизируются
- [ ] Health monitoring работает

### Технические
- [ ] Process management стабилен
- [ ] Log parsing производителен
- [ ] Config sync надежен
- [ ] Health checks точны

### Качественные
- [ ] Нет memory leaks
- [ ] Graceful error handling
- [ ] Comprehensive logging
- [ ] Good performance

## 🔗 СВЯЗАННЫЕ ДОКУМЕНТЫ

- [Cross-Project Integration Plan](../integration-plan.md)
- [INTEGRATION-01: Foundation](phase-1-foundation.md)
- [INTEGRATION-03: Advanced](phase-3-advanced.md)

## 📝 ЗАМЕТКИ

### Приоритеты
1. **Process Management** - основа для интеграции
2. **Log Parsing** - основа для observability
3. **Health Monitoring** - основа для reliability

### Риски
- Performance impact от stdout capture
- Complexity process lifecycle management
- Resource usage при health checks

### Альтернативы
- Если stdout capture сложен, можно начать с file-based logging
- Если health checks тяжелы, можно уменьшить frequency

---

**Следующий шаг:** [INTEGRATION-03: Advanced](phase-3-advanced.md) 