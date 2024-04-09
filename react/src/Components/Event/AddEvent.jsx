import React, { useState } from 'react';

const AddEvent = () => {
  const [eventData, setEventData] = useState({
    calendar: '',
    start_time: '',
    duration: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/calendars/create_event/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          
        },
        body: JSON.stringify(eventData)
      });
      if (response.ok) {
        alert('Event created successfully.');
      } else {
        throw new Error('Failed to create event.');
      }
    } catch (error) {
      console.error('Error creating event:', error);
      alert('Failed to create event.');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEventData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  return (
    <div>
      <h2>Add Event</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="calendar" placeholder="Calendar ID" onChange={handleChange} />
        <input type="text" name="start_time" placeholder="Start Time" onChange={handleChange} />
        <input type="text" name="duration" placeholder="Duration" onChange={handleChange} />
        <button type="submit">Create Event</button>
      </form>
    </div>
  );
};

export default AddEvent;
