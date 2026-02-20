# Firebase to Supabase Auth Migration

The Django `migrate_firebase.py` ETL command handles all business logic migration (Farmers, Suppliers, Products, Finance). However, for security, Supabase Auth (`auth.users`) needs to be populated with the user credentials directly to retain the ability for those workers to login.

Here is the approach for Phase 5 to import Firebase Authentication Users into Supabase.

### 1. Export Firebase Auth Users (JSON/CSV)
You need to export your current Firebase users. The easiest way is via the Firebase CLI:
```bash
firebase auth:export users.json --format=json
```

### 2. Format & Import into Supabase
Supabase allows for programmatic user creation if you have the hashed passwords. If you don't care about their old passwords (e.g. forcing a password reset), you can simply insert them directly into the Postgres `auth.users` table using the Supabase SQL editor:

```sql
-- Replace the values below with the exported Firebase users
INSERT INTO auth.users (
  instance_id,
  id,
  aud,
  role,
  email,
  encrypted_password,
  email_confirmed_at,
  created_at,
  updated_at
) VALUES 
('00000000-0000-0000-0000-000000000000', 'firebase_uid_1', 'authenticated', 'authenticated', 'user1@greenfield.com', 'dummy_hash', NOW(), NOW(), NOW()),
('00000000-0000-0000-0000-000000000000', 'firebase_uid_2', 'authenticated', 'authenticated', 'user2@greenfield.com', 'dummy_hash', NOW(), NOW(), NOW());
```

> Note: Notice the `id` field maps to `firebase_uid_1`. It is CRUCIAL that the Supabase `auth.users.id` exactly matches the UID from Firebase Auth. Our Django `migrate_firebase.py` script relies on `User.username` matching this same UID to marry the Auth user to the `EmployeeProfile`!
