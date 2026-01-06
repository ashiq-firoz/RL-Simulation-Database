
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, get_weighted_choice
import random

def generate_custom_fields(conn, workspace_id):
    print("Generating custom fields...")
    cursor = conn.cursor()
    
    # 1. Definitions
    fields = [
        ("Story Points", "number", "Engineering"),
        ("Priority Level", "enum", "All"),
        ("Estimated Hours", "number", "Engineering"),
        ("Vendor Name", "text", "Operations"),
        ("Customer Segment", "enum", "Product")
    ]
    
    field_map = {} # name -> id
    
    for name, ftype, cat in fields:
        fid = generate_uuid()
        cursor.execute("INSERT INTO custom_field_definitions (field_id, workspace_id, name, type) VALUES (?, ?, ?, ?)", 
                       (fid, workspace_id, name, ftype))
        field_map[name] = fid
        
        # Options for Enums
        if ftype == 'enum':
            if name == "Priority Level":
                opts = ["P0", "P1", "P2", "P3"]
            else: # Customer Segment
                opts = ["SMB", "Enterprise", "Mid-Market"]
            
            for idx, val in enumerate(opts):
                oid = generate_uuid()
                cursor.execute("INSERT INTO custom_field_options (option_id, field_id, value, order_index) VALUES (?, ?, ?, ?)",
                               (oid, fid, val, idx))
                               
    conn.commit()
    
    # 2. Assign to Projects
    print("Associating fields with projects...")
    cursor.execute("SELECT project_id, name FROM projects")
    projects = cursor.fetchall()
    
    project_fields = [] # (pid, fid)
    
    for proj in projects:
        pid = proj['project_id']
        pname = proj['name']
        
        # Heuristic assignment
        assigned_fields = []
        if "Roadmap" in pname or "Refactor" in pname or "Bug" in pname:
           assigned_fields.append(field_map["Story Points"])
           assigned_fields.append(field_map["Priority Level"])
        elif "Sales" in pname or "Lead" in pname:
           assigned_fields.append(field_map["Customer Segment"])
        else:
           assigned_fields.append(field_map["Priority Level"])
           
        for fid in assigned_fields:
            project_fields.append((pid, fid))
            
            # 3. Generate Values for Tasks in this Project
            cursor.execute("SELECT task_id FROM tasks WHERE project_id = ?", (pid,))
            tasks = cursor.fetchall()
            
            # Fetch options if enum
            options = []
            cursor.execute("SELECT option_id FROM custom_field_options WHERE field_id = ?", (fid,))
            options = [r[0] for r in cursor.fetchall()]
            
            task_values = []
            for t in tasks:
                 tid = t['task_id']
                 # Simple random assignment
                 val_id = generate_uuid()
                 
                 v_text, v_num, v_enum = None, None, None
                 if fid == field_map.get("Story Points"):
                     v_num = random.choice([1, 2, 3, 5, 8, 13])
                 elif fid == field_map.get("Priority Level") or fid == field_map.get("Customer Segment"):
                     v_enum = random.choice(options)
                 
                 # Only insert if we have a value
                 if v_num or v_enum:
                     task_values.append((val_id, tid, fid, v_num, v_enum))
            
            if task_values:
                cursor.executemany("""
                    INSERT INTO custom_field_values (value_id, task_id, field_id, value_number, value_enum_option_id)
                    VALUES (?, ?, ?, ?, ?)
                """, task_values)
                
    cursor.executemany("INSERT INTO project_custom_fields (project_id, field_id) VALUES (?, ?)", project_fields)
    conn.commit()
    print("Custom fields generation complete.")
