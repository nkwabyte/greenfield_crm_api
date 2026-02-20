import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from accounts.models import User, EmployeeProfile
from farmers.models import Farmer, FarmerGroup
from inventory.models import Supplier, Product
from finances.models import Transaction

class Command(BaseCommand):
    help = 'Mirrors Firebase Firestore data to Supabase PostgreSQL'

    def handle(self, *args, **options):
        # 1. Initialize Firebase
        cred_path = os.environ.get('FIREBASE_CREDENTIALS_PATH', 'firebase-adminsdk.json')
        if not os.path.exists(cred_path):
            self.stdout.write(self.style.ERROR(f"Firebase credentials not found at {cred_path}."))
            self.stdout.write(self.style.WARNING("Please download your serviceAccountKey from Firebase Console -> Project Settings -> Service Accounts -> Generate New Private Key."))
            return

        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        self.stdout.write(self.style.SUCCESS('Successfully connected to Firebase Firestore.'))

        # 2. Extract and Transform
        self.migrate_employees(db)
        self.migrate_farmers(db)
        self.migrate_suppliers(db)
        self.migrate_products(db)
        self.migrate_transactions(db)

        self.stdout.write(self.style.SUCCESS('\n================================='))
        self.stdout.write(self.style.SUCCESS('Data Migration Complete!'))
        self.stdout.write(self.style.SUCCESS('=================================\n'))

    def migrate_employees(self, db):
        self.stdout.write(self.style.WARNING('\nMigrating Employees...'))
        users_ref = db.collection('employees').stream()
        for doc in users_ref:
            data = doc.to_dict()
            self.stdout.write(f" -> Found employee: {data.get('name')}")
            
            # Since Supabase handles passwords/auth, we just generate users 
            # and map them to EmployeeProfile.
            # In a real scenario, you'd use Supabase Admin API to create auth accounts.
            
            user, created = User.objects.get_or_create(
                username=doc.id, # Map Firebase UID to Django Username
                defaults={
                    'email': data.get('email'),
                    'role': 'EMPLOYEE',
                    'is_active': True
                }
            )

            EmployeeProfile.objects.update_or_create(
                id=doc.id,
                defaults={
                    'user': user,
                    'name': data.get('name', ''),
                    'phone': data.get('phone', ''),
                    'role_title': data.get('role', 'Field Agent'),
                    'salary': data.get('salary', 0),
                    'is_verified': data.get('isVerified', False),
                    'status': data.get('status', 'Active'),
                }
            )
        self.stdout.write(self.style.SUCCESS('Employees migration completed.'))

    def migrate_farmers(self, db):
        self.stdout.write(self.style.WARNING('\nMigrating Farmers...'))
        farmers_ref = db.collection('farmers').stream()
        for doc in farmers_ref:
            data = doc.to_dict()
            Farmer.objects.update_or_create(
                id=doc.id,
                defaults={
                    'name': data.get('name', ''),
                    'gender': data.get('gender'),
                    'region': data.get('region'),
                    'district': data.get('district'),
                    'society': data.get('society'),
                    'community': data.get('community'),
                    'contact': data.get('contact'),
                    'age': data.get('age'),
                    'farm_size': data.get('farmSize'),
                    'status': data.get('status'),
                }
            )
        self.stdout.write(self.style.SUCCESS('Farmers migration completed.'))

    def migrate_suppliers(self, db):
        self.stdout.write(self.style.WARNING('\nMigrating Suppliers...'))
        suppliers_ref = db.collection('suppliers').stream()
        for doc in suppliers_ref:
            data = doc.to_dict()
            Supplier.objects.update_or_create(
                id=doc.id,
                defaults={
                    'name': data.get('name', ''),
                    'contact_person': data.get('contactPerson', ''),
                    'email': data.get('email', ''),
                    'phone': data.get('phone', ''),
                }
            )
        self.stdout.write(self.style.SUCCESS('Suppliers migration completed.'))

    def migrate_products(self, db):
        self.stdout.write(self.style.WARNING('\nMigrating Products...'))
        products_ref = db.collection('products').stream()
        for doc in products_ref:
            data = doc.to_dict()
            supplier_id = data.get('supplierId')
            
            # Resolve supplier relation
            try:
                supplier = Supplier.objects.get(id=supplier_id)
            except Supplier.DoesNotExist:
                supplier = None
                self.stdout.write(self.style.ERROR(f"!!! Skipping Product '{data.get('name')}', Supplier ID {supplier_id} not found."))
                continue

            Product.objects.update_or_create(
                id=doc.id,
                defaults={
                    'name': data.get('name', ''),
                    'category': data.get('category', ''),
                    'supplier': supplier,
                    'quantity': data.get('quantity', 0),
                    'price': data.get('price', 0),
                }
            )
        self.stdout.write(self.style.SUCCESS('Products migration completed.'))

    def migrate_transactions(self, db):
        self.stdout.write(self.style.WARNING('\nMigrating Transactions...'))
        tx_ref = db.collection('finances').stream()
        for doc in tx_ref:
            data = doc.to_dict()
            
            # Map Firestore Timestamp to Python Date
            date_field = data.get('date')
            try:
                tx_date = date_field.date() if hasattr(date_field, 'date') else None
            except:
                tx_date = None

            if not tx_date:
                 self.stdout.write(self.style.ERROR(f"!!! Skipping Transaction '{doc.id}', missing date."))
                 continue

            Transaction.objects.update_or_create(
                id=doc.id,
                defaults={
                    'type': data.get('type', 'Expense'),
                    'category': data.get('category', ''),
                    'description': data.get('description', ''),
                    'amount': data.get('amount', 0),
                    'date': tx_date,
                    'employee_name': data.get('employee', ''),
                }
            )
        self.stdout.write(self.style.SUCCESS('Transactions migration completed.'))
