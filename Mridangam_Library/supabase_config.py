from supabase import create_client

SUPABASE_URL = "https://goszsnddiyhzyhcnmrtl.supabase.co"

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdvc3pzbmRkaXloenloY25tcnRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI0ODgyODgsImV4cCI6MjA5ODA2NDI4OH0.jB1vSYwf867nRVZExKrnuUFBsGPEAyPTPGWrhvQDj9M"

supabase = create_client(
SUPABASE_URL,
SUPABASE_KEY
)

