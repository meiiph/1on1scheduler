import React, { useState, useEffect } from 'react';

const ViewEventsCalendar = ({ calendarId }) => {
  const [events, setEvents] = useState([]);
  const [status, setStatus] = useState('confirmed');

  useEffect(() => {
    const fetchCalendarEvents = async () => {
      try {
        const response = await fetch(`/api/events/list/${calendarId}/?status=${status}`);
        if (response.ok) {
          const data = await response.json();
          setEvents(data);
        } else {
          throw new Error('Failed to fetch calendar events.');
        }
      } catch (error) {
        console.error('Error fetching calendar events:', error);
      }
    };
    fetchCalendarEvents();
  }, [calendarId, status]);

  const handleChangeStatus = (e) => {
    setStatus(e.target.value);
  };

  return (
    <div>
      <h2>Calendar Events</h2>
      <div>
        <label>Status:</label>
        <select value={status} onChange={handleChangeStatus}>
          <option value="confirmed">Confirmed</option>
          <option value="unconfirmed">Unconfirmed</option>
        </select>
      </div>
      <ul>
        {events.map(event => (
          <li key={event.id}>{event.id}</li>
        ))}
      </ul>
    </div>
  );
};

export default ViewEventsCalendar;
