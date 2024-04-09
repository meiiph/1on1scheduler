import { Component, Fragment } from "react";
import axios from "axios";
import { API_URL, TOKEN } from "../../constants/index";
import { Modal, ModalHeader, ModalFooter, Button } from "reactstrap";

class DeleteContactModal extends Component {
  state = {
    modal: false
  };

  toggle = () => {
    this.setState(previous => ({
      modal: !previous.modal
    }));
  };

  deleteContact = id => {
    const headers = {'Authorization': `Bearer ` + TOKEN};
    axios.delete(API_URL + "/contacts/" + id, { headers }).then(() => {
      this.props.resetState();
      this.toggle();
    });
  };

  render() {
    return (
      <Fragment>
        <Button color="danger" onClick={() => this.toggle()}>
          Delete
        </Button>
        <Modal isOpen={this.state.modal} toggle={this.toggle}>
          <ModalHeader toggle={this.toggle}>
            Are you sure you want to delete this contact?
          </ModalHeader>

          <ModalFooter>
            <Button type="button" onClick={() => this.toggle()}>
              Cancel
            </Button>
            <Button
              type="button"
              color="primary"
              onClick={() => this.deleteContact(this.props.id)}
            >
              Yes
            </Button>
          </ModalFooter>
        </Modal>
      </Fragment>
    );
  }
}

export default DeleteContactModal;