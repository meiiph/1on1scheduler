import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom'; // Import useHistory for navigation

const ViewInvitations = () => {
  const [invitations, setInvitations] = useState([]);
  const [viewSentInvites, setViewSentInvites] = useState(true); // State to toggle between sent and received invites
  const [calendarNames, setCalendarNames] = useState({}); // State to store calendar names
  const history = useHistory(); // Initialize useHistory hook for navigation

  useEffect(() => {
    const fetchInvitations = async () => {
      try {
        const response = await fetch(`/OneOnOne/invitations/all'}`, {
          // headers: {
          //   'Authorization': `Bearer ${YOUR_AUTH_TOKEN}`,
          // },
        });
        if (response.ok) {
          const data = await response.json();
          setInvitations(data);
        } else {
          throw new Error('Failed to fetch invitations.');
        }
      } catch (error) {
        console.error('Error fetching invitations:', error);
      }
    };
    fetchInvitations();
  }, [viewSentInvites]); // Fetch invitations when viewSentInvites changes

  useEffect(() => {
    const fetchCalendarNames = async () => {
      const names = {};
      await Promise.all(
        invitations.map(async (invitation) => {
          try {
            const response = await fetch(`/OneOnOne/calendars/${invitation.calendar_id}`, {
            // headers: {
            // 'Authorization': `Bearer ${YOUR_AUTH_TOKEN}`,
            // },
            });
            if (response.ok) {
              const data = await response.json();
              names[invitation.calendar_id] = data.name;
            } else {
              throw new Error('Failed to fetch calendar name.');
            }
          } catch (error) {
            console.error('Error fetching calendar name:', error);
            names[invitation.calendar_id] = ''; // Set empty string if there's an error
          }
        })
      );
      setCalendarNames(names);
    };
    fetchCalendarNames();
  }, [invitations]); // Fetch calendar names when invitations change

  const handleRespond = (invitationId) => {
    history.push(`${invitationId}/respond`); // Navigate to the respond invitation component
  };

  const handleDelete = (invitationId) => {
    history.push(`${invitationId}/delete`); // Navigate to the delete invitation component
  };

  const sendReminderEmail = (recipientEmail) => {
    window.location.href = `mailto:${recipientEmail}?subject=Meeting%20Reminder&body=Hi%20there,%20just%20a%20reminder%20that%20you%20have%20not%20accepted%20the%20invitation%20I%20sent%20for%20our%20meeting.%20Please%20log%20into%20your%20account%20and%20accept%20or%20decline%20the%20invitation%20as%20soon%20as%20possible.%20Thanks!`;
  };
  
  return (
    <div>
      <h2>View Invitations</h2>
      <div>
        <button onClick={() => setViewSentInvites(true)}>View Sent Invitations</button>
        <button onClick={() => setViewSentInvites(false)}>View Received Invitations</button>
      </div>
      <div>
        {viewSentInvites ? (
          <div>
            <h3>Your Sent Invitations</h3>
            <ul>
              {invitations.map(invitation => (
                <li key={invitation.id}>
                  Receiver: {invitation.receiver.username}
                  Calendar: {calendarNames[invitation.calendar_id]}
                  Status: Pending
                  <button onClick={() => sendReminderEmail(invitation.receiver.email)}>Send Reminder Email</button>
                  <button onClick={() => handleDelete(invitation.id)}>Delete</button>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <div>
            <h3>Your Received Invitations</h3>
            <ul>
              {invitations.map(invitation => (
                <li key={invitation.id}>
                  Sender: {invitation.sender_username}
                  Calendar: {calendarNames[invitation.calendar_id]}
                  <button onClick={() => handleRespond(invitation.id)}>Respond</button>
                  <button onClick={() => handleDelete(invitation.id)}>Delete</button>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default ViewInvitations;
