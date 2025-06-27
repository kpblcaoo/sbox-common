# Cross-Project Integration Plan

**Дата создания:** 2025-06-27  
**Статус:** 🔄 **В РАЗРАБОТКЕ**  
**Версия:** 1.0

## 🎯 ЦЕЛЬ ИНТЕГРАЦИИ

Объединить три проекта в единую экосистему:
- **sboxmgr** (Python CLI) - обработка подписок, генерация конфигураций
- **sboxagent** (Go daemon) - оркестрация, логирование, мониторинг
- **sbox-common** (Shared) - общие схемы, протоколы, интерфейсы

## 📊 ТЕКУЩИЙ СТАТУС ПРОЕКТОВ

### sboxagent ✅ MVP ГОТОВ
- **Версия:** 0.1.0-alpha
- **Статус:** Phase 1B MVP завершена
- **Готово:** Agent core, event dispatcher, log aggregator, health checker, systemd integration
- **Следующий этап:** Phase 1C (HTTP API, метрики)
- **Интеграция:** Готов к интеграции с sboxmgr

### sboxmgr 🔄 STAGE 4
- **Версия:** v1.5.0 (Stage 4: Agent Integration & Security)
- **Статус:** Планирование интеграции с агентом
- **Готово:** CLI, plugin system, configuration, logging, event system
- **Следующий этап:** Интеграция с sboxagent
- **Интеграция:** Планирование CLI команд для управления агентом

### sbox-common 🔄 БАЗОВЫЙ
- **Статус:** Базовые схемы и протоколы
- **Готово:** CLI utilities, примеры, базовые схемы (agent_config.json, api.schema.json)
- **Следующий этап:** Общие интерфейсы интеграции
- **Интеграция:** Частично готовы схемы для интеграции

## 🏗️ АРХИТЕКТУРА ИНТЕГРАЦИИ

### Point-to-Point Architecture (Phase 1-2)
```
┌─────────────────────────────────────────────────────────────┐
│                    Sbox Ecosystem                           │
├─────────────────────────────────────────────────────────────┤
│  sboxmgr (Python CLI)        │  sboxagent (Go daemon)      │
│  - subscription processing    │  - orchestration            │
│  - config generation         │  - logging & aggregation    │
│  - plugin system             │  - health monitoring        │
│  - stdout capture            │  - HTTP API                 │
├─────────────────────────────────────────────────────────────┤
│                    sbox-common (Shared)                    │
│  - configuration schemas     │  - API protocols            │
│  - event definitions         │  - CLI interfaces           │
│  - integration contracts     │  - shared utilities         │
└─────────────────────────────────────────────────────────────┘
```

### Event Bus Architecture (Phase 3+)
```
┌─────────────────────────────────────────────────────────────┐
│                    Sbox Ecosystem v2.0                     │
├─────────────────────────────────────────────────────────────┤
│  sboxmgr (Python CLI)        │  sboxagent (Go daemon)      │
│  - subscription processing    │  - orchestration            │
│  - config generation         │  - logging & aggregation    │
│  - plugin system             │  - health monitoring        │
│  - event publisher           │  - HTTP API                 │
├─────────────────────────────────────────────────────────────┤
│                    Event Bus (sbox-common)                 │
│  - event routing             │  - event persistence        │
│  - event filtering           │  - event broadcasting       │
│  - event replay              │  - event validation         │
├─────────────────────────────────────────────────────────────┤
│  sbox-tui (Future)           │  sbox-monitor (Future)      │
│  - real-time UI              │  - metrics dashboard        │
│  - event consumer            │  - alerting system          │
└─────────────────────────────────────────────────────────────┘
```

## 📋 ПЛАН ИНТЕГРАЦИИ

### [INTEGRATION-01: Foundation](phases/phase-1-foundation.md)
**Приоритет:** ВЫСОКИЙ**

#### 1.1 Общие схемы конфигурации
- [x] Создать JSON схемы в sbox-common для:
  - [x] Agent configuration (agent.yaml) ✅ ГОТОВО
  - [ ] Sboxmgr configuration (sboxmgr.yaml)
  - [ ] Integration configuration (integration.yaml)
- [x] Валидация схем в sboxagent ✅ ГОТОВО
- [ ] Валидация схем в sboxmgr
- [ ] Синхронизация версий схем

#### 1.2 Event Protocol
- [ ] Определить общие типы событий в sbox-common
- [ ] Стандартизировать формат событий между sboxmgr и sboxagent
- [ ] Создать event converters для совместимости

