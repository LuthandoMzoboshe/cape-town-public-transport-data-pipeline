# Cape Town Public Transport ER Diagram

```mermaid
erDiagram

    TRANSPORT_MODE ||--o{ ROUTE : has

    TRANSPORT_MODE {
        int mode_id PK
        string mode_name
    }

    ROUTE {
        int route_id PK
        int mode_id FK
        int source_id
        string route_name
        string route_number
        string route_type
        string status
        string origin
        string destination
        float length_m
    }

    BUS_STOP {
        int stop_id PK
        int source_id
        string name
        string type
        string status
        string description
    }

    RAIL_LINE {
        int line_id PK
        int source_id
        string name
        string usage
        string type
        float length_m
    }

    RAIL_STATION {
        int station_id PK
        int source_id
        string name
    }