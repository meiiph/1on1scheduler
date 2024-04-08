import React, { useState, useEffect } from 'react';

const ViewEventsCalendar = ({ calendarId }) => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const fetchCalendarEvents = async () => {
      try {
        const response = await fetch(`/calendars/calendar_events/${calendarId}/`);
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
  }, [calendarId]);

  return (
    <div>
      <h2>Calendar Events</h2>
      <ul>
        {events.map(event => (
          <li key={event.id}>{event.name} - {event.start_time}</li>
        ))}
      </ul>
    </div>
  );
};

export default ViewEventsCalendar;
