# Supabase Python Template

This template provides a quick start for integrating Supabase with Python applications using the official Supabase Python SDK. All API functions are pre-implemented for immediate use in your projects, with seamless Django integration.

## Features

- Complete Supabase SDK integration
- Pre-implemented CRUD operations for database tables
- Authentication methods (sign up, sign in, magic link, etc.)
- Storage operations for file uploads and downloads
- Real-time subscriptions
- Edge Functions support
- Ready-to-use test suite compatible with Django

## Requirements

- Python 3.7+
- Supabase project (create one at [supabase.com](https://supabase.com))

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/supabase-python-template.git
   cd supabase-python-template 
   ```

2. Install the Supabase SDK:
   ```bash
   pip install supabase
   ```

3. Create a `.env` file in the project root with your Supabase credentials:
   ```
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   ```

## Quick Start

### Initialize Supabase Client

```python
from supabase_client import create_client

# Client is automatically initialized with environment variables
supabase = create_client()

# Or manually provide credentials
# supabase = create_client("YOUR_SUPABASE_URL", "YOUR_SUPABASE_KEY")
```

### Database Operations

```python
# Get all items from a table
data = supabase.table('table_name').select('*').execute()

# Get items with filtering
data = supabase.table('table_name').select('*').eq('column', 'value').execute()

# Insert data
data = supabase.table('table_name').insert({'column': 'value'}).execute()

# Update data
data = supabase.table('table_name').update({'column': 'new_value'}).eq('id', 1).execute()

# Delete data
data = supabase.table('table_name').delete().eq('id', 1).execute()
```

### Authentication

```python
# Sign up
user = supabase.auth.sign_up({
    "email": "example@email.com",
    "password": "example-password"
})

# Sign in
user = supabase.auth.sign_in_with_password({
    "email": "example@email.com",
    "password": "example-password"
})

# Sign in with magic link
supabase.auth.sign_in_with_otp({
    "email": "example@email.com"
})

# Sign out
supabase.auth.sign_out()

# Get user
user = supabase.auth.get_user()
```

### Storage

```python
# Upload file
result = supabase.storage.from_('bucket_name').upload(
    'file_path.txt',
    open('local_file.txt', 'rb'),
    {'content-type': 'text/plain'}
)

# Download file
data = supabase.storage.from_('bucket_name').download('file_path.txt')

# Get public URL
url = supabase.storage.from_('bucket_name').get_public_url('file_path.txt')

# List files
files = supabase.storage.from_('bucket_name').list()

# Remove file
supabase.storage.from_('bucket_name').remove(['file_path.txt'])
```

### Real-time Subscriptions

```python
def handle_broadcast(payload):
    print(payload)

# Subscribe to changes
subscription = supabase.table('table_name').on('INSERT', handle_broadcast).subscribe()

# Unsubscribe
supabase.remove_subscription(subscription)
```

### Edge Functions

```python
# Invoke an edge function
response = supabase.functions.invoke('function_name', {'data': 'value'})
```

## Django Integration

This template includes tests that work well with Django's testing framework. To use them:

1. Add the template to your Django project

2. Configure Supabase in your Django settings:
   ```python
   # settings.py
   SUPABASE_URL = 'your_supabase_project_url'
   SUPABASE_KEY = 'your_supabase_anon_key'
   ```

3. Run the included tests with Django's test runner:
   ```bash
   python manage.py test supabase_template
   ```

## Advanced Usage

### Using Row Level Security (RLS)

When using RLS policies in Supabase, you'll need to include the user's JWT token in your requests:

```python
# Sign in first
response = supabase.auth.sign_in_with_password({
    "email": "example@email.com",
    "password": "example-password"
})

# Now you can access tables with RLS policies
data = supabase.table('protected_table').select('*').execute()
```

### Handling PostgreSQL Functions

```python
# Call a PostgreSQL function
data = supabase.rpc('function_name', {'arg1': 'value1'}).execute()
```

### Foreign Table Joins

```python
# Query with joins
data = supabase.table('table_name').select('*, foreign_table(*)').execute()
```

## Error Handling

The template includes pre-configured error handling for common Supabase operations:

```python
try:
    data = supabase.table('table_name').select('*').execute()
    print(data)
except Exception as e:
    print(f"An error occurred: {e}")
```

## Environment Configuration

The template supports multiple environments through Django settings or environment variables:

```python
# In Django settings.py for different environments:
if DEBUG:
    SUPABASE_URL = 'development_url'
    SUPABASE_KEY = 'development_key'
else:
    SUPABASE_URL = 'production_url'
    SUPABASE_KEY = 'production_key'
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Python SDK Documentation](https://supabase.com/docs/reference/python/introduction)
- [GitHub Repository](https://github.com/supabase/supabase-py)