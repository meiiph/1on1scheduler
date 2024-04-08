import React, { useState, useEffect } from 'react';

const ViewEvent = ({ eventId }) => {
  const [eventData, setEventData] = useState(null);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const response = await fetch(`/api/events/${eventId}/view/`);
        if (response.ok) {
          const data = await response.json();
          setEventData(data);
        } else {
          throw new Error('Failed to fetch event.');
        }
      } catch (error) {
        console.error('Error fetching event:', error);
      }
    };
    fetchEvent();
  }, [eventId]);

  if (!eventData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>View Event</h2>
      <p>Calendar: {eventData.calendar}</p>
      <p>Event Host: {eventData.event_host}</p>
      <p>Invited User: {eventData.invited_user}</p>
      {eventData.status === 'confirmed' ? (
        <>
          <p>Start: {eventData.start}</p>
          <p>Duration: {eventData.duration}</p>
        </>
      ) : (
        <>
          <p>Valid From: {eventData.valid_from}</p>
          <p>Valid To: {eventData.valid_to}</p>
          <p>Duration: {eventData.duration}</p>
        </>
      )}
    </div>
  );
};

export default ViewEvent;
