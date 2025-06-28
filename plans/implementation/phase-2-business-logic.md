# Phase 2: JSON Protocols & Schema Standardization

**Длительность:** 3-5 дней
**Статус:** 📋 ПЛАНИРОВАНИЕ

## 🎯 ЦЕЛИ ФАЗЫ (согласно ADR-0001)

### Основные задачи
- [ ] **Configuration Schema** - стандартизация JSON схем конфигураций
- [ ] **Interface Protocol** - протокол взаимодействия sboxmgr ↔ sboxagent
- [ ] **Client Schemas** - схемы для всех subbox клиентов
- [ ] **Validation Framework** - утилиты валидации JSON
- [ ] **Documentation** - документация протоколов

## 📋 ДЕТАЛЬНЫЙ ПЛАН

### Day 1-2: Configuration Schemas
- [ ] Схемы конфигураций для sing-box
- [ ] Схемы конфигураций для clash
- [ ] Схемы конфигураций для xray
- [ ] Общие базовые схемы

### Day 3-4: Interface Protocol
- [ ] sboxmgr output format schema
- [ ] sboxagent input format schema
- [ ] Command protocol specification
- [ ] Status response schemas

### Day 5: Validation & Documentation
- [ ] JSON validation utilities
- [ ] Example configurations
- [ ] Protocol documentation
- [ ] Migration guides

## 🔧 ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ

### Configuration Schema Structure
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Subbox Configuration",
  "type": "object",
  "properties": {
    "client": {
      "type": "string",
      "enum": ["sing-box", "clash", "xray", "mihomo"]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "config": {
      "type": "object"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "source": {"type": "string"},
        "checksum": {"type": "string"},
        "generator": {"type": "string"}
      }
    }
  },
  "required": ["client", "version", "created_at", "config"]
}
```

### Interface Protocol
```json
{
  "command": {
    "type": "generate|apply|status|validate",
    "client": "sing-box|clash|xray|mihomo",
    "params": {},
    "timestamp": "2025-06-28T13:35:22Z"
  },
  "response": {
    "status": "success|error",
    "data": {},
    "message": "string",
    "timestamp": "2025-06-28T13:35:22Z"
  }
}
```

### Client-Specific Schemas
```json
// sing-box.schema.json
{
  "type": "object",
  "properties": {
    "log": {"$ref": "#/definitions/log"},
    "dns": {"$ref": "#/definitions/dns"},
    "inbounds": {"type": "array"},
    "outbounds": {"type": "array"},
    "route": {"$ref": "#/definitions/route"}
  }
}

// clash.schema.json
{
  "type": "object", 
  "properties": {
    "port": {"type": "integer"},
    "socks-port": {"type": "integer"},
    "proxies": {"type": "array"},
    "proxy-groups": {"type": "array"},
    "rules": {"type": "array"}
  }
}
```

## 📁 СОЗДАВАЕМЫЕ ФАЙЛЫ

### schemas/
- `base-config.schema.json` - базовая схема конфигурации
- `interface-protocol.schema.json` - протокол взаимодействия
- `sing-box.schema.json` - схема sing-box конфигурации
- `clash.schema.json` - схема clash конфигурации
- `xray.schema.json` - схема xray конфигурации
- `mihomo.schema.json` - схема mihomo конфигурации

### protocols/
- `sboxmgr-output.schema.json` - формат вывода sboxmgr
- `sboxagent-input.schema.json` - формат ввода sboxagent
- `status-response.schema.json` - формат статусных ответов
- `error-response.schema.json` - формат ошибок

### validation/
- `validator.py` - Python валидатор
- `validator.go` - Go валидатор
- `examples/` - примеры валидных конфигураций

### docs/
- `protocol-specification.md` - спецификация протокола
- `schema-reference.md` - справочник схем
- `migration-guide.md` - руководство по миграции

## 🧪 ТЕСТИРОВАНИЕ

### Schema Validation Tests
- [ ] Валидация базовых схем
- [ ] Валидация клиентских схем
- [ ] Валидация протокольных схем
- [ ] Негативные тесты (невалидные данные)

### Cross-Language Tests
- [ ] Python validator tests
- [ ] Go validator tests
- [ ] Совместимость валидаторов
- [ ] Performance benchmarks

### Integration Tests
- [ ] sboxmgr output validation
- [ ] sboxagent input validation
- [ ] End-to-end protocol tests
- [ ] Real configuration examples

## 📝 КРИТЕРИИ ЗАВЕРШЕНИЯ

### Schema Completeness: 🔄 IN PROGRESS
- [ ] Все клиентские схемы определены
- [ ] Протокольные схемы готовы
- [ ] Валидация работает
- [ ] Документация полная

### Cross-Platform Support: 🔄 IN PROGRESS
- [ ] Python валидатор работает
- [ ] Go валидатор работает
- [ ] Совместимость подтверждена
- [ ] Performance приемлемый

### Integration Ready: 🔄 IN PROGRESS
- [ ] sboxmgr может использовать схемы
- [ ] sboxagent может использовать схемы
- [ ] Протокол документирован
- [ ] Примеры готовы

## 🔄 СООТВЕТСТВИЕ ADR-0001

### Роль sbox-common:
- ✅ **Protocols & Schemas** - JSON схемы и протоколы
- ✅ **Shared Standards** - общие стандарты для всех компонентов
- ✅ **License Clean** - Apache-2.0, совместимо со всеми

### Интерфейс:
- ✅ **JSON-Only** - все взаимодействие через JSON
- ✅ **Language Agnostic** - работает с Python и Go
- ✅ **Validation Ready** - готовые валидаторы

### Принципы:
- ✅ **Single Responsibility** - только схемы и протоколы
- ✅ **No Logic Duplication** - общие схемы для всех
- ✅ **Clean Boundaries** - четкие интерфейсы

**Статус:** 🔄 **PHASE 2 В ПЛАНИРОВАНИИ**
