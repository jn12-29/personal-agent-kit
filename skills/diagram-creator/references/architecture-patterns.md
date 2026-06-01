# Architecture Diagram Patterns

Use these patterns as starting points, not as filler. Replace every label and edge with source-grounded project facts.

## C4-Style Context

```mermaid
flowchart LR
    User[User or actor] --> System[System under design]
    System --> External[External system]
```

Use for scope, actors, and external dependencies. Do not include internal modules.

## Component Or Container

```mermaid
flowchart TB
    subgraph System
        API[API layer]
        Worker[Worker]
        Store[(Data store)]
    end

    API --> Worker
    Worker --> Store
```

Use for internal responsibilities and dependencies. Keep deployment nodes out unless they are the point of the diagram.

PlantUML is a better fit when the component view needs UML package notation:

```plantuml
@startuml
package "System" {
  [API layer] --> [Worker]
  [Worker] --> database "Data store" as Store
}
@enduml
```

## Sequence

```mermaid
sequenceDiagram
    actor User
    participant Client
    participant API
    participant Store

    User->>Client: Start action
    Client->>API: Request
    API->>Store: Read or write
    Store-->>API: Result
    API-->>Client: Response
```

Use for one scenario. Avoid branching into multiple unrelated flows.

## Data Flow

```mermaid
flowchart LR
    Source[Source] --> Transform[Transform]
    Transform --> Store[(Store)]
    Store --> Consumer[Consumer]
```

Use for pipelines, transformations, and ownership of derived data.

## Deployment

```mermaid
flowchart TB
    subgraph Runtime
        App[App service]
        Job[Background job]
    end

    subgraph Managed
        DB[(Database)]
        Queue[Queue]
    end

    App --> DB
    App --> Queue
    Queue --> Job
```

Use for runtime placement, managed services, networks, and operational dependencies.

## Data Model

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
```

Use ER diagrams for persisted entities and cardinality. Use class diagrams for code types and inheritance.

## Class Or UML Model

```plantuml
@startuml
class Service {
  +handle(request)
}
class Repository {
  +save(entity)
}
Service --> Repository
@enduml
```

Use for code ownership, inheritance, interfaces, and type relationships. Do not use it to describe runtime deployment.

## State

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted
    Submitted --> Approved
    Submitted --> Rejected
```

Use for lifecycle states and allowed transitions. Keep guards and side effects short.
