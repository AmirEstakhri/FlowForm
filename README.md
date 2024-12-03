# 📝 FlowForm

**FlowForm** is a dynamic and collaborative platform for managing workflows, handling form submissions, assigning users/managers, and streamlining the verification process. Designed for teams and organizations, it supports multi-user role functionality and customizable form assignments to enhance task delegation and approval workflows.

---

## 🚀 Features:
### 🔹 User Roles:
1. **Normal User**:
   - Create forms and send them to the manager of their group.
   - Assign forms to other users within the same group, provided they have the required sub-role.
   - Track the status of sent forms (e.g., pending, verified).
   - Edit forms before verification but cannot modify them once verified.
   - View submission logs, including the submission date and sender details.
   - Cannot assign forms to admins or managers outside their group.

2. **Manager**:
   - Verify forms submitted by users within their group.
   - Assign forms to other managers or admins for additional verification if needed.
   - Log every verification action, capturing the verifier's name and timestamp.
   - Assign other managers to a form to share verification responsibilities.
   - Manage forms within their assigned group.

3. **Admin**:
   - Full control over the system:
     - Create, edit, and delete users.
     - Manage groups by assigning users and managers.
     - Edit or tag forms as needed.
     - Access logs for all forms and verification processes.
   - Oversee and manage the workflow across all groups.

---

## 🛠️ Technologies Used:
- **Backend**: Python (Django framework)  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: SQLite (customizable to PostgreSQL or others)  

---

