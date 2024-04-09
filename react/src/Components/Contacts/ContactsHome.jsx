import { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import ContactList from "./ContactList";
import AddEditContactModal from "./AddEditContactModal";
import axios from "axios";
import { API_URL, TOKEN} from "../../constants/index";
// import { useParams } from "react-router-dom";

class ContactsHome extends Component {
  state = {
    contacts: []
  };

  componentDidMount() {
    this.resetState();
  }

  getContacts = () => {
    // const { token } = useParams();
    // const headers = { 'Authorization': 'Bearer '+token, 'Content-Type': 'application/json' };
    const headers = { 'Authorization': `Bearer ` + TOKEN, 'Content-Type': 'application/json' };
    axios.get(API_URL + "/contacts/", { headers }).then(res => this.setState({ contacts: res.data }));

    // axios.get(API_URL + "/contacts/", {
    //       headers: {
    //           'Content-Type': 'application/json',
    //           'Authorization': 'Bearer '+token
    //       },      
    //   })      
    //   .then((response) => {
    //     console.log('response',response.data)

    //   })
    //   .catch((error) => {
    //     alert('error',error.response)
    //   })
  };

//   getContacts = () => {
//     // axios.get(API_URL).then(res => this.setState({ contacts: res.data }));
//     // const [contactsData, setContactsData] = useState([]);

//     // useEffect(() => {
//       const fetchContacts = async () => {
//         try {
//           const response = await fetch('/contacts/');
//           if (response.ok) {
//             const data = await response.json();
//             // setContactsData(data);
//             this.setState({ contacts: data})
//           } else {
//             throw new Error('Failed to fetch contacts.');
//           }
//         } catch (error) {
//           console.error('Error fetching contacts:', error);
//         }
//       };
//       fetchContacts();
//     // }, []);
//   };

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