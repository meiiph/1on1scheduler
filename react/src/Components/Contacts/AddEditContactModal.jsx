import { Component, Fragment } from "react";
import { Modal, ModalHeader, ModalBody, Button } from "reactstrap";
import ContactForm from "./ContactForm";

class AddEditContactModal extends Component {
  state = {
    modal: false
  };

  toggle = () => {
    this.setState(previous => ({
      modal: !previous.modal
    }));
  };

  render() {
    const create = this.props.create;

    var title = "Editing Contact";
    var button = <Button onClick={this.toggle}>Edit</Button>;
    if (create) {
      title = "Creating New Contact";

      button = (
        <Button
          color="primary"
          className="float-right"
          onClick={this.toggle}
          style={{ minWidth: "200px" }}
        >Add Contact</Button>
      );
    }

    return (
      <Fragment>
        {button}
        <Modal isOpen={this.state.modal} toggle={this.toggle}>
          <ModalHeader toggle={this.toggle}>{title}</ModalHeader>
          <ModalBody>
            <ContactForm
              resetState={this.props.resetState}
              toggle={this.toggle}
              contact={this.props.contact}
            />
          </ModalBody>
        </Modal>
      </Fragment>
    );
  }
}

export default AddEditContactModal;