import React, { useState } from 'react';
import { TOKEN } from "../../constants/index";

const RespondEvent = ({ eventId }) => {
  const [status, setStatus] = useState('');
  const [availability, setAvailability] = useState([]);

  const handleRespond = async () => {
    try {
      const response = await fetch(`/api/events/${eventId}/respond/`, {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ` + TOKEN,
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({
          status: status,
          availability: availability
        })
      });
      if (response.ok) {
        const eventData = await response.json();
        console.log('Response:', eventData);
      } else {
        throw new Error('Failed to respond to event.');
      }
    } catch (error) {
      console.error('Error responding to event:', error);
      alert('Failed to respond to event.');
    }
  };

  return (
    <div>
      <h2>Respond to Event</h2>
      <select value={status} onChange={(e) => setStatus(e.target.value)}>
        <option value="">Select Response</option>
        <option value="accept">Accept</option>
        <option value="decline">Decline</option>
      </select>
      {status === 'accept' && (
        <div>
          <h3>Availability</h3>
          <input type="datetime-local" value={availability[0]} onChange={(e) => setAvailability([e.target.value, availability[1]])} />
          <input type="datetime-local" value={availability[1]} onChange={(e) => setAvailability([availability[0], e.target.value])} />
        </div>
      )}
      <button onClick={handleRespond}>Respond</button>
    </div>
  );
};

export default RespondEvent;
