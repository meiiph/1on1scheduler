import React from 'react';
import { useHistory, useParams } from 'react-router-dom'; // Import useHistory and useParams for navigation

const RespondInvitation = () => {
  const { invitationId } = useParams(); // Get invitationId from URL params
  const history = useHistory(); // Initialize useHistory hook for navigation

  const handleAccept = async () => {
    try {
      const response = await fetch(`/OneOnOne/invitations/${invitationId}/respond`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        // 'Authorization': `Bearer ${YOUR_AUTH_TOKEN}`,
        },
        body: JSON.stringify({ status: 'accept' }),
      });
      if (response.ok) {
        alert('Invitation accepted.');
        history.push('invitations/all');
      } else {
        throw new Error('Failed to accept invitation.');
      }
    } catch (error) {
      console.error('Error accepting invitation:', error);
      alert('Failed to accept invitation.');
    }
  };

  const handleDecline = async () => {
    try {
      const response = await fetch(`/OneOnOne/invitations/${invitationId}/respond`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        // 'Authorization': `Bearer ${YOUR_AUTH_TOKEN}`,
        },
        body: JSON.stringify({ status: 'decline' }),
      });
      if (response.ok) {
        alert('Invitation declined.');
        history.push('invitations/all');
      } else {
        throw new Error('Failed to decline invitation.');
      }
    } catch (error) {
      console.error('Error declining invitation:', error);
      alert('Failed to decline invitation.');
    }
  };

  return (
    <div>
      <h2>Respond to Invitation</h2>
      <p>Do you want to accept or decline this invitation?</p>
      <button onClick={handleAccept}>Accept</button>
      <button onClick={handleDecline}>Decline</button>
    </div>
  );
};

export default RespondInvitation;
