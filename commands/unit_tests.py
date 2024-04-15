import datetime
from unittest.mock import MagicMock, patch
from datetime import datetime
import stop, pomodoro

@patch('bot.add_time_tracking_row')
async def test_pomodoro(mock_add_time_tracking_row):
    # Create a fake Context object
    ctx = MagicMock()
    
    now_mock = MagicMock(return_value=datetime.datetime(2022, 1, 1))
    with patch('datetime.datetime', now_mock) as _:
        await pomodoro(ctx)
        
        expected_data = {'user_id': str(ctx.author.id),
                         'time_in': now_mock.return_value.strftime("%Y-%m-%dT%H:%M:%S")}
        mock_add_time_tracking_row.assert_called_once_with(expected_data)

# Test case when exception occurs during execution
@patch('bot.convert_seconds', side_effect=ValueError("Test error"))
async def test_pomodoro_exception(self, _):
    # Create a fake Context object
    ctx = MagicMock()

    try:
        await self.pomodoro(ctx)
    except Exception as e:
        assert isinstance(e, ValueError)


@patch('bot.get_time_tracking_data')
@patch('bot.update_time_tracking_row')
def test_stop(mock_update_time_tracking_row, mock_get_time_tracking_data):
    # Mock data returned by supabase queries
    mock_data = [{'time_in': '2022-01-01T00:00:00'}]
    
    # Set up mocks
    mock_ctx = MagicMock()
    mock_ctx.author.id = 1234
    
    mock_send = MagicMock(return_value=None)
    type(mock_ctx).send = mock_send
    
    mock_tasks_cancel = MagicMock(return_value=None)

    # Patch functions
    with patch('tasks', new_callable=list) as mock_task_list:
        mock_task_list.append(MagicMock(cancel=mock_tasks_cancel))
        
        stop(mock_ctx)
        
        assert len(mock_task_list) == 0
        
        # Check if send method has been called correctly
        expected_message = f"Time tracking stopped at {datetime.datetime.now()}..."
        mock_send.assert_called_once_with(expected_message)
        
        # Assert other methods have been called as well
        mock_get_time_tracking_data.assert_called_once_with(mock_ctx)
        mock_update_time_tracking_row.assert_called_once()

# # Test case when exception occurs during execution
# @patch('bot.convert_seconds', side_effect=ValueError("Test error"))
# async def test_stop_exception(self, _):
#     # Create a fake Context object
#     mock_ctx = MagicMock()
    
#     # Call the stop function which should raise an Exception
#     await self.stop(mock_ctx)
    
#     # Check whether correct message sent or not after catching exception 
#     mock_ctx.send.assert_called_once_with(f"Error: {'Test error'}")