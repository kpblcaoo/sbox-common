# INTEGRATION-03: Advanced

**Дата создания:** 2025-06-27  
**Статус:** 📋 **ПЛАНИРОВАНИЕ**  
**Приоритет:** СРЕДНИЙ  
**Версия:** 1.0

## 🎯 ЦЕЛЬ ФАЗЫ

Реализовать продвинутые возможности интеграции:
- HTTP API Development
- Plugin Integration
- Metrics & Observability

## 📋 ЗАДАЧИ

### 3.1 HTTP API Development

#### 3.1.1 REST API Endpoints
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Реализовать HTTP API в sboxagent
- [ ] REST endpoints для управления
- [ ] Authentication и authorization
- [ ] Rate limiting и security

**API Endpoints:**
```go
// internal/api/routes.go
func (s *Server) setupRoutes() {
    // Health endpoints
    s.router.GET("/api/v1/health", s.handleHealth)
    s.router.GET("/api/v1/status", s.handleStatus)
    
    // Process management
    s.router.POST("/api/v1/processes", s.handleStartProcess)
    s.router.DELETE("/api/v1/processes/{id}", s.handleStopProcess)
    s.router.GET("/api/v1/processes", s.handleListProcesses)
    s.router.GET("/api/v1/processes/{id}", s.handleGetProcess)
    
    // Logs and events
    s.router.GET("/api/v1/logs", s.handleGetLogs)
    s.router.GET("/api/v1/events", s.handleGetEvents)
    s.router.POST("/api/v1/events", s.handleCreateEvent)
    
    // Configuration
    s.router.GET("/api/v1/config", s.handleGetConfig)
    s.router.PUT("/api/v1/config", s.handleUpdateConfig)
    s.router.POST("/api/v1/config/reload", s.handleReloadConfig)
    
    // Metrics
    s.router.GET("/api/v1/metrics", s.handleGetMetrics)
    s.router.GET("/api/v1/metrics/prometheus", s.handlePrometheusMetrics)
}
```

#### 3.1.2 WebSocket Support
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] WebSocket для real-time событий
- [ ] Event streaming
- [ ] Connection management
- [ ] Authentication для WebSocket

**WebSocket Implementation:**
```go
// internal/api/websocket.go
type WebSocketManager struct {
    connections map[string]*WebSocketConnection
    mu          sync.RWMutex
    eventChan   chan Event
}

type WebSocketConnection struct {
    ID       string
    Conn     *websocket.Conn
    Send     chan []byte
    UserID   string
    LastPing time.Time
}

func (wsm *WebSocketManager) Start() {
    go wsm.eventLoop()
    go wsm.cleanupLoop()
}

func (wsm *WebSocketManager) eventLoop() {
    for event := range wsm.eventChan {
        wsm.broadcastEvent(event)
    }
}

func (wsm *WebSocketManager) broadcastEvent(event Event) {
    data, err := json.Marshal(event)
    if err != nil {
        log.Printf("Failed to marshal event: %v", err)
        return
    }
    
    wsm.mu.RLock()
    defer wsm.mu.RUnlock()
    
    for _, conn := range wsm.connections {
        select {
        case conn.Send <- data:
        default:
            // Connection is full, skip
        }
    }
}
```

#### 3.1.3 API Security
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Token-based authentication
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Request validation

### 3.2 Plugin Integration

#### 3.2.1 Plugin Event System
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Получение событий от sboxmgr plugins
- [ ] Plugin health monitoring
- [ ] Plugin configuration management
- [ ] Plugin lifecycle management

**Plugin Integration:**
```go
// internal/integration/plugin_manager.go
type PluginManager struct {
    plugins map[string]*Plugin
    mu      sync.RWMutex
    events  chan PluginEvent
}

type Plugin struct {
    ID       string
    Name     string
    Status   PluginStatus
    Config   map[string]interface{}
    Events   []PluginEvent
    LastSeen time.Time
}

type PluginEvent struct {
    PluginID string
    Type     string
    Data     map[string]interface{}
    Timestamp time.Time
}

func (pm *PluginManager) HandlePluginEvent(event PluginEvent) {
    pm.mu.Lock()
    plugin, exists := pm.plugins[event.PluginID]
    if !exists {
        plugin = &Plugin{
            ID:       event.PluginID,
            Status:   PluginStatusUnknown,
            Events:   make([]PluginEvent, 0),
            LastSeen: time.Now(),
        }
        pm.plugins[event.PluginID] = plugin
    }
    pm.mu.Unlock()
    
    // Обновление статуса плагина
    plugin.LastSeen = time.Now()
    plugin.Events = append(plugin.Events, event)
    
    // Ограничение количества событий
    if len(plugin.Events) > 100 {
        plugin.Events = plugin.Events[len(plugin.Events)-100:]
    }
    
    // Отправка события в event dispatcher
    pm.events <- event
}
```

