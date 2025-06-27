# Sbox Ecosystem Integration

**Дата создания:** 2025-06-27  
**Статус:** 📋 **ПЛАНИРОВАНИЕ**  
**Версия:** 1.0

## 🎯 Обзор

Объединение трех проектов в единую экосистему:
- **sboxmgr** (Python CLI) - обработка подписок, генерация конфигураций
- **sboxagent** (Go daemon) - оркестрация, логирование, мониторинг  
- **sbox-common** (Shared) - общие схемы, протоколы, интерфейсы

## 🏗️ Архитектура

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

## 📋 Этапы интеграции

### [INTEGRATION-01: Foundation](docs/phases/phase-1-foundation.md)
**Статус:** 🔄 **В РАЗРАБОТКЕ**  
**Приоритет:** ВЫСОКИЙ

- ✅ Общие схемы конфигурации (частично)
- 📋 Event Protocol
- 📋 CLI Integration

### [INTEGRATION-02: Runtime](docs/phases/phase-2-runtime.md)
**Статус:** 📋 **ПЛАНИРОВАНИЕ**  
**Приоритет:** ВЫСОКИЙ

- 📋 Stdout Capture
- 📋 Configuration Synchronization  
- 📋 Health Monitoring

### [INTEGRATION-03: Advanced](docs/phases/phase-3-advanced.md)
**Статус:** 📋 **ПЛАНИРОВАНИЕ**  
**Приоритет:** СРЕДНИЙ

- 📋 HTTP API Development
- 📋 Plugin Integration
- 📋 Metrics & Observability

## 🔗 Документация

- **[Полный план интеграции](docs/integration-plan.md)** - детальный технический план
- **[Архитектурные решения](docs/architecture.md)** - ADR и схемы
- **[API спецификации](docs/api/)** - REST API и event protocols
- **[Тестирование](docs/testing.md)** - integration testing strategy

## 🚀 Быстрый старт

```bash
# Управление агентом через sboxmgr
sboxmgr agent status
sboxmgr agent start/stop/restart
sboxmgr agent logs --tail=100

# Интеграция с обновлениями
sboxmgr update --with-agent  # Запуск через агента
sboxmgr update --standalone  # Прямой запуск
```

## 📊 Статус проектов

| Проект | Версия | Статус | Готовность | Интеграция |
|--------|--------|--------|------------|------------|
| **sboxagent** | 0.1.0-alpha | ✅ MVP готов | 90% | 🔄 Foundation |
| **sboxmgr** | v1.5.0 | 🔄 Stage 4 | 75% | 📋 Планирование |
| **sbox-common** | - | 🔄 Базовый | 40% | 🔄 Foundation |

### Детальный статус:

#### sboxagent ✅ MVP ГОТОВ
- **Готово:** Agent core, event dispatcher, log aggregator, health checker, systemd integration
- **Следующий этап:** Phase 1C (HTTP API, метрики)
- **Интеграция:** Готов к интеграции с sboxmgr

#### sboxmgr 🔄 STAGE 4
- **Готово:** CLI, plugin system, configuration, logging, event system
- **Следующий этап:** Интеграция с sboxagent
- **Интеграция:** Планирование CLI команд для управления агентом

#### sbox-common 🔄 БАЗОВЫЙ
- **Готово:** Базовые схемы (agent_config.json, api.schema.json)
- **Следующий этап:** Event protocols, CLI interfaces
- **Интеграция:** Частично готовы схемы для интеграции

---

**Следующий шаг:** [INTEGRATION-01: Foundation](docs/phases/phase-1-foundation.md) 