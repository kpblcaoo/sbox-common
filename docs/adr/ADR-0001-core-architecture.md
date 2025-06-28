# ADR-0001: Core Architecture and Component Roles

**Status:** Accepted  
**Date:** 2025-06-28  
**Authors:** kpblc, AI Assistant  

## Context

The subbox ecosystem consists of three main components:
- `sboxmgr` (Python) - configuration management CLI
- `sboxagent` (Go) - daemon for service management  
- `sbox-common` (JSON/schemas) - shared protocols

During development, architectural confusion arose about component roles, interfaces, and licensing compatibility. This ADR clarifies the correct architecture and responsibilities.

## Decision

### Component Roles

| Component | Primary Role | Language | License | Responsibilities |
|-----------|-------------|----------|---------|------------------|
| `sboxmgr` | Generator & CLI | Python | Apache-2.0 | Config generation, validation, CLI interface |
| `sboxagent` | Executor & Daemon | Go | GPL-3.0 | Config application, service management, monitoring |
| `sbox-common` | Protocols & Schemas | JSON | Apache-2.0 | Shared protocols, schemas, examples |

### Architecture Principles

1. **Single Responsibility**: Each component has ONE primary role
2. **JSON Interface**: All inter-component communication via JSON
3. **License Separation**: Clean boundaries prevent GPL "contamination"
4. **No Logic Duplication**: Configuration generation ONLY in sboxmgr

### Communication Protocol

```
sboxmgr → JSON → sboxagent → subbox clients
```

**Interface Examples:**
```bash
# Generate configuration
sboxmgr config generate --client=sing-box --output=json > config.json

# Apply configuration  
sboxagent apply --config=config.json --client=sing-box
```

### Dual-Path Architecture

#### Path A (Standalone):
```
systemd timer → sboxmgr → JSON files → subbox clients
```

#### Path B (Service Mode):
```
sboxagent → exec(sboxmgr) → JSON → sboxagent applies → subbox clients
```

#### Path C (Future Centralized):
```
central sboxmgr → HTTP/JSON → remote sboxagent → subbox clients
```

## Consequences

### Positive
- ✅ Clear separation of concerns
- ✅ License compatibility maintained
- ✅ No code duplication
- ✅ Scalable to centralized management
- ✅ Language-agnostic interface

### Negative
- ❌ CLI subprocess overhead in service mode
- ❌ JSON serialization/parsing overhead
- ❌ Potential process management complexity

### Rejected Alternatives

1. **sboxagent generates configs**: Would duplicate Python logic in Go
2. **sboxmgr manages clients directly**: Violates single responsibility
3. **Shared libraries**: License incompatibility (GPL + Apache)
4. **Direct Go-Python integration**: Technical complexity, license issues

## Implementation Guidelines

### sboxmgr Responsibilities
- Configuration generation for all subbox clients
- Input validation and sanitization
- CLI interface for manual operations
- JSON export functionality
- Schema compliance validation

### sboxagent Responsibilities
- JSON configuration import and parsing
- Subbox client lifecycle management (start/stop/restart)
- System service integration (systemd)
- Health monitoring and status reporting
- HTTP API for status queries (read-only)

### sbox-common Responsibilities
- JSON schema definitions
- Protocol specifications
- Shared data structures
- Example configurations
- Documentation

### Interface Contracts

#### Configuration Generation
```bash
sboxmgr config generate \
  --subscription=<url> \
  --client=<client_type> \
  --output=json \
  --validate
```

#### Configuration Application
```bash
sboxagent apply \
  --config=<json_file> \
  --client=<client_type> \
  --action=<deploy|rollback>
```

#### Status Queries
```bash
sboxagent status \
  --client=<client_type> \
  --format=json
```

## Migration Path

### Phase 1 (Current): Establish JSON Interface
- Standardize JSON output from sboxmgr
- Implement JSON input in sboxagent
- Define schemas in sbox-common

### Phase 2: Service Integration
- sboxagent calls sboxmgr CLI for generation
- Implement service management
- Add monitoring and health checks

### Phase 3: HTTP API Extension
- Add HTTP endpoints to sboxagent
- Implement centralized management
- Scale to multiple agents

## Compliance Notes

### License Compatibility
- **Process Boundary**: sboxagent (GPL-3.0) calls sboxmgr (Apache-2.0) as subprocess
- **No Code Sharing**: No shared libraries between GPL and Apache components
- **JSON Protocol**: License-neutral data exchange format

### Security Considerations
- JSON validation required on all boundaries
- Input sanitization in both components
- Secure subprocess execution
- Audit logging for configuration changes

## References

- [Subbox Ecosystem Overview](../README.md)
- [JSON Protocol Specification](../protocols/README.md)
- [License Compatibility Matrix](../legal/LICENSE-COMPATIBILITY.md)

---

**Next Review:** 2025-09-01  
**Supersedes:** None  
**Superseded by:** None 