#### 3.2.2 Plugin Health Monitoring
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Мониторинг состояния плагинов
- [ ] Проверка доступности плагинов
- [ ] Алерты при проблемах с плагинами
- [ ] Автоматическое восстановление плагинов

#### 3.2.3 Plugin Configuration
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Управление конфигурацией плагинов
- [ ] Hot-reload конфигурации плагинов
- [ ] Валидация конфигурации плагинов
- [ ] Backup и restore конфигурации

### 3.3 Metrics & Observability

#### 3.3.1 Metrics Collection
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Системные метрики
- [ ] Процессные метрики
- [ ] Бизнес метрики
- [ ] Custom метрики

**Metrics Implementation:**
```go
// internal/metrics/collector.go
type MetricsCollector struct {
    registry *prometheus.Registry
    metrics  map[string]prometheus.Collector
    mu       sync.RWMutex
}

type SystemMetrics struct {
    CPUUsage    float64
    MemoryUsage float64
    DiskUsage   float64
    NetworkIO   NetworkMetrics
}

type ProcessMetrics struct {
    ProcessID   string
    CPUUsage    float64
    MemoryUsage float64
    Uptime      time.Duration
    Status      string
}

type BusinessMetrics struct {
    SubscriptionsProcessed int64
    ConfigsGenerated       int64
    ErrorsCount           int64
    ProcessingTime        time.Duration
}

func (mc *MetricsCollector) CollectSystemMetrics() SystemMetrics {
    // Сбор системных метрик
    var m runtime.MemStats
    runtime.ReadMemStats(&m)
    
    return SystemMetrics{
        CPUUsage:    mc.getCPUUsage(),
        MemoryUsage: float64(m.Alloc) / float64(m.Sys) * 100,
        DiskUsage:   mc.getDiskUsage(),
        NetworkIO:   mc.getNetworkMetrics(),
    }
}

func (mc *MetricsCollector) CollectProcessMetrics() []ProcessMetrics {
    // Сбор метрик процессов
    var metrics []ProcessMetrics
    
    mc.processManager.mu.RLock()
    for id, process := range mc.processManager.processes {
        metrics = append(metrics, ProcessMetrics{
            ProcessID:   id,
            CPUUsage:    mc.getProcessCPUUsage(process),
            MemoryUsage: mc.getProcessMemoryUsage(process),
            Uptime:      time.Since(process.StartTime),
            Status:      string(process.Status),
        })
    }
    mc.processManager.mu.RUnlock()
    
    return metrics
}
```

#### 3.3.2 Prometheus Integration
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Prometheus metrics endpoint
- [ ] Custom Prometheus collectors
- [ ] Metrics labeling
- [ ] Metrics aggregation

#### 3.3.3 Unified Logging
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Structured logging format
- [ ] Log correlation
- [ ] Log aggregation
- [ ] Log retention policies

## 🔧 ТЕХНИЧЕСКИЕ ДЕТАЛИ

### Структура файлов

```
sboxagent/internal/
├── api/
│   ├── server.go
│   ├── routes.go
│   ├── handlers.go
│   ├── middleware.go
│   ├── websocket.go
│   └── types.go
├── integration/
│   ├── plugin_manager.go
│   ├── plugin_health.go
│   └── plugin_config.go
└── metrics/
    ├── collector.go
    ├── prometheus.go
    ├── system.go
    ├── process.go
    └── business.go

sboxmgr/src/sboxmgr/
├── plugins/
│   ├── event_emitter.py
│   ├── health_reporter.py
│   └── metrics_collector.py
└── api/
    ├── client.py
    └── websocket_client.py
```

### API Configuration

