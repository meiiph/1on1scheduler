import { useState, useEffect } from "react";
import { Table } from "reactstrap";
import AddEditContactModal from "./AddEditContactModal";
import DeleteContactModal from "./DeleteContactModal";

const ContactList = () => {
  const [contactsData, setContactsData] = useState([]);

  useEffect(() => {
    const fetchContacts = async () => {
      try {
        const response = await fetch(`http://localhost:8000/contacts/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (response.ok) {
          const data = await response.json();
          setContactsData(data);
        } else {
          throw new Error('Failed to fetch contacts.');
        }
      } catch (error) {
        console.error('Error fetching contacts:', error);
      }
    };
    fetchContacts();
  }, []);

  return (
    <section>
      <h2> Contacts</h2>
      <Table dark>
        <tbody>
          {!contactsData || contactsData.length <= 0 ? (
            <tr>
              <td colSpan="4" align="center">
                <b>You have no contacts!</b>
              </td>
            </tr>
          ) : (
            <thead>
              <tr>
                <th>Username</th>
                <th>Name</th>
                <th>Email</th>
                <th></th>
              </tr>
            </thead> &&
            contactsData.map(contact => (
              <tr key={contact.pk}>
                <td>{contact.contact_user}</td>
                <td>{contact.name}</td>
                <td>{contact.email}</td>
                <td align="center">
                  <AddEditContactModal
                    create={false}
                    contact={contact}
                    resetState={this.props.resetState}
                  />
                  &nbsp;&nbsp;
                  <DeleteContactModal
                    pk={contact.pk}
                    resetState={this.props.resetState}
                  />
                </td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    </section>
  );
}

export default ContactList;