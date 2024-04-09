import React from 'react';
import { TOKEN } from "../../constants/index";

const RequestJoin = ({ eventId }) => {
  const handleRequestJoin = async () => {
    try {
      const response = await fetch(`/calendars/request_join/${eventId}/`, {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ` + TOKEN,
            'Content-Type': 'application/json'
          }
      });
      if (response.ok) {
        alert('Request sent successfully.');
        } else {
        throw new Error('Failed to send request.');
      }
    } catch (error) {
      console.error('Error sending request:', error);
      alert('Failed to send request.');
    }
  };

  return (
    <div>
      <h2>Request Join</h2>
      <button onClick={handleRequestJoin}>Request Join</button>
    </div>
  );
};

export default RequestJoin;