```yaml
# /etc/sboxagent/api.yaml
api:
  enabled: true
  port: 8080
  host: "127.0.0.1"
  
  security:
    auth_enabled: true
    auth_token: "your-secure-token"
    rate_limit:
      enabled: true
      requests_per_minute: 100
    cors:
      enabled: true
      allowed_origins: ["http://localhost:3000"]
  
  websocket:
    enabled: true
    ping_interval: "30s"
    pong_timeout: "10s"
    max_connections: 100
  
  metrics:
    enabled: true
    prometheus_endpoint: "/metrics"
    collection_interval: "15s"
```

### Plugin Configuration

```yaml
# /etc/sboxagent/plugins.yaml
plugins:
  enabled: true
  
  health_check:
    enabled: true
    interval: "60s"
    timeout: "10s"
    retries: 3
  
  event_collection:
    enabled: true
    buffer_size: 1000
    flush_interval: "5s"
  
  configuration:
    auto_reload: true
    validation: true
    backup_enabled: true
    backup_retention: "7d"
```

## 🚀 ПЛАН РЕАЛИЗАЦИИ

### Неделя 1: HTTP API
- [ ] Реализовать REST API endpoints
- [ ] Добавить authentication и security
- [ ] Реализовать WebSocket support
- [ ] Добавить API documentation

### Неделя 2: Plugin Integration
- [ ] Реализовать plugin event system
- [ ] Добавить plugin health monitoring
- [ ] Реализовать plugin configuration
- [ ] Интегрировать с sboxmgr plugins

### Неделя 3: Metrics & Observability
- [ ] Реализовать metrics collection
- [ ] Добавить Prometheus integration
- [ ] Реализовать unified logging
- [ ] Добавить monitoring dashboards

### Неделя 4: Testing & Polish
- [ ] End-to-end API testing
- [ ] Performance testing
- [ ] Security testing
- [ ] Documentation and examples

## 🧪 ТЕСТИРОВАНИЕ

### API Testing
- [ ] All REST endpoints work correctly
- [ ] Authentication and authorization work
- [ ] Rate limiting works properly
- [ ] WebSocket connections work
- [ ] API documentation is accurate

### Plugin Integration Testing
- [ ] Plugin events are received correctly
- [ ] Plugin health monitoring works
- [ ] Plugin configuration management works
- [ ] Plugin lifecycle management works

### Metrics Testing
- [ ] Metrics collection works correctly
- [ ] Prometheus integration works
- [ ] Metrics are accurate and timely
- [ ] Logging is structured and correlated

### Performance Testing
- [ ] API response times are acceptable
- [ ] WebSocket can handle many connections
- [ ] Metrics collection doesn't impact performance
- [ ] Memory usage is reasonable

## 🔍 КРИТЕРИИ УСПЕХА

### Функциональные
- [ ] HTTP API полностью функционален
- [ ] WebSocket работает для real-time событий
- [ ] Plugin integration работает
- [ ] Metrics и observability работают

### Технические
- [ ] API соответствует REST principles
- [ ] Security requirements соблюдены
- [ ] Performance requirements соблюдены
- [ ] Scalability requirements соблюдены

### Качественные
- [ ] API хорошо документирован
- [ ] Code quality высокая
- [ ] Tests покрывают все сценарии
- [ ] Monitoring и alerting работают

## 🔗 СВЯЗАННЫЕ ДОКУМЕНТЫ

- [Cross-Project Integration Plan](../integration-plan.md)
- [INTEGRATION-01: Foundation](phase-1-foundation.md)
- [INTEGRATION-02: Runtime](phase-2-runtime.md)
- [sboxagent Phase 1C Plan](../../../../sboxagent/plans/phase-1c/plan.md)

## 📝 ЗАМЕТКИ

### Приоритеты
1. **HTTP API** - основа для интеграции
2. **Plugin Integration** - расширяемость
3. **Metrics & Observability** - мониторинг

### Риски
- Complexity HTTP API development
- Security considerations для API
- Performance impact от metrics collection

### Альтернативы
- Если HTTP API сложен, можно начать с simple endpoints
- Если metrics тяжелы, можно уменьшить collection frequency

### Future Considerations
- GraphQL API для более гибких запросов
- gRPC для high-performance communication
- Distributed tracing (Jaeger, Zipkin)
- Advanced monitoring (Grafana, AlertManager)

---

**Следующий шаг:** Начать реализацию [INTEGRATION-01: Foundation](phase-1-foundation.md) 