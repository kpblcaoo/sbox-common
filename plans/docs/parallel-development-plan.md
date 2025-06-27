# Parallel Development Plan

**Дата создания:** 2025-06-27  
**Статус:** 🚀 **В РАЗРАБОТКЕ**  
**Версия:** 1.1

## 🎯 ЦЕЛЬ

Координировать параллельную разработку INTEGRATION-01: Foundation между тремя проектами:
- **sboxmgr** - Security Framework + CLI Integration
- **sboxagent** - Event Handler + Process Manager
- **sbox-common** - Event Protocols + Schemas

## 📊 ТЕКУЩИЙ СТАТУС

### Ветки разработки:
- **sboxmgr:** `feature/integration-foundation` ✅
- **sboxagent:** `feature/integration-foundation` ✅  
- **sbox-common:** `feature/integration-foundation` ✅

### Готовность проектов:
- **sboxmgr:** 75% (CLI, plugin system, event system готовы)
- **sboxagent:** 90% (MVP готов, нужен Event Handler)
- **sbox-common:** 60% (event protocols готовы, converters готовы)

## 🏗️ АРХИТЕКТУРА РАЗРАБОТКИ

```
┌─────────────────────────────────────────────────────────────┐
│                    Parallel Development                     │
├─────────────────────────────────────────────────────────────┤
│  sboxmgr (Python)           │  sboxagent (Go)              │
│  - Security Framework       │  - Event Handler             │
│  - CLI Integration          │  - Process Manager           │
│  - Event Sender             │  - Log Parser                │
│  - IPC Client               │  - IPC Server                │
├─────────────────────────────────────────────────────────────┤
│                    sbox-common (Shared)                    │
│  - Event Protocols          │  - API Schemas               │
│  - Configuration Schemas    │  - CLI Interfaces            │
│  - Integration Contracts    │  - Shared Utilities          │
└─────────────────────────────────────────────────────────────┘
```

## 📋 ПЛАН РАЗРАБОТКИ

### Week 1: Foundation Setup

#### Day 1-2: Event Protocols (sbox-common) ✅
**Ответственный:** sbox-common  
**Зависимости:** Нет

- [x] Создать `protocols/events/subscription-events.json`
- [x] Создать `protocols/events/config-events.json`
- [x] Создать `protocols/events/health-events.json`
- [x] Создать event converters
- [x] Добавить event validation

#### Day 3-4: IPC Foundation (sboxagent)
**Ответственный:** sboxagent  
**Зависимости:** sbox-common event protocols

- [ ] Создать `internal/ipc/server.go`
- [ ] Создать `internal/ipc/client.go`
- [ ] Создать `internal/ipc/protocol.go`
- [ ] Добавить JSON message handling
- [ ] Добавить basic event processing

#### Day 5-7: Security Framework (sboxmgr)
**Ответственный:** sboxmgr  
**Зависимости:** sbox-common event protocols

- [ ] Создать `src/sboxmgr/security/sandbox.py`
- [ ] Создать `src/sboxmgr/security/audit.py`
- [ ] Создать `src/sboxmgr/security/access.py`
- [ ] Создать `src/sboxmgr/security/validation.py`
- [ ] Интегрировать с event system

### Week 2: Integration Implementation

#### Day 1-2: CLI Integration (sboxmgr)
**Ответственный:** sboxmgr  
**Зависимости:** sboxagent IPC

- [ ] Создать `src/sboxmgr/cli/commands/agent.py`
- [ ] Создать `src/sboxmgr/cli/utils/ipc_client.py`
- [ ] Создать `src/sboxmgr/cli/utils/event_sender.py`
- [ ] Добавить agent management commands
- [ ] Добавить error handling

#### Day 3-4: Event Handler (sboxagent)
**Ответственный:** sboxagent  
**Зависимости:** sbox-common event protocols

- [ ] Создать `internal/integration/event_handler.go`
- [ ] Создать `internal/integration/process_manager.go`
- [ ] Создать `internal/integration/log_parser.go`
- [ ] Интегрировать с event dispatcher
- [ ] Добавить event validation

#### Day 5-7: Configuration Sync (sbox-common + both)
**Ответственный:** sbox-common + sboxmgr + sboxagent  
**Зависимости:** Все foundation готово

- [ ] Создать `schemas/sboxmgr-config.schema.json`
- [ ] Создать `schemas/integration-config.schema.json`
- [ ] Добавить config validation в sboxmgr
- [ ] Добавить config validation в sboxagent
- [ ] Реализовать config sync

## 🔄 СИНХРОНИЗАЦИЯ РАЗРАБОТКИ

### Daily Sync Points:
- **9:00** - Daily standup (status, blockers, dependencies)
- **17:00** - Code review и merge requests
- **18:00** - Integration testing

### Weekly Milestones:
- **Week 1:** Foundation ready (event protocols, IPC, security framework)
- **Week 2:** Integration ready (CLI commands, event handler, config sync)

### Integration Testing:
- **Day 3:** Test event protocols between projects
- **Day 5:** Test IPC communication between sboxmgr and sboxagent
- **Day 7:** Test end-to-end integration

## 🧪 ТЕСТИРОВАНИЕ

### Unit Tests:
- **sbox-common:** Event protocol validation
- **sboxmgr:** Security framework, CLI commands
- **sboxagent:** IPC, event handler

### Integration Tests:
- **Event Flow:** sboxmgr → sbox-common → sboxagent
- **IPC Flow:** sboxmgr CLI → sboxagent IPC
- **Config Flow:** sboxmgr → sbox-common → sboxagent

### End-to-End Tests:
- **Full Integration:** Complete workflow testing
- **Error Handling:** Error scenarios and recovery
- **Performance:** Load testing and optimization

## 📊 КРИТЕРИИ ГОТОВНОСТИ

### Week 1 Criteria:
- [x] Event protocols работают между проектами
- [ ] IPC communication работает между sboxmgr и sboxagent
- [ ] Security framework функционирует
- [ ] Unit tests проходят

### Week 2 Criteria:
- [ ] CLI команды управляют агентом через IPC
- [ ] Event handler обрабатывает события
- [ ] Configuration sync работает
- [ ] Integration tests проходят

### Final Criteria:
- [ ] End-to-end workflow работает
- [ ] Error handling robust
- [ ] Performance acceptable
- [ ] Documentation complete

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

### Phase 2: HTTP API (Optional)
- **Когда:** После стабильной IPC интеграции
- **Зачем:** Remote management, external integrations
- **Что:** HTTP REST API поверх существующего event system

### Phase 3: Advanced Features
- **Когда:** После стабильной интеграции
- **Что:** Advanced monitoring, analytics, automation

---

**Статус**: 🚀 **В РАЗРАБОТКЕ**  
**Прогресс**: 25% (event protocols complete)  
**Следующий шаг**: Начать IPC foundation в sboxagent 