#### 1.3 CLI Integration
- [ ] Добавить в sboxmgr команды для управления агентом:
  - [ ] `sboxmgr agent status` - статус агента
  - [ ] `sboxmgr agent start/stop/restart` - управление агентом
  - [ ] `sboxmgr agent logs` - просмотр логов
  - [ ] `sboxmgr agent config` - управление конфигурацией
- [ ] Интеграция с HTTP API sboxagent

### [INTEGRATION-02: Runtime](phases/phase-2-runtime.md)
**Приоритет:** ВЫСОКИЙ**

#### 2.1 Stdout Capture
- [ ] sboxagent перехватывает stdout sboxmgr
- [ ] Парсинг и структурирование логов
- [ ] Event generation из логов sboxmgr

#### 2.2 Configuration Synchronization
- [ ] Автоматическая синхронизация конфигураций
- [ ] Hot-reload конфигурации агента
- [ ] Validation конфигураций через общие схемы

#### 2.3 Health Monitoring
- [ ] sboxagent мониторит состояние sboxmgr
- [ ] Health checks для CLI процессов
- [ ] Alerting при проблемах

### [INTEGRATION-03: Advanced](phases/phase-3-advanced.md)
**Приоритет:** СРЕДНИЙ**

#### 3.1 HTTP API Development
- [ ] Реализовать HTTP API в sboxagent (Phase 1C)
- [ ] REST endpoints для управления
- [ ] WebSocket для real-time событий

#### 3.2 Plugin Integration
- [ ] sboxagent получает события от sboxmgr plugins
- [ ] Plugin health monitoring
- [ ] Plugin configuration management

#### 3.3 Metrics & Observability
- [ ] Общие метрики между проектами
- [ ] Unified logging format
- [ ] Centralized monitoring

## 🔧 ТЕХНИЧЕСКИЕ ДЕТАЛИ

### Конфигурация интеграции
```yaml
# /etc/sboxagent/integration.yaml
integration:
  sboxmgr:
    enabled: true
    command: ["sboxmgr", "update"]
    interval: "30m"
    timeout: "5m"
    stdout_capture: true
    health_check:
      enabled: true
      interval: "60s"
  
  events:
    subscription_updated: true
    config_generated: true
    error_occurred: true
  
  api:
    enabled: true
    mode: "integrated"  # standalone | integrated | disabled
    port: 8080
    auth_token: "your-secure-token"
    hardening:
      read_only_cli: false  # Отключает CLI write access в systemd режиме
      local_only: true      # Только localhost connections
```

### Event Protocol
```json
{
  "type": "subscription_updated",
  "source": "sboxmgr",
  "timestamp": "2025-06-27T23:30:00Z",
  "version": "1.0",
  "data": {
    "subscription_url": "https://...",
    "servers_count": 150,
    "status": "success",
    "duration_ms": 2500
  },
  "metadata": {
    "correlation_id": "uuid-here",
    "user_id": "optional-user-id"
  }
}
```

### CLI Commands
```bash
# Управление агентом через sboxmgr
sboxmgr agent status
sboxmgr agent start
sboxmgr agent stop
sboxmgr agent restart
sboxmgr agent logs --tail=100
sboxmgr agent config show
sboxmgr agent config update /path/to/config.yaml

# Интеграция с обновлениями
sboxmgr update --with-agent  # Запуск через агента
sboxmgr update --standalone  # Прямой запуск
sboxmgr update --dry-run     # Тестовый запуск
```

## 📁 СТРУКТУРА ФАЙЛОВ

### sbox-common/
```
sbox-common/
├── schemas/
│   ├── agent-config.schema.json ✅ ГОТОВО
│   ├── sboxmgr-config.schema.json 📋 ПЛАНИРОВАНИЕ
│   └── integration-config.schema.json 📋 ПЛАНИРОВАНИЕ
├── protocols/
│   ├── api.schema.json ✅ ГОТОВО
│   ├── events/
│   │   ├── subscription-events.json 📋 ПЛАНИРОВАНИЕ
│   │   ├── config-events.json 📋 ПЛАНИРОВАНИЕ
│   │   └── health-events.json 📋 ПЛАНИРОВАНИЕ
│   └── api/
│       ├── agent-api.json 📋 ПЛАНИРОВАНИЕ
│       └── integration-api.json 📋 ПЛАНИРОВАНИЕ
└── cli/
    ├── agent-commands.py 📋 ПЛАНИРОВАНИЕ
    └── integration-utils.py 📋 ПЛАНИРОВАНИЕ
```

