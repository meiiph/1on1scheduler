import React from "react";
// import axios from "axios";
import { Form, FormGroup, Label, Input, Button } from "reactstrap";

class ContactForm extends React.Component {
  // Placeholder state values
  state = {
    pk: 0,
    contact_user: "",
    name: "",
    email: ""
  };

  componentDidMount() {
    if (this.props.contact) {
      const { pk, contact_user, name, email } = this.props.contact;
      this.setState({ pk, contact_user, name, email });
    }
  }

  onChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  createContact = async (e) => {
  // createContact = e => {
    e.preventDefault();
    // axios.post("http://localhost:8000/api/contacts/", this.state).then(() => {
    //   this.props.resetState();
    //   this.props.toggle();
    // });

    try {
      const response = await fetch('/contacts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.state.contacts)
      });
      if (response.ok) {
        this.props.resetState();
        this.toggle();
        alert('Contact created successfully.');
      } else {
        throw new Error('Failed to create contact.');
      }
    } catch (error) {
      console.error('Error creating contact:', error);
      alert('Failed to create contact.');
    }
  };

  editContact = async (e) => {
  // editContact = e => {
    e.preventDefault();
    // axios.put("http://localhost:8000/contacts/" + this.state.pk, this.state).then(() => {
    //   this.props.resetState();
    //   this.props.toggle();
    // });
    try {
      const response = await fetch('/contacts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.state)
      });
      if (response.ok) {
        this.props.resetState();
        this.toggle();
        alert('Contact updated successfully.');
      } else {
        throw new Error('Failed to update contact.');
      }
    } catch (error) {
      console.error('Error updating contact:', error);
      alert('Failed to update contact.');
    }
  };

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