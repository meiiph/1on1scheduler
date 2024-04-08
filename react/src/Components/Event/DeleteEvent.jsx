import React from 'react';
import { useHistory } from 'react-router-dom';

const DeleteEvent = ({ eventId }) => {
  const history = useHistory();

  const handleDelete = async () => {
    try {
      const response = await fetch(`/calendars/cancel_event/${eventId}/`, {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
      });
      if (response.ok) {
        alert('Event deleted successfully.');
        history.push('/view_events'); // Redirect to event list page
      } else {
        throw new Error('Failed to delete event.');
      }
    } catch (error) {
      console.error('Error deleting event:', error);
      alert('Failed to delete event.');
    }
  };

  return (
    <div>
      <h2>Delete Event</h2>
      <button onClick={handleDelete}>Delete Event</button>
    </div>
  );
};

export default DeleteEvent;
