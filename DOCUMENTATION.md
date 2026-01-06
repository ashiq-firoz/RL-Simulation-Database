
# Asana Simulation Documentation

## Section A: Database Schema

This simulation uses a relational SQLite database designed to mirror Asana's core object model.

### Entity-Relationship Diagram (ERD)
*Note: This description corresponds to the `schema.sql` file.*

- **Workspaces**: The root container.
    - One-to-Many -> **Teams**
    - One-to-Many -> **Users**
    - One-to-Many -> **Tags**
- **Users**: Members of the workspace.
    - One-to-Many -> **Team Memberships** (Many-to-Many link to Teams)
    - One-to-Many -> **Tasks** (as Assignee or Creator)
- **Teams**: Functional groups.
    - One-to-Many -> **Projects**
- **Projects**: Collections of tasks.
    - One-to-Many -> **Sections**
    - One-to-Many -> **Tasks**
- **Tasks**: The unit of work.
    - Self-Reference -> **Parent Task** (Subtasks)
    - Many-to-Many -> **Tags**
    - One-to-Many -> **Stories** (Comments)
    - One-to-Many -> **Custom Field Values**

### Design Decisions
1.  **Custom Fields (EAV)**: Implemented using an Entity-Attribute-Value model (`custom_field_definitions`, `custom_field_values`) to support Asana's flexible per-project field schema.
2.  **Task Hierarchy**: Subtasks are modeled in the same `tasks` table using a self-referencing FK `parent_task_id`, allowing infinite nesting depth.
3.  **UUIDs**: All primary keys are UUIDv4 (`TEXT`) to mimic Asana's global ID system and allow distributed generation.

---

## Section B: Seed Data Methodology

### 1. Data Sources
- **Users**: Generated using `Faker` library to provide realistic names, emails, and avatars.
- **Job Titles**: Weighted distribution based on a typical SaaS org structure (40% Engineering/Product, 30% Sales/Marketing, 30% Ops).
- **Project Names**: Template-based generation derived from common industry patterns (e.g., "Q3 Roadmap", "Website Redesign").
- **Task Names**: Hybrid approach:
    - **Templates**: High-frequency patterns like "[Auth] - Fix login".
    - **LLM**: Optional integration with Google Gemini to generate context-aware task names and rich text descriptions.

### 2. Distribution Strategy
| Table | Strategy | Justification |
|Ref|---|---|
| **Users** | Linear Growth + Noise | Simulates company hiring ramp over 5 years. |
| **Tasks** | Per-Project Distribution | 10-30 tasks per project match typical "active" project sizes. |
| **Dates** | Temporal Integrity | `created_at` < `completed_at` enforced. Dates exclude future (unless due dates). |
| **Status** | Weighted Random | 15% Completed, 50% On Track, etc. reflects a snapshot of an active workspace. |

### 3. LLM Integration
When an API key is present (`GEMINI_API_KEY`), the system enriches task descriptions and comments using `gemini-2.0-flash-exp`.
- **Prompt**: "Write a 2 sentence description for this task"
- **Temperature**: 0.7 (for variety)
- **Fallback**: Pre-written string templates are used if the API is unavailable.
