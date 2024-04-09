import React from "react";
import { Form, FormGroup, Label, Input, Button } from "reactstrap";
import axios from "axios";
import { API_URL, TOKEN } from "../../constants/index";

class ContactForm extends React.Component {
  // Placeholder state values
  state = {
    id: 0,
    contact_user: "",
    name: "",
    email: ""
  };

  componentDidMount() {
    if (this.props.contact) {
      const { id, contact_user, name, email } = this.props.contact;
      this.setState({ id, contact_user, name, email });
    }
  }

  onChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

createContact = e => {
  e.preventDefault();
  const headers = { 'Authorization': `Bearer ` + TOKEN, 'Content-Type': 'application/json' };
  axios.post(API_URL + "/contacts/", JSON.stringify(this.state), {headers: headers}).then(() => {
    this.props.resetState();
    this.props.toggle();
  }).catch(function () {
    alert('Not all fields filled, username does not exist, or user already in your contacts.');
  });
}

// createContact = async (e) => {
//   // createContact = e => {
//     e.preventDefault();
//     // axios.post(API_URL, this.state).then(() => {
//     //   this.props.resetState();
//     //   this.props.toggle();
//     // });

//     try {
//       const response = await fetch('/contacts/', {
//         method: 'POST',
//         headers: {
//           // 'Authorization': `Bearer ${token}`,
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(this.state.contacts)
//       });
//       if (response.ok) {
//         this.props.resetState();
//         this.toggle();
//         alert('Contact created successfully.');
//       } else {
//         throw new Error('Failed to create contact.');
//       }
//     } catch (error) {
//       console.error('Error creating contact:', error);
//       alert('Failed to create contact.');
//     }
//   };


editContact = e => {
  e.preventDefault();
  const headers = { 'Authorization': `Bearer ` + TOKEN, 'Content-Type': 'application/json' };
  axios.put(API_URL + "/contacts/" + this.state.id +"/", JSON.stringify(this.state), {headers: headers}).then(() => {
    this.props.resetState();
    this.props.toggle();
  });
  // axios({url: API_URL + "/contacts/" + this.state.id, body: JSON.stringify(this.state), headers: headers, method: 'put'}).then(() => {
  //     this.props.resetState();
  //     this.props.toggle();
  //   });
}

// editContact = async (e) => {
//   // editContact = e => {
//     e.preventDefault();
//     // axios.put("http://localhost:8000/contacts/" + this.state.pk, this.state).then(() => {
//     //   this.props.resetState();
//     //   this.props.toggle();
//     // });
//     try {
//       const response = await fetch(API_URL + '/contacts/' +  this.state.pk, {
//         method: 'PUT',
//         headers: {
//           'Authorization': `Bearer ` + TOKEN,
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(this.state)
//       });
//       if (response.ok) {
//         this.props.resetState();
//         this.toggle();
//         alert('Contact updated successfully.');
//       } else {
//         throw new Error('Failed to update contact.');
//       }
//     } catch (error) {
//       console.error('Error updating contact:', error);
//       alert('Failed to update contact.');
//     }
//   };

  defaultIfEmpty = value => {
    return value === "" ? "" : value;
  };

  render() {
    return (
      <Form onSubmit={this.props.contact ? this.editContact : this.createContact}>
        <FormGroup>
          <Label for="contact_user">Username:</Label>
          <Input
            type="text"
            name="contact_user"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.contact_user)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="name">Name:</Label>
          <Input
            type="text"
            name="name"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.name)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="email">Email:</Label>
          <Input
            type="email"
            name="email"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.email)}
          />
        </FormGroup>
        <Button>Save</Button>
      </Form>
    );
  }
}

export default ContactForm;