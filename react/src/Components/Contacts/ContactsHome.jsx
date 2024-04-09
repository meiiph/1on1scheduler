import { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import ContactList from "./ContactList";
import AddEditContactModal from "./AddEditContactModal";
// import axios from "axios";

class ContactsHome extends Component {
  state = {
    contacts: []
  };

  componentDidMount() {
    this.resetState();
  }

  getContacts = () => {
    // axios.get("http://localhost:8000/contacts/").then(res => this.setState({ contacts: res.data }));
    // const [contactsData, setContactsData] = useState([]);

    // useEffect(() => {
      const fetchContacts = async () => {
        try {
          const response = await fetch('/contacts/');
          if (response.ok) {
            const data = await response.json();
            // setContactsData(data);
            this.setState({ contacts: data})
          } else {
            throw new Error('Failed to fetch contacts.');
          }
        } catch (error) {
          console.error('Error fetching contacts:', error);
        }
      };
      fetchContacts();
    // }, []);
  };

  resetState = () => {
    this.getContacts();
  };

  render() {
    return (
      <Container style={{ marginTop: "20px" }}>
        <Row>
          <Col>
            <ContactList
              contacts={this.state.contacts}
              resetState={this.resetState}
            />
          </Col>
        </Row>
        <Row>
          <Col>
            <AddEditContactModal create={true} resetState={this.resetState} />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default ContactsHome;