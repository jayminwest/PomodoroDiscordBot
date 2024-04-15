from config import supabase

def add_time_tracking_row(ctx, time_in):
    """
    Add a new row to the time_tracking table.

    Parameters:
    ctx (Context): The context of the command invocation.
    time_in (datetime): The time the user started tracking.

    Returns:
    None
    """
    try:
        supabase.table("time_tracking").insert({"user_id": str(ctx.author.id), "time_in": time_in}).execute()
    except Exception as e:
        print(f"Error adding time tracking row: {str(e)}")

def update_time_tracking_row(ctx, time_in, time_out, duration):
    """
    Update the time_out and duration columns of the latest row.

    Parameters:
    ctx (Context): The context of the command invocation.
    time_in (datetime): The time the user started tracking.
    time_out (datetime): The time the user stopped tracking.
    duration (int): The duration of the tracking session.

    Returns:
    None
    """
    try:
        supabase.table("time_tracking").update({"time_out": time_out.strftime("%Y-%m-%dT%H:%M:%S"), "duration": duration}).eq("user_id", str(ctx.author.id)).eq("time_in", time_in).execute()
    except Exception as e:
        print(f"Error updating time tracking row: {str(e)}")

def get_data(ctx, select, start_date=None, end_date=None):
    """
    Get data from the time_tracking table.

    Parameters:
    ctx (Context): The context of the command invocation.
    select (str): The column(s) to select.
    start_date (datetime): The start date of the range to query. Defaults to None.
    end_date (datetime): The end date of the range to query. Defaults to None.

    Returns:
    list: A list of dictionaries containing the selected data.
    """
    try:
        if start_date is None and end_date is None:
            data = supabase.table("time_tracking").select(select).eq("user_id", str(ctx.author.id)).order("time_in", desc=True).limit(1).execute()
        else:
            data = supabase.table("time_tracking").select(select).eq("user_id", str(ctx.author.id)).gte("time_in", start_date).lte("time_in", end_date).execute()
        return data
    except Exception as e:
        print(f"Error getting data: {str(e)}")
        return []