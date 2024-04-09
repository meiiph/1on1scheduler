import React, { useState } from 'react';
import { TOKEN } from "../../constants/index";

const AddAttendee = ({ eventId }) => {
  const [userId, setUserId] = useState('');

  const handleAddAttendee = async () => {
    try {
      const response = await fetch(`/calendars/add_attendee/${eventId}/${userId}/`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ` + TOKEN,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        alert('Attendee added successfully.');
        // Refresh event details or update state as needed
      } else {
        throw new Error('Failed to add attendee.');
      }
    } catch (error) {
      console.error('Error adding attendee:', error);
      alert('Failed to add attendee.');
    }
  };

  return (
    <div>
      <h2>Add Attendee</h2>
      <input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} placeholder="User ID" />
      <button onClick={handleAddAttendee}>Add Attendee</button>
    </div>
  );
};

export default AddAttendee;
