import React, { useState } from 'react';

const RemoveAttendee = ({ eventId }) => {
  const [userId, setUserId] = useState('');

  const handleRemoveAttendee = async () => {
    try {
      const response = await fetch(`/calendars/remove_attendee/${eventId}/${userId}/`, {
        method: 'PATCH',
        // Add authorization token if needed
      });
      if (response.ok) {
        alert('Attendee removed successfully.');
        // Refresh event details or update state as needed
      } else {
        throw new Error('Failed to remove attendee.');
      }
    } catch (error) {
      console.error('Error removing attendee:', error);
      alert('Failed to remove attendee.');
    }
  };

  return (
    <div>
      <h2>Remove Attendee</h2>
      <input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} placeholder="User ID" />
      <button onClick={handleRemoveAttendee}>Remove Attendee</button>
    </div>
  );
};

export default RemoveAttendee;
