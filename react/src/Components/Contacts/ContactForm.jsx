import React from "react";
import axios from "axios";
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

  createContact = e => {
    e.preventDefault();
    axios.post("http://localhost:8000/contacts/", this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  editContact = e => {
    e.preventDefault();
    axios.put("http://localhost:8000/contacts/" + this.state.pk, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
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