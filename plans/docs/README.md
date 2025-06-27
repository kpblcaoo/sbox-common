# Cross-Project Integration Documentation

**Дата создания:** 2025-06-27  
**Статус:** 🚀 **В РАЗРАБОТКЕ**  
**Версия:** 1.1

## 🎯 ОБЗОР

Этот документ описывает интеграцию между тремя проектами:
- **sboxmgr** - Python CLI для управления sing-box
- **sboxagent** - Go daemon для управления sing-box процессами
- **sbox-common** - Общие схемы и протоколы

## 📋 ФАЗЫ РАЗРАБОТКИ

### Phase 1: Foundation (INTEGRATION-01) 🚀 **В РАЗРАБОТКЕ**
**Цель:** Создать фундаментальную основу для интеграции

- **Event Protocols** - стандартизированные схемы событий
- **IPC Communication** - межпроцессное взаимодействие
- **Security Framework** - безопасность и валидация

**Прогресс:** 60% (Event Protocols Complete)

### Phase 2: Runtime (INTEGRATION-02) ⏳ **ПЛАНИРУЕТСЯ**
**Цель:** Реализовать рабочую интеграцию

- **CLI Integration** - команды управления агентом
- **Event Handler** - обработка событий в агенте
- **Configuration Sync** - синхронизация конфигураций

### Phase 3: Advanced (INTEGRATION-03) ⏳ **ПЛАНИРУЕТСЯ**
**Цель:** Расширенные возможности

- **Advanced Monitoring** - детальный мониторинг
- **Automation** - автоматизация процессов
- **Analytics** - аналитика и отчеты

## 🏗️ АРХИТЕКТУРА

### Event Flow
```
sboxmgr CLI → Event Sender → sbox-common Protocols → sboxagent Event Handler
```

### IPC Communication
```
sboxmgr (Python) ←→ IPC Protocol ←→ sboxagent (Go)
     ↓                    ↓                    ↓
Event Sender         JSON Messages        Event Handler
```

### Security Layers
```
┌─────────────────────────────────────────────────────────────┐
│                    Security Framework                       │
├─────────────────────────────────────────────────────────────┤
│  Sandbox Validation  │  Access Control  │  Audit Logging    │
│  - Plugin isolation  │  - Permissions   │  - Event tracking │
│  - Resource limits   │  - User roles    │  - Security events│
│  - Execution safety  │  - API access    │  - Compliance     │
└─────────────────────────────────────────────────────────────┘
```

## 📁 СТРУКТУРА ФАЙЛОВ

```
plans/docs/
├── README.md                    # Этот файл
├── parallel-development-plan.md # План параллельной разработки
└── phases/
    ├── foundation.md           # Phase 1: Foundation
    ├── runtime.md              # Phase 2: Runtime
    └── advanced.md             # Phase 3: Advanced
```

## 🔄 ТЕКУЩИЙ СТАТУС

### Ветки разработки:
- **sboxmgr:** `feature/integration-foundation` ✅
- **sboxagent:** `feature/integration-foundation` ✅  
- **sbox-common:** `feature/integration-foundation` ✅

### Готовность проектов:
- **sboxmgr:** 75% (CLI, plugin system, event system готовы)
- **sboxagent:** 90% (MVP готов, нужен Event Handler)
- **sbox-common:** 60% (event protocols готовы, converters готовы)

## 🧪 ТЕСТИРОВАНИЕ

### Unit Tests
- **sbox-common:** Event protocol validation, converters
- **sboxmgr:** Security framework, CLI commands
- **sboxagent:** IPC, event handler

### Integration Tests
- **Event Flow:** sboxmgr → sbox-common → sboxagent
- **IPC Flow:** sboxmgr CLI → sboxagent IPC
- **Config Flow:** sboxmgr → sbox-common → sboxagent

### End-to-End Tests
- **Complete Workflow:** CLI command → Event → IPC → Processing → Response
- **Error Scenarios:** Invalid events, IPC failures, security violations
- **Performance:** Message throughput, latency, resource usage

## 📊 КРИТЕРИИ ГОТОВНОСТИ

### Foundation Phase
- [x] Event protocols работают между проектами
- [ ] IPC communication работает между sboxmgr и sboxagent
- [ ] Security framework функционирует
- [ ] Unit tests проходят

### Runtime Phase
- [ ] CLI команды управляют агентом через IPC
- [ ] Event handler обрабатывает события
- [ ] Configuration sync работает
- [ ] Integration tests проходят

### Advanced Phase
- [ ] Advanced monitoring работает
- [ ] Automation features реализованы
- [ ] Analytics и отчеты функционируют
- [ ] Performance optimization завершен

## 🔗 КОММУНИКАЦИЯ

### Communication Channels:
- **Git Issues:** Feature tracking и blockers
- **Pull Requests:** Code review и discussion
- **Daily Standup:** Status updates
- **Weekly Review:** Milestone review

### Decision Making:
- **Architecture:** Cross-project review
- **API Changes:** All projects must agree
- **Breaking Changes:** Coordinated release

## 🚀 СЛЕДУЮЩИЕ ШАГИ

### Immediate (Today):
1. ✅ Создать ветки для интеграции
2. ✅ Обновить планы Stage 4
3. ✅ Завершить event protocols в sbox-common
4. 🔄 Начать IPC foundation в sboxagent

### This Week:
1. ✅ Завершить event protocols
2. 🔄 Начать IPC в sboxagent
3. 🔄 Начать security framework в sboxmgr

### Next Week:
1. Завершить foundation
2. Начать integration implementation
3. Провести integration testing

## 🔮 FUTURE PHASES (Optional)

### HTTP API (Optional)
- **Когда:** После стабильной IPC интеграции
- **Зачем:** Remote management, external integrations
- **Что:** HTTP REST API поверх существующего event system

### Advanced Features
- **Когда:** После стабильной интеграции
- **Что:** Advanced monitoring, analytics, automation

---

**Статус**: 🚀 **В РАЗРАБОТКЕ**  
**Прогресс**: 25% (Event Protocols Complete)  
**Следующий шаг**: Начать IPC foundation в sboxagent 