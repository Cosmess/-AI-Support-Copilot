# Clean Architecture Diagram

```mermaid
flowchart TB
  P[Presentation]
  A[Application]
  D[Domain]
  I[Infrastructure]

  P --> A
  A --> D
  I --> D
```
