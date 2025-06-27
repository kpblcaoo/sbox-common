# INTEGRATION-01: Foundation

**Дата создания:** 2025-06-27  
**Статус:** 🔄 **В РАЗРАБОТКЕ**  
**Приоритет:** ВЫСОКИЙ  
**Версия:** 1.0

## 🎯 ЦЕЛЬ ФАЗЫ

Создать фундаментальную основу для интеграции между sboxmgr и sboxagent:
- Общие схемы конфигурации
- Event Protocol
- CLI Integration

## 📋 ЗАДАЧИ

### 1.1 Общие схемы конфигурации

#### 1.1.1 Agent Configuration Schema
**Статус:** ✅ **ЗАВЕРШЕНО**

- [x] Создать `sbox-common/schemas/agent-config.schema.json`
- [x] Определить структуру конфигурации агента
- [x] Добавить валидацию в sboxagent
- [x] Создать примеры конфигурации

**Реализовано:** Полная JSON схема для конфигурации агента с поддержкой:
- Базовые настройки агента (name, version, log_level)
- HTTP API сервер (port, host, timeout)
- Управление сервисами (sboxmgr integration)
- Управление клиентами (sing-box, xray, clash, hysteria)
- Логирование и мониторинг

#### 1.1.2 Sboxmgr Configuration Schema
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Создать `sbox-common/schemas/sboxmgr-config.schema.json`
- [ ] Определить структуру конфигурации sboxmgr
- [ ] Добавить валидацию в sboxmgr
- [ ] Создать примеры конфигурации

#### 1.1.3 Integration Configuration Schema
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Создать `sbox-common/schemas/integration-config.schema.json`
- [ ] Определить параметры интеграции
- [ ] Добавить валидацию в оба проекта
- [ ] Создать примеры конфигурации

### 1.2 Event Protocol

#### 1.2.1 Event Definitions
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Создать `sbox-common/protocols/events/`
- [ ] Определить типы событий:
  - [ ] `subscription-events.json` - события подписок
  - [ ] `config-events.json` - события конфигураций
  - [ ] `health-events.json` - события здоровья
- [ ] Стандартизировать формат событий
- [ ] Создать event converters

**Event Format:**
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

#### 1.2.2 Event Types
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

**Subscription Events:**
- `subscription_started` - начало обработки подписки
- `subscription_updated` - подписка обновлена
- `subscription_failed` - ошибка обработки подписки
- `subscription_completed` - завершение обработки

**Config Events:**
- `config_generation_started` - начало генерации конфигурации
- `config_generated` - конфигурация сгенерирована
- `config_deployed` - конфигурация развернута
- `config_failed` - ошибка генерации/развертывания

**Health Events:**
- `health_check_started` - начало проверки здоровья
- `health_check_passed` - проверка пройдена
- `health_check_failed` - проверка не пройдена
- `service_started` - сервис запущен
- `service_stopped` - сервис остановлен

### 1.3 CLI Integration

#### 1.3.1 Agent Management Commands
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Создать `sboxmgr/src/sboxmgr/cli/agent.py`
- [ ] Реализовать команды:
  - [ ] `sboxmgr agent status` - статус агента
  - [ ] `sboxmgr agent start` - запуск агента
  - [ ] `sboxmgr agent stop` - остановка агента
  - [ ] `sboxmgr agent restart` - перезапуск агента
  - [ ] `sboxmgr agent logs` - просмотр логов
  - [ ] `sboxmgr agent config show` - показать конфигурацию
  - [ ] `sboxmgr agent config update` - обновить конфигурацию

#### 1.3.2 HTTP Client
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Создать `sboxmgr/src/sboxmgr/cli/utils/agent_client.py`
- [ ] Реализовать HTTP клиент для sboxagent API
- [ ] Добавить authentication
- [ ] Добавить error handling
- [ ] Добавить retry logic

#### 1.3.3 Event Sender
**Статус:** 📋 **ПЛАНИРОВАНИЕ**

- [ ] Создать `sboxmgr/src/sboxmgr/cli/utils/event_sender.py`
- [ ] Реализовать отправку событий в sboxagent
- [ ] Добавить event validation
- [ ] Добавить event queuing
- [ ] Добавить event retry

## 🔧 ТЕХНИЧЕСКИЕ ДЕТАЛИ

### Структура файлов

```
sbox-common/
├── schemas/
│   ├── agent-config.schema.json  ✅ ГОТОВО
│   ├── sboxmgr-config.schema.json 📋 ПЛАНИРОВАНИЕ
│   └── integration-config.schema.json 📋 ПЛАНИРОВАНИЕ
├── protocols/
│   ├── api.schema.json ✅ ГОТОВО
│   └── events/
│       ├── subscription-events.json 📋 ПЛАНИРОВАНИЕ
│       ├── config-events.json 📋 ПЛАНИРОВАНИЕ
│       └── health-events.json 📋 ПЛАНИРОВАНИЕ
└── cli/
    ├── agent-commands.py 📋 ПЛАНИРОВАНИЕ
    └── integration-utils.py 📋 ПЛАНИРОВАНИЕ

sboxmgr/src/sboxmgr/cli/
├── agent.py 📋 ПЛАНИРОВАНИЕ
└── utils/
    ├── agent_client.py 📋 ПЛАНИРОВАНИЕ
    └── event_sender.py 📋 ПЛАНИРОВАНИЕ

sboxagent/internal/
├── schemas/
│   └── validation.go ✅ ГОТОВО (в config/)
└── integration/
    └── event_handler.go 📋 ПЛАНИРОВАНИЕ
```

