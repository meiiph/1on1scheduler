import React, { useState, useEffect } from 'react';

const ViewEvents = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch('/calendars/my_events/');
        if (response.ok) {
          const data = await response.json();
          setEvents(data);
        } else {
          throw new Error('Failed to fetch events.');
        }
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    };
    fetchEvents();
  }, []);

  return (
    <div>
      <h2>My Events</h2>
      <ul>
        {events.map(event => (
          <li key={event.id}>{event.name} - {event.start_time}</li>
        ))}
      </ul>
    </div>
  );
};

export default ViewEvents;
