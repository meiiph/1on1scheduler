import React, { useState } from 'react';
import { useHistory, useParams } from 'react-router-dom'; // Import useHistory and useParams for navigation

const DeleteInvitation = () => {
  const [confirmation, setConfirmation] = useState(false); // State to track confirmation
  const { invitationId } = useParams(); // Get invitationId from URL params
  const history = useHistory(); // Initialize useHistory hook for navigation

  const handleDelete = async () => {
    try {
      const response = await fetch(`/api/invitations/${invitationId}/delete`, {
        method: 'DELETE',
        // headers: {
        //   'Authorization': `Bearer ${YOUR_AUTH_TOKEN}`,
        // },
      });
      if (response.ok) {
        alert('Invitation deleted successfully.');
        history.push('invitations/all'); // Navigate back to the ViewInvitations component
      } else {
        throw new Error('Failed to delete invitation.');
      }
    } catch (error) {
      console.error('Error deleting invitation:', error);
      alert('Failed to delete invitation.');
    }
  };

  return (
    <div>
      <h2>Delete Invitation</h2>
      {confirmation ? (
        <div>
          <p>Are you sure you want to delete this invitation?</p>
          <button onClick={handleDelete}>Yes, Confirm</button>
          <button onClick={() => setConfirmation(false)}>Cancel</button>
        </div>
      ) : (
        <div>
          <p>Click the button below to confirm deletion of the invitation.</p>
          <button onClick={() => setConfirmation(true)}>Delete Invitation</button>
        </div>
      )}
    </div>
  );
};

export default DeleteInvitation;
