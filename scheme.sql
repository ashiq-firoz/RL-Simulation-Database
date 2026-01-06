PRAGMA foreign_keys = ON;

-- Core Organization Entities
CREATE TABLE workspaces (
    workspace_id TEXT PRIMARY KEY, -- UUID
    name TEXT NOT NULL,
    domain TEXT, -- e.g., 'acme-saas.com'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    job_title TEXT, -- Critical for 'Realistic Data' (e.g., "Senior DevOps Engineer")
    avatar_url TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id)
);

CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL, -- e.g., "Growth Marketing", "Core Infrastructure"
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id)
);

-- Many-to-Many: Users belong to multiple teams
CREATE TABLE team_memberships (
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT DEFAULT 'member', -- 'member', 'admin'
    joined_at TIMESTAMP NOT NULL,
    PRIMARY KEY (team_id, user_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


-- Project Management Structure
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    owner_id TEXT, -- Project lead
    name TEXT NOT NULL, -- e.g., "Q3 Mobile App Launch"
    description TEXT,
    status TEXT CHECK(status IN ('on_track', 'at_risk', 'off_track', 'on_hold', 'completed')),
    due_date DATE,
    created_at TIMESTAMP NOT NULL,
    archived BOOLEAN DEFAULT 0,
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL, -- e.g., "Backlog", "In Review", "Done"
    order_index INTEGER NOT NULL, -- To maintain visual order on the board
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);


-- 3. The Work Unit (Tasks)
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT, -- Nullable because subtasks might not link directly to a project in some views, but usually do.
    section_id TEXT, -- The column the task sits in
    parent_task_id TEXT, -- Self-reference for Subtasks
    assignee_id TEXT,
    creator_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT, -- Rich text content simulation
    priority TEXT CHECK(priority IN ('low', 'medium', 'high', NULL)), -- Built-in priority, separate from custom fields
    due_date DATE,
    start_date DATE,
    completed BOOLEAN DEFAULT 0,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id),
    FOREIGN KEY (creator_id) REFERENCES users(user_id)
);


-- 4. Social & Metadata
CREATE TABLE stories (
    story_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL, -- Who wrote the comment or triggered the system event
    text TEXT, -- The comment content
    type TEXT CHECK(type IN ('comment', 'system')) DEFAULT 'comment', -- 'system' for "User X changed due date"
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id)
);

CREATE TABLE task_tags (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);


-- Custom Fields System (EAV Model)
-- Definition: What is the field? (e.g., "Story Points", "Vendor")
CREATE TABLE custom_field_definitions (
    field_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT CHECK(type IN ('text', 'number', 'enum', 'date', 'boolean')),
    description TEXT,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id)
);

-- Options: If type is 'enum', what are the dropdown options?
CREATE TABLE custom_field_options (
    option_id TEXT PRIMARY KEY,
    field_id TEXT NOT NULL,
    value TEXT NOT NULL, -- e.g., "High", "Low", "Critical"
    color TEXT,
    order_index INTEGER,
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id)
);

-- Association: Which projects use which fields?
CREATE TABLE project_custom_fields (
    project_id TEXT NOT NULL,
    field_id TEXT NOT NULL,
    PRIMARY KEY (project_id, field_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id)
);

-- Values: The actual data for a task
CREATE TABLE custom_field_values (
    value_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    field_id TEXT NOT NULL,
    
    -- We store the value in the column matching the type. 
    -- Application logic must handle which one to read.
    value_text TEXT,
    value_number REAL,
    value_date TIMESTAMP,
    value_enum_option_id TEXT, -- FK to options table if it's a dropdown
    
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id),
    FOREIGN KEY (value_enum_option_id) REFERENCES custom_field_options(option_id)
);