from config import supabase

def add_time_tracking_row(user_id, start_time):
    """
    Add a new row to the time_tracking table.

    Parameters:
    user_id (int): The ID of the user.
    start_time (datetime): The time the user started tracking.

    Returns:
    None
    """
    try:
        supabase.table("time_tracking").insert({"user_id": str(user_id), "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S")}).execute()
    except Exception as e:
        print(f"Error adding time tracking row: {str(e)}")

def update_time_tracking_row(user_id, start_time, end_time, duration):
    """
    Update the end_time and duration columns of the latest row.

    Parameters:
    user_id (int): The ID of the user.
    start_time (datetime): The time the user started tracking.
    end_time (datetime): The time the user stopped tracking.
    duration (int): The duration of the tracking session.

    Returns:
    None
    """
    try:
        supabase.table("time_tracking").update({"end_time": end_time.strftime("%Y-%m-%dT%H:%M:%S"), "duration": duration}).eq("user_id", str(user_id)).eq("start_time", start_time).execute()
    except Exception as e:
        print(f"Error updating time tracking row: {str(e)}")

def update_paused_at(user_id, start_time, paused_at):
    """
    Update the paused_at column of the latest row.

    Parameters:
    user_id (int): The ID of the user.
    start_time (datetime): The time the user started tracking.
    paused_at (datetime): The time the user paused tracking.

    Returns:
    None
    """
    try:
        supabase.table("time_tracking").update({"paused_at": paused_at.strftime("%Y-%m-%dT%H:%M:%S")}).eq("user_id", str(user_id)).eq("start_time", start_time).execute()
    except Exception as e:
        print(f"Error updating paused_at: {str(e)}")

def update_resumed_at(user_id, start_time, resumed_at):
    """
    Update the resumed_at column of the latest row.

    Parameters:
    user_id (int): The ID of the user.
    start_time (datetime): The time the user started tracking.
    resumed_at (datetime): The time the user resumed tracking.

    Returns:
    None
    """
    try:
        supabase.table("time_tracking").update({"resumed_at": resumed_at.strftime("%Y-%m-%dT%H:%M:%S")}).eq("user_id", str(user_id)).eq("start_time", start_time).execute()
    except Exception as e:
        print(f"Error updating resumed_at: {str(e)}")

def get_data(user_id, select, start_date=None, end_date=None):
    """
    Get data from the time_tracking table.

    Parameters:
    user_id (int): The ID of the user.
    select (str): The column(s) to select.
    start_date (datetime): The start date of the range to query. Defaults to None.
    end_date (datetime): The end date of the range to query. Defaults to None.

    Returns:
    list: A list of dictionaries containing the selected data.
    """
    try:
        if start_date is None and end_date is None:
            data = supabase.table("time_tracking").select(select).eq("user_id", str(user_id)).order("start_time", desc=True).limit(1).execute()
        else:
            data = supabase.table("time_tracking").select(select).eq("user_id", str(user_id)).gte("start_time", start_date).lte("start_time", end_date).execute()
        return data
    except Exception as e:
        print(f"Error getting data: {str(e)}")
        return []