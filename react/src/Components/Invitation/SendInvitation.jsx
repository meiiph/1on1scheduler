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
      // Iterate over selected contacts
      selectedContacts.forEach(contact => {
        // Construct the email body with the unique link
        const emailBody = `Dear ${contact.username},\n\nYou have been invited to schedule a regular meeting with ${loggedInUser}. Please click on the following link to specify your schedule and preferences:\n\n${generateUniqueLink(contact.id)}\n\nBest regards,\n${loggedInUser}`;
        
        // Generate mailto link
        const mailtoLink = `mailto:${contact.email}?subject=Invitation%20to%20Schedule%20a%20Meeting&body=${encodeURIComponent(emailBody)}`;
  
        // Open default email app with prefilled email
        window.open(mailtoLink);
      });
  
      // Reset form data after successful submission
      setFormData({ username: '', deadline: '' });
      setSelectedContacts([]);
      alert('Invitations sent successfully');
    } catch (error) {
      console.error('Error sending invitations:', error);
      alert('Failed to send invitations');
    }
  };

  const generateUniqueLink = (contactId) => {
    // Generate a unique link using the contact ID
    return `https://example.com/schedule-meeting/${contactId}`; // TODO: update with correct URL
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