### CLI Commands Implementation

```python
# sboxmgr/src/sboxmgr/cli/agent.py
import click
from .utils.agent_client import AgentClient
from .utils.event_sender import EventSender

@click.group()
def agent():
    """Manage sboxagent daemon"""
    pass

@agent.command()
def status():
    """Show agent status"""
    client = AgentClient()
    status = client.get_status()
    click.echo(f"Agent status: {status}")

@agent.command()
def start():
    """Start agent"""
    client = AgentClient()
    client.start()
    click.echo("Agent started")

@agent.command()
def stop():
    """Stop agent"""
    client = AgentClient()
    client.stop()
    click.echo("Agent stopped")

@agent.command()
@click.option('--tail', default=100, help='Number of lines to show')
def logs(tail):
    """Show agent logs"""
    client = AgentClient()
    logs = client.get_logs(tail=tail)
    click.echo(logs)
```

### HTTP Client Implementation

```python
# sboxmgr/src/sboxmgr/cli/utils/agent_client.py
import requests
import json
from typing import Dict, Any

class AgentClient:
    def __init__(self, base_url: str = "http://localhost:8080", token: str = None):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()
        
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        response = self.session.get(f"{self.base_url}/api/v1/status")
        response.raise_for_status()
        return response.json()
    
    def start(self) -> None:
        """Start agent"""
        response = self.session.post(f"{self.base_url}/api/v1/start")
        response.raise_for_status()
    
    def stop(self) -> None:
        """Stop agent"""
        response = self.session.post(f"{self.base_url}/api/v1/stop")
        response.raise_for_status()
    
    def get_logs(self, tail: int = 100) -> str:
        """Get agent logs"""
        response = self.session.get(f"{self.base_url}/api/v1/logs", params={"tail": tail})
        response.raise_for_status()
        return response.text
```

## 🚀 ПЛАН РЕАЛИЗАЦИИ

### День 1-2: Schemas (частично готово)
- [x] Создать JSON схемы в sbox-common (agent-config готов)
- [x] Добавить валидацию в sboxagent
- [ ] Добавить валидацию в sboxmgr
- [ ] Создать примеры конфигурации

### День 3-4: Event Protocol
- [ ] Определить типы событий
- [ ] Создать event definitions
- [ ] Реализовать event converters
- [ ] Добавить event validation

### День 5-7: CLI Integration
- [ ] Реализовать HTTP клиент
- [ ] Добавить CLI команды
- [ ] Интегрировать с sboxagent API
- [ ] Добавить error handling

## 🧪 ТЕСТИРОВАНИЕ

### Schema Validation Tests
- [x] Valid configurations pass validation (agent-config)
- [x] Invalid configurations fail validation (agent-config)
- [ ] Schema evolution works correctly
- [ ] Cross-version compatibility maintained

### Event Protocol Tests
- [ ] Event serialization/deserialization works
- [ ] Event validation works correctly
- [ ] Event converters work properly
- [ ] Event format is consistent

### CLI Integration Tests
- [ ] CLI commands successfully call API
- [ ] Error handling works correctly
- [ ] Authentication works properly
- [ ] Logs are displayed correctly

## 🔍 КРИТЕРИИ УСПЕХА

### Функциональные
- [x] Все схемы валидируют конфигурации корректно (agent-config)
- [ ] Event protocol работает между проектами
- [ ] CLI команды управляют агентом
- [ ] HTTP API отвечает на запросы

### Технические
- [x] Схемы соответствуют JSON Schema Draft 7 (agent-config)
- [ ] Events имеют версионирование
- [ ] CLI имеет proper error handling
- [ ] HTTP client поддерживает retry logic

### Качественные
- [x] Документация схем полная (agent-config)
- [ ] Примеры конфигурации работают
- [ ] Тесты покрывают все сценарии
- [ ] Code review пройден

## 🔗 СВЯЗАННЫЕ ДОКУМЕНТЫ

- [Cross-Project Integration Plan](../integration-plan.md)
- [INTEGRATION-02: Runtime](phase-2-runtime.md)
- [sboxagent Phase 1C Plan](../../../../sboxagent/plans/phase-1c/plan.md)

## 📝 ЗАМЕТКИ

### Приоритеты
1. **Schemas** - основа для валидации (частично готово)
2. **Event Protocol** - основа для коммуникации
3. **CLI Integration** - основа для управления

### Риски
- Сложность синхронизации версий схем
- Performance impact от валидации
- Security considerations для HTTP API

### Альтернативы
- Если схемы сложны, можно начать с простой валидации
- Если events сложны, можно начать с простого logging

### Прогресс
- **Готово:** 30% (agent-config schema, api schema)
- **В работе:** 0%
- **Осталось:** 70% (event protocol, CLI integration)

---

**Следующий шаг:** [INTEGRATION-02: Runtime](phase-2-runtime.md) 