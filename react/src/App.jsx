// import Auth from "./Components/Auth/Auth"
// import Nav from "./Components/Nav/Nav"
// import Calendar from "./Components/Calendar/Calendar";
// import React from "react";
import { Component } from "react";
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import ContactsHome from "./Components/Contacts/ContactsHome";
import ViewEvents from "./Components/Event/ViewEvents";
import AddEvent from "./Components/Event/AddEvent"

class App extends Component {
  render () {
    return(
      <BrowserRouter>
        <Routes>
          <Route path={'/'}/>
          <Route path={'/contacts/'} element={<ContactsHome/>}/>
          <Route path={'/events/'} element={<ViewEvents/>}/>
          <Route path={'/add/'} element={<AddEvent/>}/>
        </Routes>
      </BrowserRouter>
    );
  }
}

export default App