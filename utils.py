from config import supabase

def convert_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def add_time_tracking_row(ctx, time_in):
    data = supabase.table("time_tracking").insert({"user_id": ctx.author.id, "time_in": time_in.strftime("%Y-%m-%d %H:%M:%S")}).execute()