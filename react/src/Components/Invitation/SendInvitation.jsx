import React, { useState, useEffect } from 'react';

const SendInvitation = ({}) => {
  const [formData, setFormData] = useState({ username: '', type: '', calendarId: '' });
  const [calendars, setCalendars] = useState([]);

  useEffect(() => {
    const fetchCalendars = async () => {
      try {
        const ownResponse = await fetch(`/api/calendars/all`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            // 'Authorization': `Bearer ${YOUR_AUTH_TOKEN}`,
          },
          body: JSON.stringify({ type: 'own' }), // Set the type as 'own'
        });

        const hostResponse = await fetch(`/api/calendars/all`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            // 'Authorization': `Bearer ${YOUR_AUTH_TOKEN}`,
          },
          body: JSON.stringify({ type: 'host' }), // Set the type as 'host'
        });

        if (ownResponse.ok && hostResponse.ok) {
          const ownData = await ownResponse.json();
          const hostData = await hostResponse.json();

          // Combine calendars from both responses
          const combinedCalendars = [...ownData, ...hostData];

          setCalendars(combinedCalendars);
          if (combinedCalendars.length > 0) {
            setFormData({ ...formData, calendarId: combinedCalendars[0].id });
          }
        } else {
          throw new Error('Failed to fetch calendars.');
        }
      } catch (error) {
        console.error('Error fetching calendars:', error);
      }
    };
    fetchCalendars();
  }, []); // Empty dependency array to fetch calendars only once

  const handleChange = event => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async event => {
    event.preventDefault();
    try {
      const response = await fetch(`/api/invitations/${formData.calendarId}/send`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // 'Authorization': `Bearer ${YOUR_AUTH_TOKEN}`,
        },
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        alert(`Invitation sent successfully to ${formData.username}`);
        setFormData({ username: '', type: '', calendarId: '' }); // Reset form data after successful submission
      } else {
        throw new Error('Failed to send invitation.');
      }
    } catch (error) {
      console.error('Error sending invitation:', error);
      alert('Failed to send invitation.');
    }
  };

  return (
    <div>
      <h2>Send Invitation</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input type="text" name="username" value={formData.username} onChange={handleChange} />
        </label>
        <label>
          Type:
          <select name="type" value={formData.type} onChange={handleChange}>
            <option value="">Select Type</option>
            <option value="guest">Guest</option>
            <option value="host">Host</option>
            <option value="super_host">Super Host</option>
          </select>
        </label>
        <label>
          Calendar:
          <select name="calendarId" value={formData.calendarId} onChange={handleChange}>
            {calendars.map(calendar => (
              <option key={calendar.id} value={calendar.id}>{calendar.name}</option>
            ))}
          </select>
        </label>
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default SendInvitation;
