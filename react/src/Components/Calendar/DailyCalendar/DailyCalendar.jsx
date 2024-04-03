import React, { useState, useEffect } from 'react';
import './DailyCalendar.css'; // Import CSS for styling

const DailyCalendar = () => {
  const [events, setEvents] = useState([]);
  const currentDate = new Date();

  useEffect(() => {
    // Fetch events for the current date from your data source
    const fetchEvents = async () => {
      try {
        const response = await fetch(`/api/events/all`);
        if (response.ok) {
          const data = await response.json();
          setEvents(data);
        } else {
          throw new Error('Failed to fetch events');
        }
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    };
    fetchEvents();
  }, [currentDate]);

  // Function to format time (e.g., 09:00 AM)
  const formatTime = (timeString) => {
    return new Date(timeString).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
  };

  return (
    <div className="daily-calendar">
      <h2>{currentDate.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</h2>
      <div className="time-slots">
        {Array.from({ length: 24 }, (_, i) => {
          const startTime = `${i}:00`;
          const endTime = `${i + 1}:00`;
          const event = events.find(event => event.start.includes(startTime));
          return (
            <div key={i} className="time-slot">
              <div className="time">{formatTime(startTime)}</div>
              <div className="event">{event && event.title}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DailyCalendar;