### sboxmgr/
```
sboxmgr/src/sboxmgr/cli/
├── agent.py 📋 ПЛАНИРОВАНИЕ
├── integration.py 📋 ПЛАНИРОВАНИЕ
└── utils/
    ├── agent_client.py 📋 ПЛАНИРОВАНИЕ
    └── event_sender.py 📋 ПЛАНИРОВАНИЕ
```

### sboxagent/
```
sboxagent/internal/
├── api/ 📋 ПЛАНИРОВАНИЕ (Phase 1C)
├── integration/ 📋 ПЛАНИРОВАНИЕ
│   ├── sboxmgr_client.go 📋 ПЛАНИРОВАНИЕ
│   ├── event_handler.go 📋 ПЛАНИРОВАНИЕ
│   └── config_sync.go 📋 ПЛАНИРОВАНИЕ
└── schemas/ ✅ ГОТОВО (в config/)
```

## 🚀 ПЛАН РЕАЛИЗАЦИИ

### Неделя 1: Foundation (частично готово)
- [x] Создать схемы в sbox-common (agent-config готов)
- [ ] Добавить CLI команды в sboxmgr
- [ ] Настроить базовую интеграцию

### Неделя 2: Runtime
- [ ] Реализовать stdout capture
- [ ] Настроить event protocol
- [ ] Добавить health monitoring

### Неделя 3: API
- [ ] Разработать HTTP API в sboxagent
- [ ] Интегрировать CLI с API
- [ ] Добавить authentication

### Неделя 4: Testing & Polish
- [ ] End-to-end тестирование
- [ ] Документация интеграции
- [ ] Performance optimization

## 🧪 INTEGRATION TESTING

### CLI-to-API Testing
- [ ] CLI commands successfully call API endpoints
- [ ] Error handling works correctly
- [ ] Authentication/authorization works
- [ ] Rate limiting and timeouts work

### API Schema Conformance
- [ ] All API responses match schemas
- [ ] Request validation works
- [ ] Version compatibility maintained
- [ ] Schema evolution handled

### Cross-Version Compatibility
- [ ] sboxmgr v1.5.0 ↔ sboxagent v0.1.0
- [ ] Backward compatibility maintained
- [ ] Forward compatibility planned
- [ ] Version negotiation works

### Config Reload Testing
- [ ] Hot-reload without downtime
- [ ] Config validation on reload
- [ ] Rollback on invalid config
- [ ] Config synchronization works

## 🔍 КРИТЕРИИ УСПЕХА

### Функциональные
- [ ] sboxmgr может управлять sboxagent через CLI
- [ ] sboxagent перехватывает и обрабатывает stdout sboxmgr
- [ ] Конфигурации синхронизируются между проектами
- [ ] Health monitoring работает для обоих компонентов

### Технические
- [x] Общие схемы валидации работают (agent-config)
- [ ] Event protocol стандартизирован
- [ ] HTTP API стабилен и документирован
- [ ] CLI интеграция интуитивна

### Качественные
- [ ] Документация интеграции полная
- [ ] Тесты покрывают все сценарии
- [ ] Performance не деградирует
- [ ] Security requirements соблюдены

## 🔗 СВЯЗАННЫЕ ДОКУМЕНТЫ

- [sboxagent Phase 1B Plan](../../../sboxagent/plans/phase-1b/plan.md)
- [sboxmgr Stage 4 Plan](../../../sboxmgr/plans/roadmap_v1.5.0/stage4-agent-integration/README.md)
- [ADR-0012: Service Architecture](../../../sboxmgr/docs/arch/decisions/ADR-0012-service-architecture.md)

## 📝 ЗАМЕТКИ

### Приоритеты
1. **Foundation Integration** - базовые схемы и CLI (частично готово)
2. **Runtime Integration** - stdout capture и events
3. **Advanced Integration** - API и observability

### Риски
- Сложность синхронизации конфигураций
- Performance impact от stdout capture
- Security considerations для HTTP API

### Альтернативы
- Если интеграция сложна, можно начать с простого autoupdater (systemd timer)
- Постепенная миграция от autoupdater к sboxagent

### Security Considerations
- API mode control (standalone/integrated/disabled)
- CLI hardening в systemd режиме
- Local-only connections по умолчанию
- Token-based authentication
- Rate limiting для API endpoints

### Прогресс
- **INTEGRATION-01:** 30% готово (agent-config schema, api schema)
- **INTEGRATION-02:** 0% готово
- **INTEGRATION-03:** 0% готово

---

**Следующий шаг:** [INTEGRATION-01: Foundation](phases/phase-1-foundation.md) 