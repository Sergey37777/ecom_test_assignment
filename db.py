def initialize_db(db):
    form_templates_table = db.table("form_templates")
    if not form_templates_table.all():
        form_templates_table.insert_multiple([
            {
                'name': 'Order Form',
                'fields': [
                    {'field_name': 'email', 'field_type': 'email'},
                    {'field_name': 'phone', 'field_type': 'phone'}
                ]
            },
            {
                'name': 'Registration Form',
                'fields': [
                    {'field_name': 'email', 'field_type': 'email'},
                    {'field_name': 'user_name', 'field_type': 'text'},
                    {'field_name': 'registration_date', 'field_type': 'date'}
                ]
            },
            {
                'name': 'Feedback Form',
                'fields': [
                    {'field_name': 'feedback', 'field_type': 'text'},
                    {'field_name': 'email', 'field_type': 'email'}
                ]
            },
            {
                'name': 'Application Form',
                'fields': [
                    {'field_name': 'application_id', 'field_type': 'text'},
                    {'field_name': 'submission_date', 'field_type': 'date'}
                ]
            }
        ])


def cleanup_db(db_file_path=None):
    if db_file_path.exists():
        db_file_path.unlink()